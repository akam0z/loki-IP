# loki-IP

Ce guide décrit l'utilisation et l'installation des dépendances nécessaires pour un script Python conçu pour vérifier la présence de services SSH et Telnet sur des adresses IP publiques générées aléatoirement. Ce script teste également la vulnérabilité de ces services en tentant des connexions avec des identifiants communs. Il est particulièrement utile pour des simulations ou des tests de pénétration dans un environnement contrôlé.

Fonctionnalités du Script
Génération d'adresses IP publiques aléatoires : Le script génère des adresses IP qui ne font pas partie des plages d'adresses réservées.
Vérification des services : Il vérifie la présence de services SSH (port 22) et Telnet (port 23) sur les adresses IP générées.
Test de vulnérabilité : Pour les services détectés, le script tente des connexions avec des paires d'identifiants prédéfinies pour évaluer la vulnérabilité.
Enregistrement dans une base de données MySQL : Les adresses IP avec des services détectés et vulnérables sont enregistrées dans une base de données MySQL avec des détails tels que le type de service et la région (à configurer).
Installation des Dépendances
Le script nécessite Python 3 et l'installation de plusieurs dépendances externes, dont MySQL Connector pour Python, Paramiko pour les connexions SSH, et éventuellement un serveur MySQL pour stocker les résultats. Voici comment vous pouvez installer ces dépendances :

Installation de Python 3 : Assurez-vous que Python 3 est installé sur votre système. Vous pouvez le télécharger depuis le site officiel python.org.

Installation de MySQL Connector : Utilisez pip, le gestionnaire de paquets Python, pour installer MySQL Connector. Ouvrez un terminal ou une invite de commande et exécutez :

Copy code
pip install mysql-connector-python
Installation de Paramiko : De la même manière, installez Paramiko pour gérer les connexions SSH :

Copy code
pip install paramiko
Configuration de MySQL (facultatif) : Si vous n'avez pas encore de serveur MySQL, installez MySQL sur votre système. Consultez la documentation officielle de MySQL pour les instructions spécifiques à votre système d'exploitation. Créez une base de données et un utilisateur pour le script, puis ajustez les paramètres de connexion dans le script (host, user, password, database) en conséquence.

Utilisation du Script
Configurer le Script : Avant de lancer le script, assurez-vous de configurer les paramètres de connexion MySQL dans la fonction main() pour correspondre à votre environnement de base de données.

Lancer le Script : Exécutez le script depuis un terminal ou une invite de commande avec la commande :

Copy code
python nom_du_script.py
Interprétation des Résultats : Le script affiche les résultats de la vérification dans le terminal et enregistre les adresses IP vulnérables dans la base de données MySQL configurée. Les résultats incluent l'adresse IP, le type de service (SSH ou Telnet), et si le service est considéré comme vulnérable basé sur les tests d'identifiants prédéfinis.

Sécurité et Avertissement
L'utilisation de ce script doit être effectuée de manière responsable et uniquement dans des environnements où vous avez l'autorisation explicite de réaliser de tels tests. L'analyse de réseaux et de services sans autorisation peut être illégale et éthiquement répréhensible.

Pour toute question ou assistance supplémentaire, n'hésitez pas à ouvrir une issue dans le dépôt GitHub du projet

# nous recruton 
nous somme la recherche d'aide pour developer se logiciel
# email : akam0z@pronton.me
