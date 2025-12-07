# Sensitive data robots.txt

![alt text](sensitive_datat_robots.txt.png)

## Description

La faille Sensitive Data Exposure via robots.txt se produit lorsqu’un fichier robots.txt révèle des chemins sensibles du site web.
Ce fichier est destiné aux moteurs de recherche pour indiquer quelles parties du site ne pas indexer, mais il est publiquement accessible, ce qui permet à un attaquant de découvrir des répertoires cachés ou sensibles.
Lorsque ces répertoires sont accessibles sans protection, ils peuvent contenir des fichiers critiques (comme des fichiers d’authentification), entraînant une fuite d’informations et un contournement de l’authentification.

## Comment reproduire la faille

1. Aller sur le fichier robots.txt du site `/robots.txt`

2. Observer les chemins interdits listés, par exemple :
     ```
    Disallow: /whatever
    Disallow: /.hidden
     ```

3. Accéder directement au répertoire sensible depuis le navigateur `/whatever/`

- Si la liste des fichiers apparaît, la faille est confirmée.

4. Télécharger le fichier sensible exposé :
     ```
    htpasswd
     ```

5. Récupérer les identifiants exposés :
    ```
    root:437394baff5aa33daa618be47b75cb49
    ```

6. Décrypter le hash MD5 avec un outil en ligne type CrackStation :
     ```
    Résultat : qwerty123@
     ```

7. Accéder à la page d’administration `/admin`


8. Se connecter avec les identifiants compromis :
     ```
    Username : root
    Password : qwerty123@
    ```

- Si l’accès est autorisé, la faille est confirmée.

## Recommandations pour empêcher la faille

* Ne jamais exposer de chemins sensibles dans robots.txt

* Désactiver le listing de répertoire :
    * Désactiver l’option d’indexation des fichiers sur le serveur web.

* Déplacer les fichiers sensibles hors du répertoire web :
    * Les fichiers comme htpasswd ne doivent jamais être accessibles publiquement.

* Utiliser des méthodes de hashage sécurisées :
    * Remplacer MD5 par des algorithmes robustes comme bcrypt ou Argon2.

* Restreindre l’accès aux pages sensibles :
    * Protéger /admin par authentification forte et/ou filtrage IP.

* Utiliser un WAF :
    * Peut bloquer l’accès aux fichiers sensibles et détecter les comportements anormaux.

## Conclusion

Cette faille liée au fichier robots.txt est particulièrement dangereuse car elle révèle involontairement des répertoires et fichiers sensibles.
Elle facilite le travail d’un attaquant en lui indiquant où chercher des informations critiques, menant à une fuite de données et à un contournement de l’authentification.
En désactivant l’indexation des répertoires, en évitant l’exposition des chemins sensibles et en protégeant correctement les fichiers d’authentification, il est possible de se prémunir efficacement contre ce type de vulnérabilité.