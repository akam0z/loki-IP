# loki-IP

## Description

loki-IP est un outil pour scanner des adresses IP à la recherche de services réseau ouverts. Il vérifie la présence de divers services courants (comme SSH, HTTP, FTP) et peut également détecter des services personnalisés ajoutés par l'utilisateur.

## Fonctionnalités

- **Scan de Services Standards** : SSH, Telnet, HTTP, HTTPS, FTP, SMTP, POP3, IMAP.
- **Services Personnalisés** : Permet l'ajout de services personnalisés avec un port, un nom et une commande pour obtenir la version.
- **Vérification des Versions** : Peut vérifier les versions des services lorsque cela est possible.
- **Parallélisme** : Utilise des threads pour exécuter plusieurs scans en parallèle.
- **Configuration Flexible** : Permet de définir le nombre d'IP à scanner, les services à rechercher, le délai entre les tentatives, et le nombre de threads.
- **Interface Graphique** : Fournit une interface graphique pour une configuration facile via Tkinter.

## Installation

Assurez-vous d'avoir Python installé. Vous pouvez installer les dépendances nécessaires avec pip :

```bash
pip install paramiko
