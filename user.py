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



##################################
# Définition locale de fonctions #
##################################

def start():
# Tout d'abord on vérifie que le script a bien été exécuté 
# en tant que root (la fonction geteuid() retourne l'identifiant 
# numérique de l'utilisateur) 0 dans le cas de root.

    if os.geteuid() == 0:
        print("Vous avez bien lancer le script en tant que root.")
    else:
        print("Cette commande doit être lancée en tant que root!")
        sys.exit(0)

# Ensuite, on teste si le chemin du fichier CSV a été fourni 
# comme premier argument à la commande (si ce n'est pas le cas,
# on quitte le programme en rappelant que le fichier est 
# nécessaire):

    if len(sys.argv) > 1:
        global fichier_csv
        fichier_csv = sys.argv[1]
        print("Vous avez bien passez un fichier en paramètre.")
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
        print("Le fichier .csv existe.")
    else:
        print("Le chemin du fichier .csv est incorrect ou l'extension de celui-ci n'est pas .csv!")
        sys.exit(0)


# La liste des données est lue ligne par ligne, la ligne 
# d'en-tête est supprimée:

def lire_lignes():
    """Cette fonction permet de lire les lignes d'un fichier, de formatter 
    les données et de renvoyer un nom d'utilisateur et le groupe de l'utilisateur."""
    f = open(fichier_csv, 'r')
    line = f.readline()
    i = 1
    for line in f.readlines():
        
        tab = line.split(";")
        password = tab[2].strip('\t\t').strip('  ')
        nom = formatage(tab[1]).strip('\t\t')
        prenom = formatage(tab[0]).strip('\t\t')
        global groupe
        groupe = formatage(tab[3]).strip('\t\t')
        lieu = formatage(tab[4]).strip('\t\t')
        global user
        user = nom + "_" + prenom
        global path_csv
        path_csv = "/home/" + groupe + "/" + user
        global path
        path = "/home/" + groupe + "/"
        ############################""
        lire_groupe(groupe)
        creer_groupe(groupe)
        creer_path_groupe(groupe)

        chercher_user(user)
        modifier_user(user, user_path, path_csv)
        creer_user(user, password, groupe)
        ####################"""
        i = i + 1
    f.close()
#################################################

def formatage(valeur):
    val = valeur.lower().replace("é", "e").replace(".", "").replace(" ", "").replace("è", "e").strip('\t\t').rstrip('\n\r')
    return val

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
    os.system("mv " + path3 + " /archives/" + user + "-" + date + ".tar.gz")
    #os.system("rm -R " + path3)

#################################################################""""
def chercher_user(user):
    global user_exist
    f = open("/etc/passwd", "r")
    i = 1
    for line in f.readlines():
        tab = line.split(':')
        c_user = tab[0]
        uid = tab[2]
        gid = tab[3]

        if c_user != user:
            user_exist = False
            continue
        else:
            #print("L'utilisateur", user, "existe dans /etc/passwd.")
            global user_path
            user_path = tab[5]
            #print("dans /etc/passwd", user_path)
            user_exist = True
            break
        
        i = i + 1
    f.close()
######################################################################################
def creer_user(user, password, groupe):
    # Le répertoire squelette (/etc/skel/) contient les fichiers et 
    # répertoires qui seront copiés dans le répertoire 
    # personnel de l’utilisateur au moment de sa création.
    
    if not user_exist:
        os.system("useradd -d /home/" + groupe + "/" + user + " -g " + groupe + " -s /bin/bash " + " --password  $(mkpasswd -H md5 " + password + " ) " + user )
        os.system("passwd -e " + user)
###################################################################################
def modifier_user(user, user_path, path_csv):
    global path_init
    global new_path
    path_init = user_path
    new_path = path_csv
    # Si l'utilisateur existe
    if user_exist and (path_init != new_path):
        #print("Le path", user_path, "existe dans /etc/passwd.")
        print(path_init, "-->", new_path)
        try:
            os.mkdir(path_init)
        except FileExistsError:
            deplacer_user(path_init, path)
            os.system("usermod -d " + new_path + " " + user)
######################################################""

def supprimer_user(user):
    os.system("userdel -r -f " + user)
#################################################################""
def deplacer_user(path_init, path):
    if path_init != new_path and groupe != "-":
        os.system("mv " + path_init + " " + path)

########################################################################
#####################################################################

def lire_groupe(groupe):
    # Verifier le path du groupe
    global path2
    path2 = os.path.join("/home/", groupe)
    if os.path.exists(path2):
        #print("Le path du groupe", groupe, "exist!", path2)
        global path_du_groupe
        path_du_groupe = True
    else:
        print("Le path du groupe:", groupe, "n'existe pas!")

    # Verifier /etc/group
    f = open("/etc/group", "r")
    i = 1
    for line in f.readlines():
        tab = line.split(':')
        c_groupe = tab[0]
        gid = tab[2]

        if c_groupe != groupe:
            continue
        else:
            #print("Le groupe", groupe, "existe bien dans /etc/group, " + "son GID est", gid)
            global groupe_exist
            groupe_exist = True
            break
        i = i + 1
    f.close()

####################################################################

def creer_groupe(groupe):
    if not groupe_exist and groupe != "-":
        os.system("groupadd " + groupe)

######################################################################

def creer_path_groupe(groupe):
    if not path_du_groupe:
        os.mkdir(path2)
        print("Le path du groupe", groupe, "vient d'être créer!", path2)

####################################################################
# La fonction suprimer_groupe essaie de supprimer le répertoire
# du groupe - si cela reussit, ça signifie que le groupe est vide
# on peut alors le supprimer.
def supprimer_path_groupe(groupe):
    os.system("rm /home/" + groupe)

def supprimer_groupe(groupe):
    os.system("groupdel " + groupe)

##########################################:

if __name__ == '__main__':
    print("####################################################")
    start()
    print("####################################################")
    lire_lignes()
    print("####################################################")
    