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

# Variables globales

groupe_exist = False
groupe = "superadmin"
path_du_groupe_exist = False
user_exist = False
user = "victor_perez"
password = "Victor@1972"

def create_groupe():
    '''
    La fonction create_groupe() permet de créer le groupe s'il n'existe pas.
    Cela veut
    '''
    global groupe_exist
    global groupe

    if not groupe_exist :
        try:
            os.system("groupadd " + groupe)
            groupe_exist = True
        except FileExistsError:
            groupe_exist = True
    else:
        groupe_exist = True

    return groupe_exist

def creer_path_groupe():
    '''
    La fonction creer_path_groupe() permet de créer le /home/<groupe> s'il n'existe pas.
    '''
    global path_du_groupe_exist

    if not path_du_groupe_exist:
        try:
            os.mkdir("/home/" + groupe)
            path_du_groupe_exist = True
        except FileExistsError:
            path_du_groupe_exist = True
    else:
        path_du_groupe_exist = True


    return path_du_groupe_exist


def create_user():
    '''
    La fonction creer_user() permet de creer un utilisateur s'il n'existe pas
    dans /etc/passwd.
    '''
    # Le répertoire squelette (/etc/skel/) contient les fichiers et
    # répertoires qui seront copiés dans le répertoire
    # personnel de l’utilisateur au moment de sa création.

    global user
    global user_exist
    global password

    if not user_exist:
        try:
            os.system("useradd -d /home/" + groupe + "/" + user + " -g " + groupe + " -s /bin/bash " + " --password  $(mkpasswd -H md5 " + password + " ) " + user)
            os.system("passwd -e " + user)
            user_exist = True
        except FileExistsError:
            user_exist = True
    else:
        user_exist = True

    return user_exist
##########################################"

a = 1
while True:
    if groupe_exist:
        print("pass2", groupe, groupe_exist)
        pdb.set_trace()
        if path_du_groupe_exist:
            print("pass4", path_du_groupe_exist)
            pdb.set_trace()
            if user_exist:
                print("pass6", user_exist)
                pdb.set_trace()
                break
            else:
                create_user()
                print("pass5", user_exist)
                pdb.set_trace()
                continue
        else:
            creer_path_groupe()
            print("pass3", path_du_groupe_exist)
            pdb.set_trace()
            continue
    else:
        create_groupe()
        print("pass1", groupe_exist)
        pdb.set_trace()
        continue
    a += 1


