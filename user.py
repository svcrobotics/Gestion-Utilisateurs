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
# en tant que root (la fonction geteuid() retourne l'identifiant 
# numérique de l'utilisateur) 0 dans le cas de root.

if os.geteuid() == 0:
    print("Vous avez bien lancer le script en tant que root. => pass1")
else:
    print("Cette commande doit être lancée en tant que root!")
    sys.exit(0)

# Ensuite, on teste si le chemin du fichier CSV a été fourni 
# comme premier argument à la commande (si ce n'est pas le cas,
# on quitte le programme en rappelant que le fichier est 
# nécessaire):

if len(sys.argv) > 1:
    fichier_csv = sys.argv[1]
    print("Vous avez bien passez un fichier en paramètre. => pass2")
else:
    print("Ou est le fichier .csv ?")
    sys.exit(0)

# Enfin, on vérifie que le fichier en question existe 
# (on stoppe le script s'il n'existe pas) et que l'extension du fichier
# est bien .csv pour evité d'ouvrir un autre type de fichier:

exists = os.path.exists(fichier_csv)
# basename permet d'obtenir le nom d'un fichier et son extension à partir d'un chemin d'accès
basename(fichier_csv)
fileName, fileExtension = os.path.splitext(fichier_csv)
if exists and fileExtension == '.csv':
    print("Le fichier .csv existe => pass3")
else:
    print("Le chemin du fichier .csv est incorrect ou l'extension de celui-ci n'est pas .csv!")
    sys.exit(0)

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
        password = tab[2]
        nom = formatage(tab[1])
        prenom = formatage(tab[0])
        groupe = formatage(tab[3])
        user = nom + "_" + prenom
        #creer_groupe(user, groupe, password)

        i = i + 1
    f.close()
#################################################

def formatage(valeur):
    val = valeur.lower().replace("é", "e").replace(".", "").rstrip('\n\r')
    return val

###################################################
# 
'''
def creer_groupe(user, groupe, password):

    path = "/home"
    path2 = os.path.join(path, groupe)
    path3 = os.path.join(path2, user)

    if os.path.exists(path2):
        print(path2, "Le groupe: ", groupe, "exist!", " pass6")

        if os.path.exists(path3):
            print(path3, " exist!", " pass7")
        else:
            os.mkdir(path3)
            print(path3, "vient d'être crée!", " pass8")
    else:
        
        os.mkdir(path2)
        os.system("groupadd " + groupe)
        
        creer_user(user, password, groupe)
        print("Le groupe: ", groupe, " et l'utilisateur: ", user, " viennent d'être crées!" ," pass9")
'''
def creer_groupe(groupe):
    path = "/home/" + groupe
    os.mkdir(path)
    os.system("groupadd " + groupe)

############################################################
# La fonction suprimer_groupe essaie de supprimer le répertoire
# du groupe - si cela reussit, ça signifie que le groupe est vide
# on peut alors le supprimer.

def supprimer_groupe(groupe):
    
    os.system("groupdel " + groupe)
    os.system("rm -R /home/" + groupe + "/*")

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


def chercher_user(user):
    print(os.system("id -u " + user))
    print(os.system("id -g " + user))
    print(os.system("echo ~" + user))

def creer_user(user, password, groupe):
    # Le répertoire squelette (/etc/skel/) contient les fichiers et 
    # répertoires qui seront copiés dans le répertoire 
    # personnel de l’utilisateur au moment de sa création.
    
    os.system("useradd -d /home/" + groupe + "/" + user + " -s /bin/bash " + " -g " + groupe + " --password  $(mkpasswd -H md5 " + password + " ) " + user )
    #os.mkdir("/home/" + groupe + "/" + user)
    os.system("passwd -e " + user)
    os.system("cp -r /etc/skel/* /home/" + groupe + "/" + user + "/")
    print(os.system("ls -al /home/"+ groupe + "/" + user))

def delete_user(user):
    os.system("userdel -r -f " + user)

 
##########################################
print("####################################################")
#lire_lignes()
print("####################################################")
#chercher_user()
#supprimer_groupe(groupe)   
#print(os.system("cat /etc/group"))
#print(os.system("cat /etc/shadow"))

###############################""

#creer_groupe("admin")
creer_user("victor", "Victor@1972", "admin")
#chercher_user("victor")
#delete_user('victor')
#supprimer_groupe("admin")