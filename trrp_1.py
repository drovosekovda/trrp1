import getpass
import binascii
from Crypto.Cipher import AES
from github import Github
import base64
key = binascii.unhexlify('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
cipher = AES.new(key)
def encrypt_(username,password):
    if len(username)<16:
        for i in range(0,16-len(username)):
            username+=" "
    if len(password)<16:
        for i in range(0,16-len(password)):
            password+=" "
    tag1 = cipher.encrypt(username)
    tag2 = cipher.encrypt(password)
    file_name="log_pas"
    with open(file_name, 'wb') as byte_file:
        byte_file.write(tag1)
        byte_file.write(tag2)
username=""
password=""
file_name="log_pas"
try:
    with open(file_name, 'rb') as byte_file:
        tag=byte_file.readline()
        tag1 = cipher.decrypt(tag)
        username=tag1.decode()
        password=username.split()[1]
        username=username.split()[0]
        print("Авторизация под логином: "+username)
except:
    print("")
if (str(username)==""):
    print("Введите Логин")
    username=input()
    print("Введите пароль")
    password=getpass.getpass()
    


#print(username)
try:
    g = Github(username, password)
    encrypt_(username,password)
    repo = g.get_repo("drovosekovda/test")#Получить репозиторий
    print("insert [название файла] - создать файл")
    print("select [название файла] - показать файл")
    print("update [название файла] - обновить файл")
    print("delete [название файла] - удалить файл")
    print("show - показать содержимое каталога")
    print("exit - выход")
    command=input()
    while command!="exit":
        try:
            if (command.split()[0]=="insert"):
                print("Введите текс:")
                text=input()
                repo.create_file(command.split()[1], "",text)#Создать файл
            if (command=="show"):
                #Получить файлы в репозитории
                repo = g.get_repo("drovosekovda/test")#Получить репозиторий
                contents = repo.get_contents("")
                for content_file in contents:
                    print("->",content_file.path)
            if (command.split()[0]=="update"):
                contents = repo.get_contents(command.split()[1])#Получить файл по названию
                file_bytes = base64.b64decode(contents.content)
                file_str = file_bytes.decode('utf-8')
                print("Содержимое файла:")
                print(file_str)
                print("Введите новое содержимое:")
                text=input()
                repo.update_file(contents.path, "", text, contents.sha)#Изменить
            if (command.split()[0]=="delete"):
                contents = repo.get_contents(command.split()[1])#Получить файл по названию
                repo.delete_file(contents.path, "", contents.sha)#Удалить файл
            if (command.split()[0]=="select"):
                contents = repo.get_contents(command.split()[1])#Получить файл по названию
                file_bytes = base64.b64decode(contents.content)
                file_str = file_bytes.decode('utf-8')
                print("Содержимое файла:")
                print(file_str)
        except:
            print("Error")
        command=input()
except:
    print("Ошибка авторизации")