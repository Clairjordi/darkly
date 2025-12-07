# Hidden Directory

![alt text](hidden_directory.png)

## Description

La faille Hidden Directory apparaît lorsqu’un serveur web expose un répertoire sensible accessible publiquement.
Même si ce répertoire est mentionné dans le fichier robots.txt, celui-ci ne constitue pas un mécanisme de sécurité, mais seulement une recommandation pour les moteurs de recherche.
Cette vulnérabilité permet à un attaquant d’accéder à des dossiers censés être cachés, de lister leur contenu et de récupérer des informations sensibles.

## Comment reproduire la faille

1. Aller sur le fichier robots.txt du site `/robots.txt`

2. Observer les chemins interdits listés, par exemple :
     ```
    Disallow: /whatever
    Disallow: /.hidden
     ```

3. Accéder directement au répertoire sensible depuis le navigateur `/.hidden/`

- Si le contenu du dossier est listé automatiquement, la faille est confirmée.

4. Télécharger le contenu complet du dossier via un outil en ligne de commande :
     ```
    wget --recursive --no-parent --execute robots=off http://<IP_ADDRESS>/.hidden/
     ```

5. Utiliser un script de recherche 
Rechercher le flag dans les fichiers récupérés :
     ```
    bash ./finder.sh | grep flag
     ```

- Le flag est retourné :
     ```
    Hey, here is your flag : d5eec3ec36cf80dce44a896f961c1831a05526ec215693c8f2c39543497d4466
     ```

## Recommandations pour empêcher la faille

* Ne jamais exposer de chemins sensibles dans robots.txt

* Désactiver le listing de répertoire :
    * Désactiver l’option d’indexation des fichiers sur le serveur web.

* Déplacer les fichiers sensibles hors du répertoire web :
    * Les fichiers comme htpasswd ne doivent jamais être accessibles publiquement.

* Utiliser des méthodes de hashage sécurisées :
    * Remplacer MD5 par des algorithmes robustes comme bcrypt ou Argon2.

* Restreindre les permissions des fichiers :
    * Limiter les droits de lecture aux seuls services nécessaires.

## Conclusion

Cette faille d’exposition de répertoire caché permet à un attaquant d’obtenir des informations sensibles simplement en consultant des dossiers accessibles publiquement.
Le fichier robots.txt ne protège pas les ressources : il indique seulement leur existence.
En désactivant l’indexation des dossiers et en appliquant de vrais contrôles d’accès, il est possible de se protéger efficacement contre ce type de vulnérabilité.