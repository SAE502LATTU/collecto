from scapy.layers.inet import Ether
from scapy.layers.l2 import ARP, srp
# import argparse
import socket
import time
import napalm
import paramiko

#info kali 
# Dictionnaire d'informations de connexion
machine_info = {
    'ip': '192.168.253.135',
    'utilisateur': 'user',
    'mdp': 'bonjour'
}
def afficher_logs_services():
    
    logs = []
    # instance SSHClient de Paramiko
    client_ssh = paramiko.SSHClient()

    client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # connextion à la kali (pas oublié le service ssh start)
        client_ssh.connect(
            machine_info['ip'],
            username=machine_info['utilisateur'],
            password=machine_info['mdp']
        )

        # log /var/log
        commandes = [
            'tail -n 50 /var/log/apache2/access.log',  # apache
            'tail -n 50 /var/log/auth.log',           # ssh
            'dmesg | tail -n 50'                      # boot
        ]

        
        services = ["apache2", "ssh", "boot"] # var services correspondant aux commandes dans la liste commandes
        for i, commande in enumerate(commandes):
            _, sortie, _ = client_ssh.exec_command(commande) # stdin, stdout et stderr
            logs_data = { ##
                'service': services[i], # 
                'logs': sortie.read().decode()
            }
            logs.append(logs_data)

    except Exception as e:
        print(f"SSH activé{e}")

    finally:

        client_ssh.close()

    return logs

def afficher_processus_ssh():

    client_ssh = paramiko.SSHClient()

 
    client_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    process_info = []  # Liste qui stockera toutes les infos qui seront énumérées dans le tableau HTML

    try:
        # Connexion au serveur SSH
        client_ssh.connect(
            machine_info['ip'],
            username=machine_info['utilisateur'],
            password=machine_info['mdp']
        )


        commande = 'ps aux'

        
        _, sortie, _ = client_ssh.exec_command(commande)

        # itère sur chaque paire (index, commande)
        for ligne in sortie.read().decode().splitlines()[1:]:  # Ignorer la première ligne (entêtes de la commande)
            # 
            colonnes = ligne.split()
            user = colonnes[0]
            pid = colonnes[1]
            #cpu_percentage = colonnes[2] ?
            process_name = colonnes[10]  

            # Ajouter les informations du processus à la liste
            process_info.append({
                'user': user,
                'pid': pid,
                'process_name': process_name,  # Ajoutez la clé pour le nom du processus
                # Ajoutez d'autres clés selon vos besoins
            })

    except Exception as e:
        print(f"Erreur de connexion SSH : {e}")

    finally:
        # Fermeture de la connexion SSH
        client_ssh.close()

    return process_info



def getInfo(self, ip, port):
        driver = napalm.get_network_driver('ios')
        device = driver(hostname=ip, username='user', password='',
                        optional_args={'port': port, 'transport': "ssh"})
        device.open()
        print(device.get_interfaces_ip())
        device.close()

def get_port():
    #startTime = time.time()
    ports_info = []  # Liste pour stocker les informations sur chaque port

    for i in range(79, 82):  # Vérifier les ports de 1 à 1024
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn = s.connect_ex((machine_info['ip'], i))
        port_status = "OPEN" if conn == 0 else "CLOSED"
        
        # Nom associé au port (ajustez en fonction de vos besoins)
        port_name = "HTTP" if i == 80 else "SSH" if i == 22 else "Autre"

        ports_info.append({
            'port_number': i,
            'port_name': port_name,
            'status': port_status
        })

        if conn == 0:
            # Vous pouvez appeler getInfo(ip, i) ici si nécessaire
            print(f'Port {i} ({port_name}): {port_status}')

        s.close()  # Fermer la connexion

    #print("Time taken:", time.time() - startTime)
    #print(ports_info)
    return ports_info

#port()
#afficher_logs_services(info_connexion_kali)
#afficher_processus_ssh(info_connexion_kali)
