import json
import math
import os
import re
import urllib.parse
import requests
import wikipedia
from bs4 import BeautifulSoup


def get_wikipage_from_title(json_title):
    wiki_title = None
    wiki_page = None
    input_query = f"intitle:'{json_title}'"
    try:
        search = wikipedia.search(input_query, suggestion=False, results=50)
        founds = [item for item in search if 'disambiguation' not in item.lower()]
        if len(founds) == 1:
            # Unique title found
            wiki_title = founds[0]
        elif len(founds) > 1:
            exact_matches = [found for found in founds if json_title == found]
            if not exact_matches:
                exact_matches = [found for found in founds if json_title.lower() in found.lower()]
            if len(exact_matches) == 1:
                wiki_title = exact_matches[0]
            elif len(exact_matches) > 1:
                in_subject_matches = [found for found in exact_matches if "painting" in wikipedia.summary(found)]
                if len(in_subject_matches) >= 1:
                    wiki_title = in_subject_matches[0]
                else:
                    print("No matches found containing the word 'painting' in the title or summary.")
            else:
                matches_with_whole_title = [found for found in founds if json_title.lower() in found.lower()]
                if len(matches_with_whole_title) == 1:
                    wiki_title = matches_with_whole_title[0]
                elif len(matches_with_whole_title) > 1:
                    painting_matches = [found for found in founds if "painting" in found.lower()]
                    if len(painting_matches) == 1:
                        wiki_title = painting_matches[0]
                    elif len(painting_matches) > 1:
                        print("Multiple titles found, unable to determine a unique title.")
                    else:
                        in_subject_matches = [found for found in founds if "painting" in wikipedia.summary(found)]
                        if len(in_subject_matches) >= 1:
                            wiki_title = in_subject_matches[0]
                        else:
                            print("No matches found containing the word 'painting' in the title or summary.")
                else:
                    matches_with_founds = [found for found in founds if found.lower() in json_title.lower()]
                    if len(matches_with_founds) == 1:
                        wiki_title = matches_with_founds[0]

                    elif len(matches_with_founds) > 1:
                        in_subject_matches = [found for found in founds if "painting" in wikipedia.summary(found)]
                        if len(in_subject_matches) >= 1:
                            wiki_title = in_subject_matches[0]
                        else:
                            print("No matches found containing the word 'painting' in the title or summary.")
        else:
            disambiguos = [item for item in search[0] if 'disambiguation' in item.lower()]
            print('disambiguous: ', disambiguos)
            print("No titles found matching the given title.")
        if wiki_title:
            wiki_page = wikipedia.WikipediaPage(wiki_title)

    except wikipedia.exceptions.DisambiguationError as e:
        print(f"DisambiguationError: {e.options}")
        in_subject_matches = [found for found in e.options if "painting" in wikipedia.summary(found)]
        if len(in_subject_matches) >= 1:
            wiki_title = in_subject_matches[0]
        else:
            wiki_title = e.options[0]
            print("No matches found containing the word 'painting' in the title or summary.")
        wiki_page = wikipedia.WikipediaPage(wiki_title)
        wiki_title = wiki_page.title

    except wikipedia.exceptions.PageError:
        print(f"PageError: {json_title}")
        wiki_page = wikipedia.WikipediaPage(json_title)
        wiki_title = wiki_page.title
    return wiki_page, wiki_title


def get_context(wiki_page):
    excluded_titles = ["Notes", "References", "External links", "Further reading", "See also", "Sources",
                       "Bibliography", "Literature", "Gallery", "Citations"]
    whole_text = wiki_page.content

    # Extract sections and subsections from the Wikipedia page
    pattern = r'==+\s*([\w\s]+)\s*==+'
    matches = re.findall(pattern, whole_text)
    sections = [match.strip() for match in matches if match.strip() not in excluded_titles]
    section_content = [f"{section}:\n{wiki_page.section(section)}" for section in sections if wiki_page.section(section)]
    section_content = "\n".join(section_content)
    content = f"{wiki_page.summary}\n{section_content}"
    content = re.sub(r'\n{2,}', '\n', content)

    # Split content into sentences
    sentences = re.split(r'(?<=[.!?])\s+(?=\")|\n', content)

    return sentences


def get_image_url(wiki_title, wiki_url):
    image_url_partial = 'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='
    main_image_api_request_url = image_url_partial + urllib.parse.quote(wiki_title.replace(' ', '_'))

    response = requests.get(main_image_api_request_url)
    data = response.json()
    pages = data['query']['pages']
    page_id = next(iter(pages))
    main_image_url = pages[page_id].get('original', {}).get('source', '')
    # print('0 main_image_url', main_image_url)
    if not main_image_url:
        response = requests.get(wiki_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            infobox = soup.find('table', class_='infobox')
            if infobox:
                main_image = infobox.find('img')
            else:
                main_image = soup.find('img', class_='image')

            if not main_image:
                thumbinner_divs = soup.find_all('div', class_='thumbinner')
                if thumbinner_divs:
                    first_thumbinner_div = thumbinner_divs[0]
                    main_image = first_thumbinner_div.find('img')

            main_image_url = main_image.get('src') if main_image else None
            if main_image_url and 'thumb' in main_image_url:
                main_image_url = main_image_url.replace('/thumb', '')
                main_image_url = main_image_url.rsplit('/', 1)[0]
            # Prepend 'https:' to the URL if the scheme is missing
            if main_image_url and not main_image_url.startswith('https:'):
                main_image_url = 'https:' + main_image_url
        else:
            print('Failed to retrieve the Wikipedia page.')
    return main_image_url


def get_year(wiki_title):
    wikidata = 'https://www.wikidata.org/w/api.php?action=wbgetentities&sites=enwiki&props=claims&format=json&titles=' +\
               urllib.parse.quote(wiki_title.replace(' ', '_'))
    response_year = requests.get(wikidata)
    year_data = response_year.json()
    inbox_year = None
    if 'claims' in year_data['entities'][next(iter(year_data['entities']))] and \
            'P571' in year_data['entities'][next(iter(year_data['entities']))]['claims']:
        claims = year_data['entities'][next(iter(year_data['entities']))]['claims']['P571']
        for claim in claims:
            if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
                year_value = claim['mainsnak']['datavalue']['value']['time']
                inbox_year = year_value.strip('+').split('-')[0]
                break
            elif 'qualifiers' in claim and 'P1319' in claim['qualifiers'] and 'datavalue' in \
                    claim['qualifiers']['P1319'][0]:
                year_value = claim['qualifiers']['P1319'][0]['datavalue']['value']['time']
                inbox_year = year_value.strip('+').split('-')[0]
                break
        else:
            inbox_year = 3000
    else:
        inbox_year = 3000
    if len(str(inbox_year)) != 4:
        inbox_year = 3000
    return inbox_year
