import socket
import random
import paramiko
import threading
import time
import tkinter as tk
from tkinter import messagebox, simpledialog

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

# Fonction pour vérifier un service
def check_service(ip, port, timeout=1):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

# Fonction pour obtenir la version d'un service
def get_service_version(ip, port, banner_request):
    try:
        with socket.create_connection((ip, port), timeout=1) as conn:
            conn.sendall(banner_request.encode())
            response = conn.recv(1024).decode()
            return response.split('\n')[0]
    except:
        return None

# Fonction pour vérifier les services avec versions et informations
def check_services(ip, selected_services, version_check):
    services = {service: 'non' for service in selected_services}

    if 'ssh' in selected_services:
        if check_service(ip, 22):
            services['ssh'] = 'oui'
            if version_check:
                version = get_service_version(ip, 22, "SSH -V")
                if version:
                    services['ssh'] += f" (Version: {version})"

    if 'telnet' in selected_services:
        if check_service(ip, 23):
            services['telnet'] = 'oui'
            if version_check:
                version = get_service_version(ip, 23, "TELNET")
                if version:
                    services['telnet'] += f" (Version: {version})"

    if 'http' in selected_services:
        if check_service(ip, 80):
            services['http'] = 'oui'
            if version_check:
                version = get_service_version(ip, 80, "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(ip))
                if version:
                    services['http'] += f" (Version: {version})"

    if 'https' in selected_services:
        if check_service(ip, 443):
            services['https'] = 'oui'
            if version_check:
                version = get_service_version(ip, 443, "HEAD / HTTP/1.1\r\nHost: {}\r\n\r\n".format(ip))
                if version:
                    services['https'] += f" (Version: {version})"

    if 'ftp' in selected_services:
        if check_service(ip, 21):
            services['ftp'] = 'oui'
            if version_check:
                version = get_service_version(ip, 21, "USER anonymous\r\n")
                if version:
                    services['ftp'] += f" (Version: {version})"

    if 'smtp' in selected_services:
        if check_service(ip, 25):
            services['smtp'] = 'oui'
            if version_check:
                version = get_service_version(ip, 25, "HELO example.com\r\n")
                if version:
                    services['smtp'] += f" (Version: {version})"

    if 'pop3' in selected_services:
        if check_service(ip, 110):
            services['pop3'] = 'oui'
            if version_check:
                version = get_service_version(ip, 110, "USER anonymous\r\n")
                if version:
                    services['pop3'] += f" (Version: {version})"

    if 'imap' in selected_services:
        if check_service(ip, 143):
            services['imap'] = 'oui'
            if version_check:
                version = get_service_version(ip, 143, "A0001 LOGIN anonymous password\r\n")
                if version:
                    services['imap'] += f" (Version: {version})"

    return services

# Fonction pour enregistrer les résultats dans un fichier
def save_results(filename, results):
    with open(filename, "w") as f:
        for result in results:
            f.write(result + "\n")

# Fonction principale de scan
def scan_ips(num_ips, selected_services, filename, pause_time, version_check, parallelism):
    results = []

    def worker():
        for _ in range(num_ips // parallelism):
            ip = generate_public_ip()
            services = check_services(ip, selected_services, version_check)
            if any(services[service] == 'oui' for service in selected_services):
                service_results = ", ".join(f"{service}: {status}" for service, status in services.items())
                result = f"IP: {ip} - {service_results}"
                results.append(result)
                print(result)
            time.sleep(pause_time)

    threads = []
    for _ in range(parallelism):
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    save_results(filename, results)
    print(f"Scan terminé. Les résultats sont enregistrés dans le fichier {filename}.")

# Fonction d'interface utilisateur
def run_gui():
    def start_scan():
        num_ips = int(num_ips_entry.get())
        selected_services = services_entry.get().split(',')
        selected_services = [service.strip().lower() for service in selected_services]
        filename = filename_entry.get()
        pause_time = float(pause_entry.get())
        version_check = version_check_var.get()
        parallelism = int(parallelism_entry.get())
        
        threading.Thread(target=scan_ips, args=(num_ips, selected_services, filename, pause_time, version_check, parallelism)).start()
        messagebox.showinfo("Info", "Scan démarré. Veuillez vérifier la console pour les résultats.")

    root = tk.Tk()
    root.title("Scanner IP")

    tk.Label(root, text="Nombre d'IP à scanner :").grid(row=0, column=0)
    num_ips_entry = tk.Entry(root)
    num_ips_entry.grid(row=0, column=1)
    num_ips_entry.insert(0, "100")

    tk.Label(root, text="Services à rechercher (séparés par des virgules) :").grid(row=1, column=0)
    services_entry = tk.Entry(root)
    services_entry.grid(row=1, column=1)
    services_entry.insert(0, "ssh,telnet,http,https,ftp,smtp,pop3,imap")

    tk.Label(root, text="Nom du fichier pour les résultats :").grid(row=2, column=0)
    filename_entry = tk.Entry(root)
    filename_entry.grid(row=2, column=1)
    filename_entry.insert(0, "resultats_ips.txt")

    tk.Label(root, text="Pause entre les tentatives (en secondes) :").grid(row=3, column=0)
    pause_entry = tk.Entry(root)
    pause_entry.grid(row=3, column=1)
    pause_entry.insert(0, "0")

    tk.Label(root, text="Nombre de threads (parallélisme) :").grid(row=4, column=0)
    parallelism_entry = tk.Entry(root)
    parallelism_entry.grid(row=4, column=1)
    parallelism_entry.insert(0, "1")

    version_check_var = tk.BooleanVar()
    tk.Checkbutton(root, text="Vérifier les versions des services", variable=version_check_var).grid(row=5, column=0, columnspan=2)

    tk.Button(root, text="Démarrer le scan", command=start_scan).grid(row=6, column=0, columnspan=2)

    root.mainloop()

run_gui()  # Exécuter l'interface graphique

