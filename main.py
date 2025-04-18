import sqlite3
import hashlib
import datetime

class Inzeraty:
    def __init__(self):
        #create both tables
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            # Create Users table
            create_users = '''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                username TEXT NOT NULL,
                age INTEGER,
                email TEXT,
                phone INTEGER,
                password TEXT
            );
            '''
            # Create Adverts table
            create_adverts = '''
            CREATE TABLE IF NOT EXISTS Adverts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                date_created DATE,
                user TEXT,
                price INTEGER,
                section TEXT,
                category TEXT
            );
            '''

            cursor.execute(create_users)
            cursor.execute(create_adverts)

            # Commit the changes
            connection.commit()


        #Load sections and categories
        self.sections = dict()

        with open("sections_categories.txt") as subor:
            riadky = subor.read().split("\n")
            categories = riadky[1].split(";")
            i = 0
            for section in riadky[0].split(" "):
                subcategories = []
                for category in categories[i].split(","):
                    subcategories.append(category.strip())

                self.sections[section] = subcategories

                i+= 1
        
        pass

            



    def add_user(self,name,age,email,phone,password,username=None):
        #check for conditions
        if "@" not in email:
            return "email"
        
        
        if username is None:
            username = "_".join(name.lower().split(" "))    
            print(username)
        
        #hash password
        hashed = self.passsword_hash(password)
        

        try:

            #insert into database
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()

                # Insert a record into the Students table
                insert_query = '''
                INSERT INTO Users (name, username, age, email, phone, password) 
                VALUES (?, ?, ?, ?, ?, ?);
                '''

                cursor.execute(insert_query, (name,username,age,email,phone,hashed))

                # Commit the changes automatically
                connection.commit()

                
                return True
        except Exception as e:
            print("Error insertig into database: ",e)
            return False
    
    def passsword_hash(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def add_advert(self,title,date_created, user, price, section, category):
        #check for conditions
        if type(title) != str or len(title) <1:
            return "Invalid title."
        
        if section not in self.sections.keys():
            section = "Ostatné"
        
        if category not in self.sections[section]:
            category = "Ostatné"
        
        if type(price) != int:
            return "Invalid price"
        elif price <0:
            return "Price cannot be negative"
        
        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()

                # Insert a record into the Adverts table
                insert_query = '''
                INSERT INTO Adverts (title, date_created, user, price, section, category) 
                VALUES (?, ?, ?, ?, ?, ?);
                '''

                cursor.execute(insert_query, (title,date_created,user,price,section,category))

                # Commit the changes automatically
                connection.commit()

                
                return True
        except Exception as e:
            print("Error insertig into database: ",e)
            return False


i = Inzeraty()
# i.add_user("Milan Lasica",23,"lasica@skibidi.sk",273982791,"skibidi123")
print(i.add_advert("Test",datetime.datetime(2009, 5, 5),"milan_lasica",999,"Ostatné","Jadrové hlavice"))