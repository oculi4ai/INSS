import socket
from manage import main
import os
from django.core.management import execute_from_command_line
import webbrowser
from django.apps import AppConfig
import threading
import requests, configparser


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('settings.ini')
    hostname = socket.gethostname()
    print(config['INFO']['HOST_TYPE'])  

    if config['INFO']['HOST_TYPE'] == 'LAN':
        
        try:
            local_ip = socket.gethostbyname(hostname + ".local")
        except:
            local_ip = socket.gethostbyname(hostname)
 
    elif config['INFO']['HOST_TYPE'] == 'Device':
        local_ip = socket.gethostbyname(hostname)

    else:
        local_ip = socket.gethostbyname(hostname)
        

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INSServer.settings')

    

    def check_if_server_is_ready():

        while True:
            try:
                requests.get('http://'+local_ip+':8000')
                webbrowser.open('http://'+local_ip+':8000')
                break
            except:
                pass


    threading.Thread(target=check_if_server_is_ready).start()    
    
    execute_from_command_line(('','runserver',local_ip+':8000', '--insecure'))
