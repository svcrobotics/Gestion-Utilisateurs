# Gestion Utilisateurs

## Besoin

Dans le cadre de la gestion utilisateurs, un administrateur peut recevoir quotidiennement un fichier .csv contenant la liste des utilisateurs qui doivent exister sur un serveur.

Ce fichier, appelé *data.csv*, pourrait alors avoir le contenu suivant :

| Prénom    | Nom         | Mot de passe | Goupe        |
| --------- | ----------- | ------------ | ------------ |
| Suzanne   | Sto Hélit   | bigadin      | Comptabilité |
| Esméralda | Ciredutemps | gytha        | Formation    |
| Havelock  | Vétérrini   | serviteur    | System       |
| Mustrum   | Ridculle    | ciredutemps  | Direction    |
| Planteur  | J.M.T.L.G.  | brioche      | -            |

Le mot de passe correspond au mot de passe original de l'utilisateur (celui-ci doit le modifier à sa première connexion), le groupe correspond à un secteur auquel l'utilisateur est rattaché; lorsque le groupe est remplacé par un tiret, l'utilisateur doit être supprimé et ses données archivées.

La tache quotidienne de cet administrateur est alors multiple:

- Il doit ajouter les utilisateurs de la liste qui ne sont pas sur le système.
- Il doit modifier le groupe auquel les utilisateurs sont rattachés s'ils sont déplacés.
- Il ne doit **pas** modifier le mot de passe des utilisateurs existants.
- Il doit supprimer les utilisateurs qui ne doivent plus exister.
- Il doit archiver les fichiers de ces utilisateurs.

Dans ce cadre:

- Les noms d'utilisateurs doivent avoir le format "nom_prenom", les accents doivent être supprimés et les majuscules doivent devenir des minuscules de même pour les noms de groupes.

- Chaque utilisateur doit être associé à un groupe.

- Les fichiers de l'utilisateurs doivent être dans le répertoire

  ```
  /home/<groupe>/<utilisateur>
  ```

- S'il n'existe pas déjà, le répertoire de l'utilisateur doit contenir une copie du contenu du répertoire */etc/skel* et son mot de passe doit être celui qui est donné dans le fichier (avec obligation de le changer à la prochaine connexion).

- Les archives doivent être placées dans 

  ```
  /archives/<utilisateur>-<date>.tar.gz
  ```

## Solution

Le script *user.py* que vous retrouverez dans mon dépôt [github](https://github.com/svcrobotics/Gestion-Utilisateurs/blob/master/user.py) effectue automatiquement toutes ces opérations.
