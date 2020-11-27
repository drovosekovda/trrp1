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
    pas1=password[0:16]
    pas2=password[16:32]
    pas3=password[32:40]
    if len(pas3)<16:
        for i in range(0,16-len(pas3)):
            pas3+=" "
    tag1 = cipher.encrypt(username)
    tag21 = cipher.encrypt(pas1)
    tag22 = cipher.encrypt(pas2)
    tag23 = cipher.encrypt(pas3)
    file_name="log_pas"
    with open(file_name, 'ab') as byte_file:
        byte_file.write(tag1)
        byte_file.write(tag21+tag22+tag23)
username=""
password=""
b=0
file_name="log_pas"
try:
    with open(file_name, 'rb') as byte_file:
        username1=input("Введите имя пользователя: ")
        tag=byte_file.readline()
        while (tag != None and password==""):
            print("Загрузили из файла "+file_name+" данные:" +str(tag))
            tag1 = cipher.decrypt(tag)
            username2=tag1.decode()
            username=username2.split()[0]
            if (username==username1):
                password=username2.split()[1]
                print("Авторизация под логином: "+username)
            else:
                tag=byte_file.readline()
except:
    print("")
if (str(password)==""):
    print("Воспользуйтесь для получения токена"+" "+"https://github.com/settings/tokens")
    print("Введите Логин")
    username=input()
    print("Введите токен")
    password=getpass.getpass()
    b=1
    


#print(username)
try:
    g = Github(password)
    if b==1:   
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
                print("Введите текст:")
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