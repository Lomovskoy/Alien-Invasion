# -*- coding: utf-8 -*-
import socket
import urllib.request

class ServerConnection():

    def set_save_server(self, key, record):
        record = str(record)
        data = ('record_save=["'+key+'","'+record+'"]').encode("utf-8") # отправим методо POST параметр z, равный 555
        response = urllib.request.urlopen("http://opgames.h1n.ru/record/controller.php",data)
        html = response.read().decode("utf-8") # utf-8 чтобы принять русские буквы
        #return html

    def get_save_server(self):
        data = "load_save=load".encode("utf-8") # отправим методо POST параметр z, равный 555
        response = urllib.request.urlopen("http://opgames.h1n.ru/record/controller.php",data)
        html = response.read().decode("utf-8") # utf-8 чтобы принять русские буквы
        return html

    def get_connect(self):

        try:
            socket.gethostbyname('www.opgames.h1n.ru')
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

