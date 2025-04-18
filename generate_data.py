import sqlite3
import hashlib
from faker import Faker

fake = Faker("sk_SK")

#This script generates dummy data
subor = open("adverts_sample.txt")
obsah = subor.read().split("\n")
subor.close

# usernames = ['user16', 'user4', 'user8', 'user14', 'user17', 'user9', 'user3', 'user10', 'user18', 'user12', 'user2', 'user13', 'user7', 'user6', 'user20', 'user11', 'user19', 'user5', 'user15']
usernames = []

def title_hash(title):
    return hashlib.md5(title.encode()).hexdigest()

def create_advert_file(title,text):
    nazov = title_hash(title)
    with open("Adverts/"+nazov+".dat","wb") as subor:
        byte_text = text.encode()
        subor.write(byte_text)

with sqlite3.connect('database.db') as connection:
    cursor = connection.cursor()

    # cursor.execute("DELETE FROM Adverts")
    # connection.commit()

    for riadok in obsah:
        try:
            riadok = riadok.split(";")

            # Insert a record into the Adverts table
            insert_query = '''
            INSERT INTO Adverts (title, date_created, user, price, section, category, likes) 
            VALUES (?, ?, ?, ?, ?, ?,?);
            '''
            if riadok[2] not in usernames:
                usernames.append(riadok[2])
            

            cursor.execute(insert_query, (riadok[0],riadok[1],riadok[2],riadok[3],riadok[4],riadok[5],riadok[6]))

            # create_advert_file(riadok[0],riadok[7])
            
    
        except Exception as e:
            print("Error insertig into database: ",e)

        connection.commit()

def passsword_hash( password):
    return hashlib.sha256(password.encode()).hexdigest()


write_str = ""
users = []
users_clean = []
#create users
for nazov in usernames:
    name = fake.name()
    username = nazov
    email = nazov + "@example.com"
    phone = fake.phone_number()
    slovo = fake.word()
    # password = "_".join(fake.words(2)) + str(random.randint(0,99))
    password = passsword_hash(slovo)
    users.append((name, username,email, phone, password))
    users_clean.append((name, username,email, phone, slovo))


for user in users_clean:
    write_str+= ";".join(user)+"\n"


with open("users.txt","w") as subor:
    subor.write(write_str)

with sqlite3.connect('database.db') as connection:
    cursor = connection.cursor()
    # Insert Users
    cursor.executemany('''
    INSERT INTO Users (name, username, email, phone, password)
    VALUES (?, ?, ?, ?, ?);''', users)
    
    connection.commit()