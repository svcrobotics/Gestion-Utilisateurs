#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Gestion des utilisateurs
# Victor Perez
# Licence: GPL

# Importation des fonctions externes

import os
from os.path import basename
import sys
import datetime

# Définition locale de fonctions #
##################################

def verifier_fichier():
    '''
    La fonction verifier_fichier() fait trois chose fondamentale, elle 
    verifie que nous avons bien executer le script en mode root, puis 
    elle verifie que l'on a bien passer un fichier en argument et enfin 
    que le fichier en  question est bien un fichier valide c'est a dire qu'il a bien l'extention .csv.
    '''
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

#######################################################################################
# La liste des données est lue ligne par ligne, la ligne 
# d'en-tête est supprimée et on formatte les données:


def run():
    '''
    La fonction run() permet de lire les lignes d'un fichier, de formatter 
    les données et d'executer plusieurs fonctions permettant la création, modification des groupes
    et utilisateurs.
    '''

    global groupe
    global user
    global path_csv
    global path
    global password

    f = open(fichier_csv, 'r')
    # On lit la première ligne du fichier
    line = f.readline()
    i = 1
    # readlines() va nous permettre de lire les differentes lignes du fichier sauf celle lu par readline()
    for line in f.readlines():
        # On découpe la ligne du fichier (slit) et on la sauvegarde dans un tableau
        tab = line.split(";")
        # strip() nous permet déffacer des éléments indésirable ici des espaces et des tabulations
        # nous avons récuperez l'élément du tableau situé a l'indice 2 cela correspond au mot de passe
        # et nous l'avons stocker dans une variable password
        password = tab[2].strip('\t\t').strip('  ')
        # Nous avons appeller la fonction formatage() créer par nos soins 
        nom = formatage(tab[1]).strip('\t\t')
        prenom = formatage(tab[0]).strip('\t\t')
        # La variable groupe sera utiliser par la suite dans d'autre fonctions
        # Nous avons donc rendu sa portée globale
        groupe = formatage(tab[3]).strip('\t\t')
        #lieu = formatage(tab[4]).strip('\t\t')
        user = nom + "_" + prenom
        path_csv = "/home/" + groupe + "/" + user
        path = "/home/" + groupe + "/"
        ############################""
        # On cherche a repondre a la question /home/<groupe> exist? et 
        # groupe est dans /etc/group ? 
        read_groupe(groupe)
        print("groupe_exit", groupe_exist)
        read_user(user)
        print(user_exist, user_path)

        if groupe_exist or (groupe == "-"):
            #print(groupe)
            if path_du_groupe_exist:
                if user_exist:
                    print("L'utilisateur", user, "existe dans /etc/passwd.")
                    # Si on essaye de créer /home/<groupe>/<user> et qu'une erreur apparait
                    # de type FileExistsError alors le répertoire utilisateur existe déja.
                    if user_path == path_csv:
                        try:
                            os.mkdir(path_csv)
                        except FileExistsError:
                            print("Le repertoire utilisateur existe déja.")
                    else:
                        edit_user(user)
                else:
                    create_user(user_exist, user, password, groupe)
            else:
                creer_path_groupe(path_du_groupe_exist)
                if not user_exist:
                    create_user(user_exist, user, password, groupe)
                else:
                    edit_user(user)
        else:
            create_groupe(groupe_exist)
            print("groupe_exist", groupe_exist)

        i = i + 1
    f.close()

def formatage(valeur):
    ''' 
    La fonction formatage() est chargée d'enlever les accents, les espaces de transformer la
    chaîne de caractères en minuscules d'enlever les retour chariot en fin de ligne et d'eliminer les tabulations. 
    '''

    val = valeur.lower().replace("é", "e").replace(".", "").replace(" ", "").replace("è", "e").strip('\t\t').rstrip('\n\r')
    return val

def read_groupe(groupe):
    '''
    La fonction read_groupe() permet de vérifier que le groupe passer en paramètre
    est bien dans le path /home/<groupe>/, elle enregistre True ou False dans
    la variable path_du_groupe, elle permet aussi de verifier que le groupe 
    existe dans /etc/group et d'enregistrer True ou False dans la variable 
    groupe_exist.
    '''
    global path2
    global groupe_exist
    global path_du_groupe_exist

    # Verifier le path du groupe, qui doit etre /home/<groupe>
    # Si le path existe return path_du_groupe_exist == True
    # Sinon return path_du_groupe_exist == False
    path2 = os.path.join("/home/", groupe)
    if os.path.exists(path2):
        print("Le path du groupe", groupe, "exist!", path2)
        path_du_groupe_exist = True
    else:
        print("Le path du groupe:", groupe, "n'existe pas!")
        path_du_groupe_exist = False

    # Le groupe existe t-il dans /etc/group ?
    # Si oui return groupe_exist == True
    # Sinon return groupe_exist == False

    f = open("/etc/group", "r")
    i = 1
    for line in f.readlines():
        tab = line.split(':')
        # La première colonne dans /etc/group correspond on nom du groupe
        c_groupe = tab[0]
        gid = tab[2]

        if c_groupe != groupe:
            groupe_exist = False
            continue
        else:
            print("Le groupe", groupe, "existe bien dans /etc/group, " + "son GID est", gid)
            groupe_exist = True
            break
        i = i + 1
    f.close()
    return groupe_exist, path_du_groupe_exist


def create_groupe(groupe_exist):
    '''
    La fonction creer_groupe() permet de créer le groupe s'il n'existe pas.
    '''

    if not groupe_exist and groupe != "-":
        os.system("groupadd " + groupe)
        print("Le groupe", groupe, "vient d'etre creer dans /etc/group.")
        groupe_exist = True
    elif groupe == "-":
        print("Le groupe", groupe, "ne sera pas créer dans /etc/group.")
        groupe_exist = False
    else:
        print("Le groupe", groupe, "existe deja dans /etc/group.")
        groupe_exist = True


def creer_path_groupe(path_du_groupe_exist):
    '''
    La fonction creer_path_groupe() permet de créer le /home/<groupe> s'il n'existe pas.
    '''
    if not path_du_groupe_exist:
        try:
            os.mkdir(path2)
        except FileExistsError:
            print("Le path du groupe", groupe, "vient d'être créer!", path2)
            path_du_groupe_exist = True
    else:
        print("Le path du groupe", groupe, "a deja été créer!", path2)
        path_du_groupe_exist = True

    return path_du_groupe_exist

def read_user(user):
    '''
    La fonction read_user() permet de savoir si un utilisateur existe ou non dans 
    /etc/passwd nous enregistrons cette donnée dans la variable user_exist, elle nous 
    permet aussi de savoir quel est le path actuel de l'utilisateur nous enregistrons 
    cette information dans la variable user_path.
    '''
    global user_exist
    global user_path

    f = open("/etc/passwd", "r")
    i = 1
    for line in f.readlines():
        tab = line.split(':')
        c_user = tab[0]

        if c_user != user:
            user_path = ""
            user_exist = False
            continue
        else:
            #print("L'utilisateur", user, "existe dans /etc/passwd.")
            user_path = tab[5]
            user_exist = True
            break
        i = i + 1
    f.close()
    return user_exist, user_path

def create_user(user_exist, user, password, groupe):
    '''
    La fonction creer_user() permet de creer un utilisateur s'il n'existe pas 
    dans /etc/passwd.
    '''
    # Le répertoire squelette (/etc/skel/) contient les fichiers et 
    # répertoires qui seront copiés dans le répertoire 
    # personnel de l’utilisateur au moment de sa création.
    
    if user_exist == False and groupe != "-":
        os.system("useradd -d /home/" + groupe + "/" + user + " -g " + groupe + " -s /bin/bash " + " --password  $(mkpasswd -H md5 " + password + " ) " + user )
        os.system("passwd -e " + user)
        user_exist = True
        creer_path_user(user_exist)

    return user_exist

def creer_path_user(user_exist):
    if user_exist:
        os.mkdir(path2 + '/' + user)


def edit_user(user):
    '''
    La fonction edit_user() permet a condition que l'utilisateur existe et que 
    son path dans /etc/passwd soit different du path que l'on a récuperez du fichier 
    .csv de déplacer son répertoire actuel dans un nouveau répertoire stipuler dans le fichier
    .csv.
    '''
    global path_init
    global new_path

    # La variable globale user_path represente le path de l'utilisateur
    # dans /etc/passwd
    path_init = user_path
    new_path = path_csv
    # Si l'utilisateur existe et que son path actuel ne correspond pas avec son path futur
    if user_exist and ((path_init != new_path) or (groupe == "-")):
         
        #print("Le path", user_path, "existe dans /etc/passwd.")
        print(path_init, "-->", new_path)
        # Gestion erreur de type le fichier n'existe pas
        try:
            os.mkdir(path_init)
        except FileExistsError:
            print("Avant déplacement:", path_init)
            deplacer_user(path_init, path)
            print("Apres déplacement:", new_path)
            os.system("usermod -d " + new_path + " " + user)
            archiver_user(user)

def archiver_user(user):
    '''
    La fonction archiver_user() crée en premier lieu une archive au format gzip de l'utilisateur
    puis déplace le répertoire de l'utilisateur dans /archives/ et enfin supprime le répertoire de 
    l'utilisateur.
    '''
    date = datetime.datetime.now().strftime("%d-%m-%y")
    os.system("tar czvf " + user + ".tar.gz " + path_csv)
    os.system("mv " + path_csv + " /archives/" + user + "-" + date + ".tar.gz")
    # TODO: verifier archivage avant toute suppression
    os.system("rm -R " + path_csv)


def deplacer_user(path_init, path):
    '''
    La fonction deplacer_user() permet a condition que le path dans /etc/passwd
    ne corresponde pas au nouveau path stipuler dans fichier_csv, de déplacer le répertoire courant
    de l'utilisateur dans son nouveau répertoire.
    '''
    if path_init != new_path:
        os.system("mv " + path_init + " " + path)
            
#########################################################
if __name__ == '__main__':

    path = ""
    path_csv = ""
    password = ""
    groupe = ""
    user = ""
    path2 = ""

    verifier_fichier()
    run()
    print("####################################################")
    os.system("ls /home/*/*")
    #os.system("cat /etc/passwd")
