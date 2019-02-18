#!/usr/bin/python3
# -*- encoding:utf8 -*-

# Gestion des utilisateurs
# Victor Perez
# Licence: GPL

# Importation des fonctions externes

import os
import sys

# Tout d'abord on vérifie que le script a bien été exécuté 
# en tant que root (la commande getuid retourne l'identifiant 
# numérique de l'utilisateur)

if os.getuid == 0:
    print("Cette commande doit être lancée en tant que root.")
else:
    print("pass1")

# Ensuite, on teste si le chemin du fichier CSV a été fourni 
# comme premier argument à la commande (si ce n'est pas le cas,
# on quitte le programme en rappelant que le fichier est 
# nécessaire):

if len(sys.argv) != 1:
    fichier_csv = sys.argv[1]
    print("pass2")
else:
    print("Ou est le fichier .csv ?")

# Enfin, on vérifie que le fichier en question existe 
# (on stoppe le script s'il n'existe pas):

exists = os.path.exists(fichier_csv)
if exists:
    print("pass3")
else:
    print("Le fichier n'existe pas!")

##################################
# Définition locale de fonctions #
##################################

# La liste des données est lue ligne par ligne, la ligne 
# d'en-tête est supprimée:

def lire_lignes():
    """Cette fonction permet de lire une ligne 
    et de formatter les données"""
    f = open(fichier_csv, 'r')
    line = f.readline()
    i = 0
    while line != "":
        print(line)
        if i == 0:
            i = i + 1
            continue

        tab = line.split()
        print(tab)
        if tab != []:
            nom = formatage(tab[1])
            prenom = formatage(tab[0])
            groupe = formatage(tab[3])

            user = nom + "_" + prenom
            return user, groupe
            i = i + 1
    f.close()
#################################################


def formatage(valeur):
    val = valeur.lower().replace("é", "e").replace(".", "")
    return val

###################################################

def creer_groupe(user, groupe):
    
    path = "/home"
    path2 = os.path.join(path, groupe)
    path3 = os.path.join(path2, user)
    if os.path.exists(path2):
        print(path2, " exist!", " pass6")

        if os.path.exists(path3):
            print(path3, " exist!", " pass7")
        else:
            os.mkdir(path3)
            print(path3, "vient d'être crée!", " pass8")
    else:
        os.mkdir(path2)
        os.mkdir(path3)
        print("Le groupe: ", groupe, " et ", " l'utilisateur: ", user, " viennent d'être crées!" ," pass9")

 

########################################""

user, groupe = lire_lignes()
creer_groupe(user, groupe)
    
