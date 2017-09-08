import urllib.request

class ServerConnection():

    def set_save_server(self, record):
        record = str(record)
        data = ("record_save="+record).encode("utf-8") # отправим методо POST параметр z, равный 555
        response = urllib.request.urlopen("http://opgames.h1n.ru/record/controller.php",data)
        html = response.read().decode("utf-8") # utf-8 чтобы принять русские буквы
        return html

    def get_save_server(self):
        data = "load_save=load".encode("utf-8") # отправим методо POST параметр z, равный 555
        response = urllib.request.urlopen("http://opgames.h1n.ru/record/controller.php",data)
        html = response.read().decode("utf-8") # utf-8 чтобы принять русские буквы
        return html


'''server_connect = ServerConnection()
record = input('Введите значение: ')
ansver = server_connect.set_save_server(record)
print(ansver)
ansver = server_connect.get_save_server()
print('Ответ с сервера: ',ansver)'''
