import json
from cryptography.fernet import Fernet
from server_connection import ServerConnection

class Encoder():
    '''Класс который шифрует рекорд и отправляет его в json файл
    или разшифровывает и выводит обратно для сравнения'''
    
    '''# Передаёт рекорд и ключ если нужно в конструктор
    def __init__(self, record, key = b''):
        #Строка для шифрования
        self.record = record
        #Ключ для шифрования
        self.key = key'''

    def seve_record(self, record):
        '''Метод шифрования рекорда и сохранения в файл'''
        #Строка для шифрования
        self.record = record
        #Создаём обьект сланна соединение с сервером
        self.server_connect = ServerConnection()
        #Проверка есть ли соединение с сервером
        self.connect = self.server_connect.get_connect()
        #Если есть то
        if self.connect:
            #Генерируем новый ключ для шифрования
            self.key = Fernet.generate_key()
            #Создаём функцию шифрвоания на основе ключа
            self.cipher = Fernet(self.key)
            #Переводим строку рекорда в байты
            self.record = bytes(str(self.record), encoding = 'utf-8')
            #Создание зашифрованной копии рекорда
            self.record = self.cipher.encrypt(self.record)
            #Перевод рекорда из байтовых в строковые значения для записи
            self.record = str(self.record.decode('utf-8'))
            #Перевод ключа из байтовых в строковые значения для записи
            self.key = str(self.key.decode('utf-8'))
            #Отправляем запрос на сервес, сохранение
            self.server_connect.set_save_server(self.key, self.record)
            #Имя файла для записи, если нет создаётсяавтматически
            self.filename = 'record/record.json'
            #Всё это кладём в массив
            self.save_arr = [self.key, self.record]
            #Функция записи в файл
            with open(self.filename, 'w') as self.f_obj:
                json.dump(self.save_arr , self.f_obj)

        else:
            #Переводим строку рекорда в байты
            self.record = bytes(str(self.record), encoding = 'utf-8')
            #Генерируем новый ключ для шифрования
            self.key = Fernet.generate_key()
            #Создаём функцию шифрвоания на основе ключа
            self.cipher = Fernet(self.key)
            #Создание зашифрованной копии рекорда
            self.record = self.cipher.encrypt(self.record)
            #Имя файла для записи, если нет создаётсяавтматически
            self.filename = 'record/record.json'
            #Перевод рекорда из байтовых в строковые значения для записи
            self.record = str(self.record.decode('utf-8'))
            #Перевод ключа из байтовых в строковые значения для записи
            self.key = str(self.key.decode('utf-8'))
            #Всё это кладём в массив
            self.save_arr = [self.key, self.record]
            #Функция записи в файл
            with open(self.filename, 'w') as self.f_obj:
                json.dump(self.save_arr , self.f_obj)

    def load_record(self):
        '''Метод расшифровки рекорда и загрузка его из файла'''
        #Создаём обьект сланна соединение с сервером
        self.server_connect = ServerConnection()
        #Проверка есть ли соединение с сервером
        self.connect = self.server_connect.get_connect()
        #Если есть то
        if self.connect:
            #Получаем рекорд с сервера
            self.server_record = self.server_connect.get_save_server()
            #Избавляемся от ненужных символов
            self.server_record = self.server_record.replace('"', "")
            self.server_record = self.server_record.replace('[', '')
            self.server_record = self.server_record.replace(']', '')
            self.server_record = self.server_record.replace(' ', '')
            #Нарезаем в кортеж
            self.server_record_split = self.server_record.split(',')
            #Перевод значений из считенного массива в байты
            self.key_serv = bytes(self.server_record_split[0], encoding = 'utf-8')
            self.record_serv = bytes(self.server_record_split[1], encoding = 'utf-8')
            #Создание нового шифровальщика на основе старого считанного ключа
            self.cipher_serv = Fernet(self.key_serv)
            #Расшифровка сообщения создание расшифрованной копии
            self.record_serv = self.cipher_serv.decrypt(self.record_serv)
            self.record_serv = self.record_serv.decode('utf-8')
            self.record_serv = int(self.record_serv)

            #Имя файла для загрузки, если нет создаётсяавтматически
            self.filename = 'record/record.json'
            #Функция чтения из файла
            with open(self.filename) as self.f_obj:
                self.load_arr = json.load(self.f_obj)
            #Перевод значений из считенного массива в байты
            self.key = bytes(self.load_arr[0], encoding = 'utf-8')
            self.record = bytes(self.load_arr[1], encoding = 'utf-8')
            #Создание нового шифровальщика на основе старого считанного ключа
            self.cipher = Fernet(self.key)
            #Расшифровка сообщения создание расшифрованной копии
            self.record = self.cipher.decrypt(self.record)
            self.record = self.record.decode('utf-8')
            self.record = int(self.record)

            if self.record <= self.record_serv:
                return self.record_serv
            else:
                return self.record
        else:
            #Имя файла для загрузки, если нет создаётсяавтматически
            self.filename = 'record/record.json'
            #Функция чтения из файла
            with open(self.filename) as self.f_obj:
                self.load_arr = json.load(self.f_obj) 
            #Перевод значений из считенного массива в байты
            self.key = bytes(self.load_arr[0], encoding = 'utf-8')
            self.record = bytes(self.load_arr[1], encoding = 'utf-8')
            #Создание нового шифровальщика на основе старого считанного ключа
            self.cipher = Fernet(self.key)
            #Расшифровка сообщения создание расшифрованной копии
            self.record = self.cipher.decrypt(self.record)
            self.record = self.record.decode('utf-8')
            self.record = int(self.record)
            return self.record

'''Тестирование класса'''
'''string_to_encrypt = int(input('Введите строку для шифрования: '))
enkoder = Encoder()
enkoder.seve_record(string_to_encrypt)
string_to_decrypt = enkoder.load_record()
print(string_to_decrypt)'''
