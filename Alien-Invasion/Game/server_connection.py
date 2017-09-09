# -*- coding: utf-8 -*-
import socket
import urllib.request
from settings import Settings

class ServerConnection():
    
    def __init__(self):
        #Задаём настрйоки игры
        self.settings = Settings()
    
    def set_save_server(self, key, record):
        record = str(record)
        data = ('record_save=["'+key+'","'+record+'"]').encode("utf-8")
        # отправим методо POST параметр
        response = urllib.request.urlopen(self.settings.get_set_irl,data)
        # utf-8 чтобы принять русские буквы
        html = response.read().decode("utf-8")
        #return html

    def get_save_server(self):
        data = "load_save=load".encode("utf-8")
        # отправим методо POST параметр 
        response = urllib.request.urlopen(self.settings.get_set_irl,data)
        # utf-8 чтобы принять русские буквы
        html = response.read().decode("utf-8")
        return html

    def get_connect(self):
        #Проверка соединения с сервером
        try:
            socket.gethostbyname(self.settings.connect_url)
        except socket.gaierror:
            return False
        return True
     
'''server_connect = ServerConnection()
connect = server_connect.get_connect()
if connect:
    key = input('Введите ключ: ')
    record = input('Введите значение: ')
    ansver = server_connect.set_save_server(key,record)
    print(ansver)
    ansver = server_connect.get_save_server()
    print('Ответ с сервера: ',ansver)
else:
    print('Нет соединения с сервером\n')'''
