#!/usr/bin/python3
# -*- encoding:utf8 -*-

# Gestion des utilisateurs
# Victor Perez
# Licence: GPL

# Importation des fonctions externes

import os
from os.path import basename
import sys
import datetime

# Tout d'abord on vérifie que le script a bien été exécuté 
# en tant que root (la commande getuid retourne l'identifiant 
# numérique de l'utilisateur)

if os.getuid == 0:
    print("Cette commande doit être lancée en tant que root.")
else:
    print("Vous avez bien lancer la commande en tant que root => pass1")

# Ensuite, on teste si le chemin du fichier CSV a été fourni 
# comme premier argument à la commande (si ce n'est pas le cas,
# on quitte le programme en rappelant que le fichier est 
# nécessaire):

if len(sys.argv) != 1:
    fichier_csv = sys.argv[1]
    print("Vous avez bien passez un fichier en paramètre => pass2")
else:
    print("Ou est le fichier .csv ?")
    sys.exit()

# Enfin, on vérifie que le fichier en question existe 
# (on stoppe le script s'il n'existe pas):

exists = os.path.exists(fichier_csv)
basename(fichier_csv)
fileName, fileExtension = os.path.splitext(fichier_csv)
if exists and fileExtension == '.csv':
    print("Le fichier .csv existe => pass3")
else:
    print("Le fichier .csv n'existe pas!")
    sys.exit()

##################################
# Définition locale de fonctions #
##################################

# La liste des données est lue ligne par ligne, la ligne 
# d'en-tête est supprimée:

def lire_lignes():
    """Cette fonction permet de lire les lignes d'un fichier, de formatter 
    les données et de renvoyer un nom d'utilisateur et le groupe de l'utilisateur."""
    f = open(fichier_csv, 'r')
    line = f.readline()
    i = 1
    for line in f.readlines():
        
        tab = line.split()
        nom = formatage(tab[1])
        prenom = formatage(tab[0])
        groupe = formatage(tab[3])

        user = nom + "_" + prenom
        creer_groupe(user, groupe)

        i = i + 1
    f.close()
#################################################

def formatage(valeur):
    val = valeur.lower().replace("é", "e").replace(".", "")
    return val

###################################################
# 
def creer_groupe(user, groupe):
    
    path = "/home"
    path2 = os.path.join(path, groupe)
    global path3 
    path3 = os.path.join(path2, user)

    if os.path.exists(path2):
        print(path2, "Le groupe: ", groupe, "exist!", " pass6")

        if os.path.exists(path3):
            print(path3, " exist!", " pass7")
            if groupe == "-":
                print(user)
                #archiver_user(user)
        else:
            os.mkdir(path3)
            print(path3, "vient d'être crée!", " pass8")
    else:
        if groupe != "-":
            os.mkdir(path2)
            os.mkdir(path3)
            
            print("Le groupe: ", groupe, " et l'utilisateur: ", user, 
            " viennent d'être crées!" ," pass9")

############################################################
# La fonction suprimer_groupe essaie de supprimer le répertoire
# du groupe - si cela reussit, ça signifie que le groupe est vide
# on peut alors le supprimer.

def supprimer_groupe(groupe):
    os.system("rm -R /home/" + groupe)
    
###########################################################
# Pour archiver un utilisateur, il faut que Lieu soit égal à -
# dans le fichier .csv
# Une fois l'ordre reçu (d'archiver l'utilisateur) nous devons 
# procédé de la manière suivante:
# rechercher l'utilisateur en question dans tous les groupes 
# soit dans /home/*/nom_user
# targz le répertoire utilisateur
# le formater en ajoutant la notion de temps
# le déplacer dans /archives/
# et en dernier lieu le détruire de son groupe

def archiver_user(user):
    date = datetime.datetime.now().strftime("%d-%m-%y")
    os.system("tar czvf " + user + ".tar.gz " + path3)
    os.system("cp " + path3 + " /archives/" + user + "-" + date + ".tar.gz")
    os.system("rm -R " + path3)


def chercher_user(full_path):
    
    print("This file directory and name")
    path, filename = os.path.split(full_path)
    print(path + ' --> ' + filename + "\n")
##########################################

#lire_lignes()
jm = "jmtlg_planteur"
full_path = "/home/lancre/ciredutemps_esmeralda"
chercher_user(full_path)
groupe = "universite"
#supprimer_groupe(groupe)   
