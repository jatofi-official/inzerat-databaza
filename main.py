import sqlite3
import hashlib
import datetime
import random
import tkinter as tk
from tkinter import ttk, messagebox
import faker


class Inzeraty(tk.Tk):
    def __init__(self):
        #initialise window
        super().__init__()
        self.title("Adverts")
        self.geometry("800x600")


        # Load sections and categories
        self.load_sections()


        # Create both tables
        self.create_tables()

        # Create widhets
        self.create_widgets()

        # List Adverts
        self.update_adverts()


    def create_widgets(self):
        # TOP FRAME 

        top_frame = ttk.Frame(self)
        top_frame.pack(fill=tk.X, pady=5)

        register_button = ttk.Button(top_frame, text="Register")
        register_button.pack(side=tk.RIGHT,padx=5)

        login_button = ttk.Button(top_frame, text="Login")
        login_button.pack(side=tk.RIGHT, padx=5)

        self.user_label = ttk.Label(top_frame, text="Not logged in")
        self.user_label.pack(side=tk.RIGHT, padx=5)


        # SEARCH FRAME

        search_frame = ttk.Frame(self)
        search_frame.pack(fill=tk.X, pady=(10,5))

        # Search entry
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT,padx=5)
        self.search_var = tk.StringVar()

        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame,textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT,padx=5)
        # search_entry = ttk.Entry(search_frame, textvariable=self.search_var)

        # Sections
        ttk.Label(search_frame, text="Section:").pack(side=tk.LEFT,padx=(6,0))
        self.section_var = tk.StringVar()

        self.section_menu = ttk.Combobox(search_frame, textvariable=self.section_var, values=['All'] + [key for key in self.sections.keys()], state='readonly')
        self.section_menu.current(0)
        self.section_menu.pack(side=tk.LEFT)
        self.section_menu.bind('<<ComboboxSelected>>', lambda e: self.update_categories())

        # Categories
        ttk.Label(search_frame, text="Category:").pack(side=tk.LEFT,padx=(6,0))
        self.category_var = tk.StringVar()

        self.category_menu = ttk.Combobox(search_frame, textvariable=self.category_var, values=['All'], state='readonly')
        self.category_menu.current(0)
        self.category_menu.pack(side=tk.LEFT)
        self.category_menu.bind('<<ComboboxSelected>>', lambda e: self.update_adverts())

        # BOTTOM FRAME
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill=tk.X,padx=5,pady=5)

        left_frame = tk.Frame(bottom_frame, bg="red")
        right_frame = tk.Frame(bottom_frame, bg="blue")

        left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        right_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # Listbox of 
        self.listbox = tk.Listbox(left_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_item_selected)

    
    def on_item_selected(self,event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            id = self.fetched_adverts[index][0]

            # print(f"Selected index: {index}, id: {id}")

            self.show_advert_details(id)

    
    def update_categories(self):
        section = self.section_var.get()

        if section != "All":        
            self.category_menu["values"] = ["All"] + self.sections[section]
            self.category_menu.current(0)

        self.update_adverts()

    def update_adverts(self):
        search = self.search_var.get().lower()
        section = self.section_var.get()
        category = self.category_var.get()

        if section == "All":
            query_str = "SELECT id, title FROM Adverts ORDER BY Likes DESC"
        else:
            if category == "All":
                query_str = "SELECT id, title FROM Adverts WHERE section = '"+section+"' ORDER BY Likes DESC"
            else:
                query_str = "SELECT id, title FROM Adverts WHERE category = '"+category+"' ORDER BY Likes DESC"

        print(query_str)

        # Get Adverts
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            cursor.execute(query_str)
            self.fetched_adverts = cursor.fetchmany(5)

        # print(fetched_adverts)
        

        self.update_listbox(self.fetched_adverts)


    def update_listbox(self,content):
        self.listbox.delete(0,tk.END)
        for riadok in content:
            print(riadok)
            self.listbox.insert(tk.END,riadok[1])

    def show_advert_details(self,advert_id):
        pass




    def create_tables(self):
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
                category TEXT,
                likes INTEGER
            );
            '''

            cursor.execute(create_users)
            cursor.execute(create_adverts)

            # Commit the changes
            connection.commit()

    def load_sections(self):
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
            username = "_".join(name.lower().split(" "))+str(random.randint(0,1000))

            while not self.check_valid_username(username):
                if username is None:
                    username = "_".join(name.lower().split(" "))+str(random.randint(0,1000))
        else:
            if not self.check_valid_username(username):
                return "Username already exists"

        

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


    def check_valid_username(self,username):
        with sqlite3.connect("database.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT username FROM Users where username= ?",(username,))
            data = cursor.fetchall()
            if not data: #username not found => is unique
                return True
            else:
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
        
        #create advert text file 
        if result:
            self.create_advert_file(title,text)
            

    def create_advert_file(self,title,text):
        nazov = self.title_hash(title)
        with open("Adverts/"+nazov+".dat","wb") as subor:
            byte_text = text.encode()
            subor.write(byte_text)

    def insert_advert(self,title,date_created, user, price, section, category):

        try:
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()

                # Insert a record into the Adverts table
                insert_query = '''
                INSERT INTO Adverts (title, date_created, user, price, section, category, likes) 
                VALUES (?, ?, ?, ?, ?, ?,0);
                '''

                cursor.execute(insert_query, (title,date_created,user,price,section,category))

                # Commit the changes automatically
                connection.commit()

                
                return True
        except Exception as e:
            print("Error insertig into database: ",e)
            return False

    def title_hash(self,title):
        return hashlib.md5(title.encode()).hexdigest()


    def fill_random(self,num_users=0, num_adverts=0):
        fake = faker.Faker()

        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            # Generate users
            users = []
            for i in range(num_users):
                name = fake.name()
                username = "_".join(name.lower().split(" "))+str(random.randint(0,10))
                email = "_".join(name.lower().split(" "))+str(random.randint(0,10)) + "@example.com"
                phone = fake.random_int(min=1000000000, max=9999999999)
                # password = "_".join(fake.words(2)) + str(random.randint(0,99))
                password = self.passsword_hash(fake.word())
                users.append((name, username,email, phone, password))

            # Insert Users
            cursor.executemany('''
            INSERT INTO Users (name, username, email, phone, password)
            VALUES (?, ?, ?, ?, ?);''', users)
            

            # Generate adverts

            # get usernames
            cursor.execute('SELECT username FROM Users')
            usernames = [row[0] for row in cursor.fetchall()]


            adverts = []
            for i in range(num_adverts):


                date_created = fake.date_between(start_date='-1y', end_date='today')
                user = random.choice(usernames)
                price = random.randint(10, 1000)

                title = "Selling " + fake.word() + " for " +str(price) + " €"
                
                section = random.choice(list(self.sections.keys()))
                category = random.choice(self.sections[section])
                likes = random.randint(0,256)

                adverts.append((title, date_created, user, price, section, category,likes))

                text = ""
                for sentence in fake.sentences(random.randint(5,11)):
                    text += sentence + " "
                # print(text)

                self.create_advert_file(title,text)


            # print(*adverts,sep="\n")

            
            # Insert Adverts

            cursor.executemany('''
            INSERT INTO Adverts (title, date_created, user, price, section, category, likes)
            VALUES (?, ?, ?, ?, ?, ?, ?);''', adverts)

            connection.commit()


if __name__ == '__main__':
    i = Inzeraty()
    i.mainloop()
    # i.fill_random(10,20)
    # print(i.create_user("admin","admin@admin",0,"adminadmin","admin8"))
    # i.create_advert("Test",datetime.datetime(2009, 5, 5),"admin",999,"Ostatné","Jadrové hlavice","skibiditextaôldsfôlsadfjs")