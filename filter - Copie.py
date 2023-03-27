import pandas as pd
from langdetect import detect

# Charger le fichier CSV dans un dataframe
df = pd.read_csv('GooglePlayReviews.csv')

# Fonction pour détecter la langue d'un commentaire
def detect_language(comment):
    try:
        lang = detect(comment)
        return lang
    except:
        return None

# Filtrer les commentaires en français
df_fr = df[df['commentaire'].apply(lambda x: detect_language(x)=='fr')]

# Afficher les commentaires en français
print(df_fr['commentaire'])

df_fr.to_csv('Comments_Filtrés.csv', index=False)
