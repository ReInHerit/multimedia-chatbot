from .models import Question_Answer


def count_unusable():
    pronoun = 0
    data = Question_Answer.objects
    print("Numero totale di domande: ")
    print(data.count())
    pronoun1 = data.filter(answer="He").count()
    pronoun += pronoun1
    print("Numero di He: ")
    print(pronoun1)
    pronoun2 = data.filter(answer="She").count()
    pronoun += pronoun2
    print("Numero di She: ")
    print(pronoun2)
    pronoun3 = data.filter(answer="he").count()
    pronoun += pronoun3
    print("Numero di he: ")
    print(pronoun3)
    pronoun4 = data.filter(answer="she").count()
    pronoun += pronoun4
    print("Numero di she: ")
    print(pronoun4)
    pronoun5 = data.filter(answer="It").count()
    pronoun += pronoun5
    print("Numero di It: ")
    print(pronoun5)
    pronoun6 = data.filter(answer="it").count()
    pronoun += pronoun6
    print("Numero di it: ")
    print(pronoun6)
    pronoun7 = data.filter(answer="They").count()
    pronoun += pronoun7
    print("Numero di They: ")
    print(pronoun7)
    pronoun8 = data.filter(answer="they").count()
    pronoun += pronoun8
    print("Numero di they: ")
    print(pronoun8)
    pronoun9 = data.filter(answer="The painting").count()
    pronoun += pronoun9
    print("Numero di The painting: ")
    print(pronoun9)
    pronoun9b = data.filter(answer="the painting").count()
    pronoun += pronoun9b
    print("Numero di the painting: ")
    print(pronoun9b)
    pronoun10 = data.filter(answer="The work").count()
    pronoun += pronoun10
    print("Numero di The work: ")
    print(pronoun10)
    pronoun11 = data.filter(answer="This work").count()
    pronoun += pronoun11
    print("Numero di This work: ")
    print(pronoun11)
    pronoun12 = data.filter(answer="her").count()
    pronoun += pronoun12
    print("Numero di her: ")
    print(pronoun12)
    pronoun13 = data.filter(answer="Her").count()
    pronoun += pronoun13
    print("Numero di Her: ")
    print(pronoun13)
    pronoun14 = data.filter(answer="his").count()
    pronoun += pronoun14
    print("Numero di his: ")
    print(pronoun14)
    pronoun15 = data.filter(answer="His").count()
    pronoun += pronoun15
    print("Numero di His: ")
    print(pronoun15)
    pronoun16 = data.filter(answer="The subject").count()
    pronoun += pronoun16
    print("Numero di The subject: ")
    print(pronoun16)
    pronoun17 = data.filter(answer="this").count()
    pronoun += pronoun17
    print("Numero di this: ")
    print(pronoun17)
    pronoun18 = data.filter(answer="the work").count()
    pronoun += pronoun18
    print("Numero di the work: ")
    print(pronoun18)
    pronoun19 = data.filter(answer="this work").count()
    pronoun += pronoun19
    print("Numero di this work: ")
    print(pronoun19)
    pronoun20 = data.filter(answer="them").count()
    pronoun += pronoun20
    print("Numero di them: ")
    print(pronoun20)
    pronoun21 = data.filter(answer="there").count()
    pronoun += pronoun21
    print("Numero di there: ")
    print(pronoun21)
    pronoun22 = data.filter(answer="this work").count()
    pronoun += pronoun22
    print("Numero di this work: ")
    print(pronoun22)
    pronoun23 = data.filter(answer="the picture").count()
    pronoun += pronoun23
    print("Numero di the picture: ")
    print(pronoun23)
    pronoun24 = data.filter(answer="we").count()
    pronoun += pronoun24
    print("Numero di we: ")
    print(pronoun24)
    pronoun25 = data.filter(answer="you").count()
    pronoun += pronoun25
    print("Numero di you: ")
    print(pronoun25)
    pronoun26 = data.filter(answer="the fragment").count()
    pronoun += pronoun26
    print("Numero the fragment: ")
    print(pronoun26)
    pronoun27 = data.filter(answer="The fragment").count()
    pronoun += pronoun27
    print("Numero The fragment: ")
    print(pronoun27)
    pronoun28 = data.filter(answer="the panel").count()
    pronoun += pronoun28
    print("Numero the panel: ")
    print(pronoun28)
    pronoun29 = data.filter(answer="The panel").count()
    pronoun += pronoun29
    print("Numero The panel: ")
    print(pronoun29)
    pronoun30 = data.filter(answer="this painting").count()
    pronoun += pronoun30
    print("Numero this painting: ")
    print(pronoun30)
    pronoun31 = data.filter(answer="This painting").count()
    pronoun += pronoun31
    print("Numero This painting: ")
    print(pronoun31)
    pronoun32 = data.filter(answer="\tfirst").count()
    pronoun += pronoun32
    print("Numero first: ")
    print(pronoun32)
    pronoun33 = data.filter(answer="\tnow").count()
    pronoun += pronoun33
    print("Numero now: ")
    print(pronoun33)
    print("Numero totale di risposte non utili: ")
    print(pronoun)
    wi = data.filter(question="What is?").count()
    print(wi)


def num_of_words():
    data = Question_Answer.objects.all()
    count_two_el = 0
    count_more_seven = 0
    for element in data:
        splitted = element.question.split()
        if len(splitted) == 2:
            count_two_el = count_two_el + 1
        elif len(splitted) >= 10:
            count_more_seven = count_more_seven + 1
    print("numero di domande con due parole: ")
    print(count_two_el)
    print("numero di domande con più di 10 parole: ")
    print(count_more_seven)
