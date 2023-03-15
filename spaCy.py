#Téléchargement des packages Python/spaCy
#!python -m spacy download fr_core_news_sm

#Importation des packages Python/spaCy
import spacy
from spacy.matcher import Matcher
from spacy.lang.fr.examples import sentences 
import re


#Exemple de texte
text = "Selon Wikipédia il l'appelle laura, La ponctuation est génial l’ensemble des signes qui, dans l’écrit, marquent les divisions et les liaisons des phrases et des membres 'de phrase'. Vous pouvez en apprendre plus sur \"la ponctuation\" en visitant ce site: https://www.larousse.fr/dictionnaires/francais/ponctuation/63717 parce que ce lien donne beaucoup d'informations intéressantes. 😊"

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


def propNounRemoval(doc):
    result = []
    for token in doc:
        if not (token.ent_type_ == "ORG" or token.ent_type_ == "PERSON" or token.text.istitle()):
            result.append(token.text)
    return " ".join(result)


#run
doc = tokenisation(text)
modifiedText = explanationsRemoval(doc)
doc = tokenisation(modifiedText)
modifiedText = quotesRemoval(doc)
modifiedText = contactRemoval(modifiedText)
modifiedText = symbolsRemoval(modifiedText)
modifiedText = stopWordsRemoval(modifiedText)
doc = tokenisation(modifiedText)
modifiedText = propNounRemoval(doc)
print(modifiedText)