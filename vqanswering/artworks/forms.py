from django import forms
import json


class ImportArtworksForm(forms.Form):
    json_file = forms.FileField(label='Select JSON file')

    def clean_json_file(self):
        json_file = self.cleaned_data.get('json_file')
        if json_file:
            try:
                artworks = json.loads(json_file.read().decode('utf-8'))
                return artworks
            except:
                raise forms.ValidationError('Invalid JSON file.')
        else:
            raise forms.ValidationError('Please select a JSON file.')
