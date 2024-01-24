import paramiko

def get_server_stats():
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    server_ip = '192.168.56.101'
    username = 'theodcnccao'
    password = 'bonjour'

    try:
        ssh_client.connect(server_ip, username=username, password=password, timeout=10)

        cpu_usage_command = 'top -bn1 | grep "Cpu(s)"'
        disk_usage_command = 'df -h'
        memory_usage_command = 'free -m'

        stdin, stdout, stderr = ssh_client.exec_command(cpu_usage_command)
        cpu_result = stdout.read().decode().strip() 
        
        stdin, stdout, stderr = ssh_client.exec_command(disk_usage_command)
        disk_result = stdout.read().decode().strip()
        
        stdin, stdout, stderr = ssh_client.exec_command(memory_usage_command)
        memory_result = stdout.read().decode().strip()
        
    except Exception as e:
        print(f"Erreur lors de la connexion ou de l'exécution des commandes : {e}")
        return None
    finally:
        ssh_client.close()

    return {
        'cpu_usage': cpu_result,
        'disk_usage': disk_result,
        'memory_usage': memory_result
    }
