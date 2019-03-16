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
import pdb

# Définition locale de fonctions #

def prerequis():
    """La fonction prerequis() fait trois choses fondamentale, elle 
    vérifie que nous avons bien exécuter le script en mode root, puis 
    elle vérifie que l'on a bien passer un fichier en argument et enfin 
    que le fichier en question est bien un fichier valide c'est a dire qu'il a bien l’extension .csv.

    """
# Tout d'abord on vérifie que le script a bien été exécuté 
# en tant que root (la fonction geteuid() retourne l'identifiant 
# numérique de l'utilisateur) 0 dans le cas de root.

    if os.geteuid() != 0:
        print("Cette commande doit être lancée en tant que root!")
        sys.exit(0)

# Ensuite, on teste si le chemin du fichier CSV a été fourni 
# comme premier argument à la commande (si ce n'est pas le cas,
# on quitte le programme en rappelant que le fichier est 
# nécessaire):

    if len(sys.argv) > 1:
        global fichier_csv
        fichier_csv = sys.argv[1]
    else:
        print("Ou est le fichier .csv ?")
        sys.exit(0)

# Enfin, on vérifie que le fichier en question existe 
# (on stoppe le script s'il n'existe pas) et que l'extension du fichier
# est bien .csv pour évité d'ouvrir un autre type de fichier:

    exists = os.path.exists(fichier_csv)
# basename permet d'obtenir le nom d'un fichier et son extension à partir d'un chemin d'accès
    basename(fichier_csv)
    fileName, fileExtension = os.path.splitext(fichier_csv)

    if fileExtension != ".csv":
        print("L'extension du fichier n'est pas .csv!")
        sys.exit(0)

#######################################################################################
# La liste des données est lue ligne par ligne, la ligne 
# d'en-tête est supprimée et on formate les données:


def run():
    """La fonction run() permet de lire les lignes d'un fichier, de formater 
    les données et d’exécuter plusieurs fonctions permettant la création, modification des groupes
    et utilisateurs.

    """

    global groupe
    global user
    global path_csv
    global path_du_groupe
    global password
    global groupe_exist
    global user_exist

    f = open(fichier_csv, 'r')
    # On lit la première ligne du fichier
    line = f.readline()
    i = 1
    # readlines() va nous permettre de lire les différentes lignes du fichier sauf celle lu par readline()
    for line in f.readlines():
        # On découpe la ligne du fichier (slit) et on la sauvegarde dans un tableau
        tab = line.split(";")
        # strip() nous permet d’effacer des éléments indésirable ici des espaces et des tabulations
        # nous avons récupérez l'élément du tableau situé a l'indice 2 cela correspond au mot de passe
        # et nous l'avons stocker dans une variable password
        password = tab[2].strip('\t\t').strip('  ')
        # Nous avons appeler la fonction formatage() créer par nos soins 
        nom = formatage(tab[1]).strip('\t\t')
        prenom = formatage(tab[0]).strip('\t\t')
        # La variable groupe sera utiliser par la suite dans d'autre fonctions
        # Nous avons donc rendu sa portée globale
        groupe = formatage(tab[3]).strip('\t\t')
        # Création de la variable user en respectant le README
        user = nom + "_" + prenom
        # Le répertoire utlisateur tel qu'il devra être
        path_csv = "/home/" + groupe + "/" + user
        # Le HOME_DIR
        path_du_groupe = "/home/" + groupe + "/"
        ############################""
        # On cherche a répondre a la question /home/<groupe> exist? et 
        # groupe est dans /etc/group ? 
        read_groupe()
        # 
        read_user()
        #
        iter = 1
        while True:
            if groupe_exist:
                if path_du_groupe_exist:
                    if user_exist:
                        if user_path == path_csv:
                            break
                        else:
                            edit_user()
                            continue
                    else:
                        create_user()
                        continue
                else:
                    creer_path_groupe()
                    continue
            else:
                create_groupe()
                continue

            iter += 1

        i = i + 1
    f.close()

def formatage(valeur):
    """La fonction formatage() est chargée d'enlever les accents, les espaces de transformer la
    chaîne de caractères en minuscules d'enlever les retour chariot en fin de ligne et d’éliminer les tabulations. 
    
    """

    val = valeur.lower().replace("é", "e").replace(".", "").replace(" ", "").replace("è", "e").strip('\t\t').rstrip('\n\r')
    return val

def read_groupe():
    """La fonction read_groupe() permet de vérifier que le groupe passer en paramètre
    est bien dans le path /home/<groupe>/, elle enregistre True ou False dans
    la variable path_du_groupe_exist, elle permet aussi de vérifier que le groupe 
    existe dans /etc/group, d'enregistrer True ou False dans la variable 
    groupe_exist.
    
    """

    global path_du_groupe
    global path_du_groupe_exist
    global groupe_exist

    # Vérifier le path du groupe, qui doit être /home/<groupe>
    # Si le path existe return path_du_groupe_exist == True
    # Sinon return path_du_groupe_exist == False
    
    if os.path.exists(path_du_groupe):
        path_du_groupe_exist = True
    else:
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

        if c_groupe != groupe:
            groupe_exist = False
            continue
        else:
            groupe_exist = True
            break
        i = i + 1
    f.close()

    return groupe_exist, path_du_groupe_exist, path_du_groupe


def create_groupe():
    """La fonction create_groupe() permet de créer le groupe dans /etc/group 
    s'il n'existe pas.
    
    """

    global groupe_exist

    if not groupe_exist and groupe != "-":
        os.system("groupadd " + groupe)
        groupe_exist = True
    elif groupe == "-":
        groupe_exist = True
    else:
        groupe_exist = True

    return groupe_exist

def creer_path_groupe():
    """La fonction creer_path_groupe() permet de créer le /home/<groupe> s'il n'existe pas.
    
    """

    global path_du_groupe_exist
    global path_du_groupe

    if not path_du_groupe_exist:
        try:
            os.mkdir(path_du_groupe)
            path_du_groupe_exist = True
        except FileExistsError:
            path_du_groupe_exist = True
    else:
        path_du_groupe_exist = True

    return path_du_groupe_exist

def read_user():
    """La fonction read_user() permet de savoir si un utilisateur existe ou non dans 
    /etc/passwd nous enregistrons cette donnée dans la variable user_exist, elle nous 
    permet aussi de savoir quel est le path actuel de l'utilisateur nous enregistrons 
    cette information dans la variable user_path.
    
    """

    global user_exist
    global user_path
    global user_path_exist

    f = open("/etc/passwd", "r")
    i = 1
    for line in f.readlines():
        tab = line.split(':')
        c_user = tab[0]

        if c_user != user:
            user_path = ""
            user_path_exist = False
            user_exist = False
            continue
        else:
            user_path = tab[5]
            user_path_exist = True
            user_exist = True
            break
        i = i + 1
    f.close()

    return user_exist, user_path, user_path_exist

def create_user():
    """La fonction create_user() permet de créer un utilisateur s'il n'existe pas 
    dans /etc/passwd, et de retourner True or False a user_exist et user_path_exist
    
    """
    
    global user_exist
    global user
    global groupe
    global user_path
    global user_path_exist

    if not user_exist and groupe != "-":
        # Creation de l'utilisateur avec son mot de passe et son repertoire courant
        os.system("useradd -d /home/" + groupe + "/" + user + " -g " + groupe + " -s /bin/bash " + " --password  $(mkpasswd -H md5 " + password + " ) " + user )
        # A la premiere connextion l'utilisateur doit changer son mot de passe
        os.system("passwd -e " + user)
        user_exist = True
        # On verifier si l'utilisateur a exister par le passer
        read_deleted_user_file()
        # Modification apporter au path si l'utilisateur a exister par le passer
        creer_path_user()
        user_path_exist = True
    else:
        user_exist = True
        user_path_exist = True

    return user_exist, user_path_exist

def read_deleted_user_file():
    """La fonction read_deleted_user_file() cherche a répondre a la question l'utilisateur
    a-t-il déja exister? 

    """

    global user_a_exister
    global user
    global line

    f = open("/deleted_user_file.txt", 'r')
    i = 1
    for line in f.readlines():
        tab = line.split("-")
        name = tab[0]

        if name != user:
            user_a_exister = False
            continue
        else:
            user_a_exister = True
            # line correspond au nom d'utulisateur
            return line
            break
        i = i + 1
    f.close()

    return user_a_exister

def creer_path_user():
    """La fonction creer_path_user() permet de construire le repertoire courant
    de l'utilisateur, en tenant compte de son existance passer.

    """

    global user_path_exist
    global path_du_groupe
    global user_path
    global user_a_exister
    global line
    global groupe
    global user

    if not user_a_exister:
        try:
            # Si l'utilisateur n'a pas été créer préalablement
            os.mkdir(path_du_groupe + user)
            # Le répertoire squelette (/etc/skel/) contient les fichiers et 
            # répertoires qui seront copiés dans le répertoire 
            # personnel de l’utilisateur.
            os.system("cp -rT /etc/skel " + path_du_groupe + user)
            # Gestion des droits sur les fichiers du répertoire utilisateur 
            # le proprietaire des fichiers créer est l'utilisateur et son groupe est groupe
            os.system("chown -R " + user + ":" + groupe + " " + path_du_groupe + user)
            user_path_exist = True
            user_path = path_csv
        except FileExistsError:
            user_path_exist = True
    else:
        # Si l'utilisateur avait déja exister par le passer alors on désarchive son ancien répertoire 
        # qui se trouve dans /archives/
        os.system("cd " + path_du_groupe + " && tar -xvzf " + "/archives/" + line)
        # On detruit son tar.gz
        os.system("rm /archives/" + line)
        # On remet les droits adecuat sur les fichiers de tel maniere que le groupe corresponde bien
        os.system("chown -R " + user + ":" + groupe + " " + path_du_groupe + user)
        user_path_exist = True
        user_path = path_csv
        
    return user_path_exist, user_path

def edit_user():
    """La fonction edit_user() permet a condition que l'utilisateur existe et que 
    son path dans /etc/passwd soit différent du path que l'on a récupérez du fichier 
    .csv de déplacer son répertoire actuel dans un nouveau répertoire stipuler dans le fichier
    .csv.
    
    """

    global groupe

    if groupe == "-":
        try:
            deplacer_user()
            archiver_user()
            detruire_user()
        except FileExistsError:
            print("L'utilisateur a déjà été archiver.")
    else:
        deplacer_user()

    return 0

def archiver_user():
    """La fonction archiver_user() crée en premier lieu une archive au format gzip de l'utilisateur
    puis déplace le répertoire de l'utilisateur dans /archives/ et enfin supprime le répertoire de 
    l'utilisateur.
    
    """

    global user
    global user_path
    global path_csv
    global path_du_groupe
    global date

    if groupe == "-":
        backup_dir = "/archives/"
        targz = user + "-" + date + ".tar.gz"
        os.system("cd " + path_du_groupe + " && tar -czvf " + backup_dir + targz + " " + user + "/")
        os.system("rm -R " + user_path)

    return 0

def detruire_user():
    """La fonction détruire_user() ne fait pas que ça, elle sauvegarde le nom de l'utilisateur
    dans un fichier qui sera utiliser dans une autre fonction.

    """

    global path_du_groupe
    global user
    global user_exist
    global date

    os.system("userdel " + user)
    user_exist = False
    
    f = open("/deleted_user_file.txt", "a")
    targz = user + "-" + date + ".tar.gz"
    f.write(targz + "\n")
    f.close()
    
    try:
        os.system("rmdir " + path_du_groupe)
    except FileExistsError:
        print("Le répertoire n'est pas vide.")

    return user_exist

def deplacer_user():
    """La fonction deplacer_user() permet a condition que le path dans /etc/passwd
    ne corresponde pas au nouveau path stipuler dans fichier_csv, de déplacer le répertoire courant
    de l'utilisateur dans son nouveau répertoire.

    """

    global user_path
    global path_du_groupe
    global path_csv
    global user
    global groupe

    print("#######################################")

    if user_path != "" and (user_path != path_csv):
        os.system("cp -R " + user_path + " " + path_du_groupe)
        # Modification du path dans le fichier /etc/passwd
        os.system("usermod -d " + path_csv + " " + user)

        if groupe != "-":
            # Modification du nom du groupe
            os.system("usermod -g " + groupe + " " + user)
            # Modification des droits sur les fichiers de l'utilisateur
            os.system("chown -R " + user + ":" + groupe + " " + path_du_groupe + user)
        
        os.system("rm -R " + user_path)
        user_path = path_csv

    return user_path
    
        
#########################################################
if __name__ == '__main__':

    user_a_exister = False
    groupe_exist = False
    path_du_groupe_exist = False
    path_du_groupe = ""
    date = datetime.datetime.now().strftime("%d-%m-%y")
    user_exist = False
    user_path_exist = False
    user_path = ""
    line =""

    try:
        os.system("touch /deleted_user_file.txt")
    except FileExistsError:
        print("Le fichier existe déjà!")

    try:
        os.system("mkdir /archives/")
    except FileExistsError:
        print("Le répertoire existe déjà!")

    prerequis()
    run()
    
    print("#####  /etc/passwd  #################")
    os.system("tail -n 6 /etc/passwd")
    print("#####  /etc/shadow  #################")
    os.system("tail -n 6 /etc/shadow")
    print("#####  /etc/group  ####################")
    os.system("tail -n 8 /etc/group")
    print("#####  /home/*/*  #######################")
    os.system("ls -al /home/*/*")
    print("#####  /archives/  ####################")
    os.system("ls /archives/")
    print("#######################################")
