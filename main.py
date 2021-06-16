import json
import os


defaultPassword = "password"


def ASCII(string: str) -> list[int]:
    arr = []
    for i in string:
        arr.append(ord(i))
    # .extend(ord(num) for num in string)
    return arr


def encrypt(passwd: str) -> list[int]:
    encrypt = ASCII(passwd)
    key = ASCII(defaultPassword)
    for i in range(len(encrypt)):
        encrypt[i] += key[i % len(key)]
    encryptStr = ''.join([chr(value)for value in encrypt])
    return encryptStr


def decrypt(passwd: str) -> str:
    decrypt = ASCII(passwd)
    key = ASCII(defaultPassword)
    for i in range(len(decrypt)):
        decrypt[i] -= key[i % len(key)]
    decryptStr = ''.join([chr(value)for value in decrypt])
    return decryptStr


def read():
    if os.path.exists('./passwords.json'):
        data = json.load(open('passwords.json'))
        for i in data:
            print(decrypt(data[i]))
    else:
        print("no current passwords found")


def add():
    dic = {
    }
    if not os.path.exists('./passwords.json'):
        with open('passwords.json', 'a') as outfile:
            json_object = json.dumps({})
            outfile.write(json_object)
            print("Created")
    username = str(input("Enter your username : "))
    password = str(input("Enter your password : "))
    password = encrypt(password)
    dic[username] = password

    with open('passwords.json', 'r+') as outfile:
        # outfile.write(json_object)
        file_data = json.load(outfile)
        # pos = len(file_data)
        outfile.seek(0)
        file_data.update(dic)
        json.dump(file_data, outfile, indent=4)


run = True

while run:

    mode = input("select the mode a for add r for read q for quit : ")

    if mode == 'r':
        read()
    if mode == 'a':
        add()
    if mode == 'q':
        run = False
