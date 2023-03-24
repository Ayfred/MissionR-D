#Téléchargement des packages Python/spaCy
#!python -m spacy download fr_core_news_sm

#Importation des packages Python/spaCy
import spacy
import re
import csv

# open the CSV file using the csv module
with open('MissionR-D/GooglePlayComments.csv', newline='',  encoding='utf-8') as csvfile:
    # create a csv reader object
    reader = csv.reader(csvfile)
    # create an empty list to store the strings
    string_list = []
    # loop through each row in the CSV file
    for row in reader:
        # add the string to the list
        #print(row)
        string_list.append(row[0])

# print the list of strings
print(string_list)

string_list_clean = []


#Exemple de texte
text = "Selon Wikipédia il l'appelle Laura 😊😊😊(hezignborzingiozrnoivznioznvionzo), La ponctuation est génial l’ensemble des signes qui, dans l’écrit, marquent les divisions et les liaisons des phrases et des membres 'de phrase'. Vous pouvez en apprendre plus sur \"la ponctuation\" en visitant ce site: https://www.larousse.fr/dictionnaires/francais/ponctuation/63717 parce que ce lien donne beaucoup d'informations intéressantes. 😊"
#text = "Fonctionnalités, salut car beau temps aujourd'hui"

#Etapes du texte Preprocessing
nlp = spacy.load("fr_core_news_sm")
listStopWords = [str(x) for x in nlp.Defaults.stop_words]

#Tokenisation
def tokenisation(text):
    return nlp(text)

#Affichage des tokens
def affichage_tokens(doc):
    for token in doc:
        # Print the text and the predicted part-of-speech tag
        print(token.text, token.pos_)

#Removal of explanations
def explanationsRemoval(doc):
    sentence = doc.text
    # Itérer à travers chaque token dans le document
    for token in doc:
        # Si le token est "parce que", "car" ou "puisque", supprimer tous les tokens suivants dans la phrase
        if token.text.lower() in ["parce", "car", "puisque"]:
            sentence = sentence[:token.idx]
            break
    # Supprimer tout ce qui est entre parenthèses
    sentence = re.sub(r'\([^()]*\)', '', sentence)
    return sentence

#Removal of quotes
def quotesRemoval(doc):
    filtered_text = ""
    Punc_list = ['"', "'"]
    boolean_punct = False
    for token in doc:
        if not token.text in Punc_list:
            if not boolean_punct:
                filtered_text += token.text
                filtered_text += " "
        else :
            if boolean_punct :
                boolean_punct = False
            else :
                boolean_punct = True
    return filtered_text

#Removal of ' and the char that precede it
def apostropheRemoval(doc):
    for token in doc:
        if token.text == "'":
            filtered_text += token.text
            filtered_text += " "
    return filtered_text

#Removal of URLs
def urlRemoval(text):
    return re.sub('http[s]?://\S+', '', text)

#Removal of contact information
def contactRemoval(text):
    # Regular expressions for phone numbers and email addresses
    phone_regex = r"(?<!\d)(?:\d[ -/\\_\d]*){10}(?!\d)"
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # matches john.doe@example.com

    # Find phone numbers and email addresses in the sentence
    text = re.sub(phone_regex,"", text)
    text = re.sub(email_regex,"", text)

    return text

#Removal of symbols
def symbolsRemoval(text):
    return re.sub(r'[^\w]', ' ', text)

#Removal of stop words
def stopWordsRemoval(text):
    splitext = text.split(" ")
    for word in splitext:
        if word in listStopWords:
            splitext.remove(word)
    return ' '.join(splitext)

def pronounAndDetRemoval(doc):
    #texte = doc.text
    sentence = ""
    for token in doc:
        if (token.pos_ == "PRON" or token.pos_ == "DET"):
            continue
        else:
            sentence += token.text_with_ws
            sentence += " "
    return sentence

def propNounRemoval(doc):
    result = []
    for token in doc:
        if not (token.ent_type_ == "ORG" or token.ent_type_ == "PERSON" or token.text.istitle()):
            result.append(token.text)
    return " ".join(result)

def united(text):
    doc =  text.split(" ");
    # Itérer à travers chaque token dans le document
    for token in doc:

        #Remove explanations
        # Si le token est "parce que", "car" ou "puisque", supprimer tous les tokens suivants dans la phrase
        if token in ["parce", "car", "puisque"]:
            doc = doc[:token.index()]
            break
    
    # Supprimer tout ce qui est entre parenthèses
    sentence = ' '.join(doc)
    sentence = re.sub(r'\([^()]*\)', '', sentence)

    doc = sentence.split(" ")
    #Filter
    filtered_text = ""
    Punc_list = ['"', "'"]
    boolean_punct = False
    for token in doc:
        if not token in Punc_list:
            if not boolean_punct:
                filtered_text += token.text
                filtered_text += " "
        else :
            boolean_punct = not boolean_punct

    sentence = filtered_text
    sentence = re.sub('http[s]?://\S+', '', sentence)

    # Regular expressions for phone numbers and email addresses
    phone_regex = r"(?<!\d)(?:\d[ -/\\_\d]*){10}(?!\d)"
    email_regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # matches john.doe@example.com

    # Find phone numbers and email addresses in the sentence
    sentence = re.sub(phone_regex,"", sentence)
    sentence = re.sub(email_regex,"", sentence)
    sentence = re.sub(r'[^\w]', ' ', sentence)
    doc = sentence.split(" ")
    for word in doc:
        if word in listStopWords:
            doc.remove(word)
    
    sentence = ' '.join(doc)
    doc = nlp(sentence)
    #texte = doc.text
    text = ""
    for token in doc:
        if (token.pos_ == "PRON" or token.pos_ == "DET"):
            continue
        else:
            if not token.text == "'":
                text += token.text
                text += " "
    sentence = text

    doc = nlp(sentence)
    result = []
    for token in doc:
        if not (token.ent_type_ == "ORG" or token.ent_type_ == "PERSON" or token.text.istitle()):
            result.append(token.text)
    sentence =  " ".join(result)

    return sentence


for string in string_list:
    united_string = united(string)
    string_list_clean.append(united_string)
print(string_list_clean)
#run
#print(united(text))