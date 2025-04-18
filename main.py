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

    
    def create_user(self,name,email,phone,password,username=None):
        #check for conditions

        #name
        if type(name) != str or len(name)<1:
            return "Invalid name"
        

        #email
        if "@" not in email:
            return "Invalid email"
        
        #phone
        #TODO
        
        #password
        if type(password) != str or len(password)<8:
            return "Invalid password. Password must contain at least 8 characters"
        
        #hash password
        hashed = self.passsword_hash(password)

        #create username
        if username is None:
            username = "_".join(name.lower().split(" "))
        
        #insert into database
        result = self.insert_user(name,email,phone,hashed,username)
        return result


    def insert_user(self,name,email,phone,password,username):

        try:

            #insert into database
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()

                # Insert a record into the Students table
                insert_query = '''
                INSERT INTO Users (name, username, email, phone, password) 
                VALUES (?, ?, ?, ?, ?);
                '''

                cursor.execute(insert_query, (name,username,email,phone,password))

                # Commit the changes automatically
                connection.commit()

                
                return True
        except Exception as e:
            print("Error insertig into database: ",e)
            return False
    
    def passsword_hash(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_advert(self,title,date_created, user, price, section, category,text):
        #check for conditions
        
        #title
        if type(title) != str or len(title) <1:
            return "Invalid title."
        
        #section
        if section not in self.sections.keys():
            section = "Ostatné"
        
        #category
        if category not in self.sections[section]:
            category = "Ostatné"
        
        #price
        if type(price) != int:
            return "Invalid price"
        elif price <0:
            return "Price cannot be negative"

        #insert advert
        result = self.insert_advert(title,date_created,user,price,section,category)

    def insert_advert(self,title,date_created, user, price, section, category):

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
print(i.create_user("admin","admin@admin",0,"adminadmin"))
# print(i.add_advert("Test",datetime.datetime(2009, 5, 5),"milan_lasica",999,"Ostatné","Jadrové hlavice"))