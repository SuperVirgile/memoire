import glob
import re
import nltk
import spacy
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import json
import string

#nltk.download("punkt")
#pour utiliser spacy avec des données en langue FR!!
nlp_fra = spacy.load("fr_core_news_sm")

#lit au fur et à mesure le fichier, tokenize (uniquement les données alpha numérique) et compte la liste finale pour définir la taille de nos données
#Avec ça, on pourra faire nos calculs!!
def definir_len_docs(chemin):
    tour = 0
    liste_finale = []
    for fichier in sorted(glob.glob(chemin)):
        f=open(fichier)
        document_html = f.read()
        f.close()
        documents = BeautifulSoup(document_html, "html.parser")
        tag = documents.find("div", type="article")
        token = nltk.tokenize.word_tokenize(tag.get_text())
        token_sans_ponctuation = [t for t in token if t.isalnum()]
        liste_finale = liste_finale + token_sans_ponctuation
        tour += 1
        test = len(liste_finale)
        print("tour : ", tour, "len fic : ", test)
        print(liste_finale)
    return liste_finale

#ouvre notre fichier et nous renvoie des données (pas utiliser ici car envoyé dans un json!!)
def ouvrir_traiter_fichier(chemin):
    donnee = []
    for fichier in sorted(glob.glob(chemin)):
        f=open(fichier)
        document_html = f.read()
        f.close()
        documents = BeautifulSoup(document_html, "html.parser")
        tag = documents.find("div", type="article")
        tag_text = tag.text
        donnee.append(tag_text)
    return str(donnee)

#compte les occurences des entités nommées et les range dans un dico
def compte_occurences_entite_nommee(dictionnaire, entite):
    try:
        dictionnaire[entite] = dictionnaire[entite] + 1
    except KeyError as e:
        dictionnaire[entite] = 1
    return

#renvoie dans la console le nom d'entité nommée avec l'entité en question et le nombre de fois qu'elle a été trouvé
def compte_nombre_occ_Ent(dictionnaire):

    for cle, iter in dictionnaire.items():
        print("L'entité nommée :", cle, "est compté :", iter, "fois dans le corpus.")

#compte le nombre d'occurence d'entité LOC dans un dictionnaire
def compte_nombre_occ_LOC(dictionnaire):
    nombre_LOC = 0
    for cle in dictionnaire.items():
        nombre_LOC = dictionnaire.get('LOC')
    return nombre_LOC

#compte le nombre d'occurence d'entité PER dans un dictionnaire
def compte_nombre_occ_PER(dictionnaire):
    nombre_PER = 0
    for cle in dictionnaire.items():
        nombre_PER = dictionnaire.get('PER')
    return nombre_PER

#compte le nombre d'occurence d'entité ORG dans un dictionnaire
def compte_nombre_occ_ORG(dictionnaire):
    nombre_ORG = 0
    for cle in dictionnaire.items():
        nombre_ORG = dictionnaire.get('LOC')
    return nombre_ORG

#calcul pourcentage
def Calcul_pourcentage(fichier, ent):
    fichier = len(fichier)
    pourcentage = ent / fichier
    return pourcentage

#Réalise un schéma basique pour pouvoir visualiser notre jeu de donnée
def faire_schema(total, lieu, personne, org):
    hauteur = [total, lieu, personne, org]
    barres = ("Total", "Lieu", "Personne", "Organisation")
    y_pos = np.arange(len(barres))
    plt.bar(y_pos, hauteur, color=['red', 'green', 'blue', 'yellow'])
    plt.xticks(y_pos, barres)
    plt.show()

#ouvre un fichier jason et return le contenu
def ouvrir_json(chemin):
    f = open(chemin, encoding="utf-8")
    doc = json.load(f)
    f.close()
    return doc

#retire la ponctuation d'une str sans se débarasser des "   '   "
def adieu_ponctuation(contenu):
    getrid_punct = string.punctuation
    getrid_punct = getrid_punct.replace("\'", "")
    regex = r"[{}]".format(getrid_punct)
    donneePropre = re.sub(regex, "", contenu)
    donneePropre = re.sub(' +', ' ', contenu)
    donneePropre = donneePropre.replace('\\n', '')
    return donneePropre

#Cette fonction nous renvoie un dictionnaire avec comme clé la str considérée comme une entité nommée et comme valeur une liste contenant
#son caracs de début et son caracs de fin.
def dico_carc_start_and_end(donnee):
    liste_start_end = []
    dic_start_end = {}
    for ent in donnee:
        liste_start_end = [ent.start_char, ent.end_char]
        dic_start_end[ent.text] = liste_start_end
    return dic_start_end


#Maintenant, on crée une fonction pour nettoyer nos données :
def nettoyer_texte_test(contenu):
    contenu = contenu.lower()
    contenu = re.sub('[%s]' % re.escape(string.punctuation), '', contenu) #on se débarasse de TOUTES les ponctuations
    return contenu

#on ouvre notre fichier qui a été traité avec definir_len_docs !
fichier = ouvrir_json('article1999_tokenizer.json')

#on ouvre notre fichier qui a été traité avec ouvrir_traiter_fichier - il s'agit d'une str, qu'on traite aussi avec la fonction adieu_ponctuation
donnee = adieu_ponctuation(ouvrir_json('article1999.json'))

doc_fr = nlp_fra(donnee) #hop, on traite nos données avec spacy
traitement = {} # un dic dans lequel on va ranger nos données traitées.
print(type(doc_fr))

#Là, on récupère les entités nommées et on crée un dico qui fonctionne ainsi :
#clé = la chaine de caractère correspondant à l'ent ; avec comme valeur le label_ (soit PER/ORG etc)
for ent in doc_fr.ents:
    traitement[ent.text] = ent.label_

jeu_de_donnee = list(traitement.values()) #notre jeu de donnée, une liste des valeurs de ce  dictionnaire
#soit une liste des MISC, LOC, PER etc -> on s'en sert ensuite avec len() pour obtenir la quantité d'entités nommées.

dic_ent = {} #notre dico d'ent
for entitee in jeu_de_donnee: #on s'en sert ici pour compter nos entités
    compte_occurences_entite_nommee(dic_ent, entitee)
compte_nombre_occ_Ent(dic_ent) #Display des occurences d'entités nommées
nombre_LOC = compte_nombre_occ_LOC(dic_ent) # On les compte selon leur type
nombre_PER = compte_nombre_occ_PER(dic_ent)
nombre_ORG = compte_nombre_occ_ORG(dic_ent)

#On calcule le pourcentage de nos entités ici :
pourcentage_ent = Calcul_pourcentage(fichier,len(jeu_de_donnee))
pourcentage_LOC = Calcul_pourcentage(fichier,nombre_LOC)
pourcentage_PER = Calcul_pourcentage(fichier,nombre_PER)
pourcentage_ORG = Calcul_pourcentage(fichier,nombre_ORG)
print(" Le corpus est composé à", pourcentage_ent*100, "% en tout d'entités nommées. Et ce sur", len(fichier), "tokens.")
print(" Le corpus est composé à", pourcentage_LOC*100, "% d'entités nommées de type \"Lieu\".")
print(" Le corpus est composé à", pourcentage_PER*100, "% d'entités nommées de type \"Personne\".")
print(" Le corpus est composé à", pourcentage_ORG*100, "% d'entités nommées de type \"Organisation\".")

#Schema représentatif :
faire_schema(len(jeu_de_donnee), nombre_LOC, nombre_PER, nombre_ORG)

# On utilise ici notre fonction pour voir le résultat !
dic_test_deux = dico_carc_start_and_end(doc_fr.ents)
print(dic_test_deux)
print(len(dic_test_deux))
