# Gestion des utilisateurs

## Besoin

Dans le cadre de la gestion utilisateurs, un administrateur peut recevoir quotidiennement un fichier CSV (export d'un tableur MS Excel par exemple) contenant la liste des utilisateurs qui doivent exister sur un serveur.

Ce fichier, appelé *personnages.csv*, pourrait alors avoir le contenu suivant :

| Prénom    | Nom         | Mot de passe | Lieu         |
| --------- | ----------- | ------------ | ------------ |
| Suzanne   | Sto Hélit   | bigadin      | Quirm        |
| Esméralda | Ciredutemps | gytha        | Lancre       |
| Havelock  | Vétérrini   | serviteur    | Ankh-Morpork |
| Mustrum   | Ridculle    | ciredutemps  | Université   |
| Planteur  | J.M.T.L.G.  | brioche      | -            |

Le mot de passe correspond au mot de passe original de l'utilisateur (celui-ci doit le modifier à sa première connexion), le lieu correspond à un secteur auquel l'utilisateur est rattaché; lorsque le lieu est remplacé par un tiret, l'utilisateur doit être supprimé et ses données archivées.

La tache quotidienne de cet administrateur est alors multiple:

- Il doit ajouter les utilisateurs de la liste qui ne sont pas sur le système.
- Il doit modifier le lieu auquel les utilisateurs sont rattachés s'ils sont déplacés.
- Il ne doit **pas** modifier le mot de passe des utilisateurs existants.
- Il doit supprimer les utilisateurs qui ne doivent plus exister.
- Il doit archiver les fichiers de ces utilisateurs.

Dans ce cadre:

- Les noms d'utilisateurs doivent avoir le format "nom_prenom", les accents doivent être supprimés et les majuscules doivent devenir des minuscules (de même pour les noms de groupes, liés aux lieux).

- Chaque utilisateur doit être associé à un groupe nommé selon le lieu auquel il est rattaché.

- Ses fichiers doivent être dans le répertoire 

  ```
  /home/<lieu>/<utilisateur>
  ```

- S'il n'existe pas déjà, le répertoire de l'utilisateur doit contenir une copie du contenu du répertoire */etc/skel* et son mot de passe doit être celui qui est donné dans le fichier (avec obligation de le changer à la prochaine connexion).

- Les archives doivent être placées dans 

  ```
  /archives/<utilisateur>-<date>.tar.gz
  ```

## Solution

Le script *user.py* que vous retrouverez dans mon dépôt [github](https://github.com/svcrobotics/Gestion-Utilisateurs/user.py) effectue automatiquement toutes ces opérations.
