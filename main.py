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

        self.right_side_created = False
        self.active_user = None

    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # MAIN FRAME
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # TOP FRAME
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=5)

        self.register_button = ttk.Button(top_frame, text="Register",command=self.register_button_pressed)
        self.register_button.pack(side=tk.RIGHT, padx=5)

        self.login_button = ttk.Button(top_frame, text="Login",command=self.login_button_pressed)
        self.login_button.pack(side=tk.RIGHT, padx=5)

        self.user_label = ttk.Label(top_frame, text="Not logged in")
        self.user_label.pack(side=tk.RIGHT, padx=5)


        # SEARCH FRAME
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=1, column=0, sticky="ew", pady=(10, 5))

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=5)

        # Sections
        ttk.Label(search_frame, text="Section:").pack(side=tk.LEFT, padx=(6,0))
        self.section_var = tk.StringVar()

        self.section_menu = ttk.Combobox(search_frame, textvariable=self.section_var, values=['All'] + list(self.sections.keys()), state='readonly')
        self.section_menu.current(0)
        self.section_menu.pack(side=tk.LEFT)
        self.section_menu.bind('<<ComboboxSelected>>', lambda e: self.update_categories())

        # Categories
        ttk.Label(search_frame, text="Category:").pack(side=tk.LEFT, padx=(6,0))
        self.category_var = tk.StringVar()

        self.category_menu = ttk.Combobox(search_frame, textvariable=self.category_var, values=['All'], state='readonly')
        self.category_menu.current(0)
        self.category_menu.pack(side=tk.LEFT)
        self.category_menu.bind('<<ComboboxSelected>>', lambda e: self.update_adverts())

        # BOTOTM FRAME
        self.bottom_frame = ttk.Frame(main_frame)
        self.bottom_frame.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        main_frame.rowconfigure(2, weight=1)

        # Proporitons here:
        self.bottom_frame.columnconfigure(0, weight=2, uniform="half")
        self.bottom_frame.columnconfigure(1, weight=3, uniform="half")
        self.bottom_frame.rowconfigure(0, weight=1)



        # LEFT FRAME
        left_frame = tk.Frame(self.bottom_frame)
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Left content
        self.listbox = tk.Listbox(left_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        self.listbox.bind('<<ListboxSelect>>', self.on_item_selected)

    def create_right_side(self):
        # RIGHT FRAME
        right_frame = tk.Frame(self.bottom_frame)
        right_frame.grid(row=0, column=1, sticky="nsew")

        # Right content 
        # TOP FRAME
        advert_top_frame = ttk.Frame(right_frame)
        advert_top_frame.pack(fill=tk.X)

        advert_top_frame.columnconfigure(0, weight=1)
        advert_top_frame.columnconfigure(1, weight=0)

        self.advert_title = ttk.Label(advert_top_frame,text="",font=("Arial", 16, "bold"),anchor="w")
        self.advert_title.grid(row=0, column=0, sticky="w", padx=5)

        self.advert_like_count = ttk.Label(advert_top_frame,text="",anchor="e")
        self.advert_like_count.grid(row=0, column=1, sticky="e", padx=5)

        # Middle text
        self.advert_text_field = tk.Text(right_frame)
        self.advert_text_field.pack(fill=tk.X)
        self.advert_text_field.insert(tk.END,"")
        self.advert_text_field.config(state=tk.DISABLED)

        # BOTTOM FRAME
        advert_bottom_frame = ttk.Frame(right_frame)
        advert_bottom_frame.pack(fill=tk.X)
        advert_bottom_frame.columnconfigure(0,weight=1)

        #user
        self.advert_user = ttk.Label(advert_bottom_frame,text="",anchor="w")
        self.advert_user.grid(row=0, column=0, sticky="w", padx=5)
        # email
        self.advert_mail = ttk.Label(advert_bottom_frame,text="",anchor="w")
        self.advert_mail.grid(row=1, column=0, sticky="w", padx=5)
        # phone
        self.advert_phone = ttk.Label(advert_bottom_frame,text="",anchor="w")
        self.advert_phone.grid(row=2, column=0, sticky="w", padx=5)
        # date
        self.advert_date = ttk.Label(advert_bottom_frame,text="",anchor="w")
        self.advert_date.grid(row=3, column=0, sticky="w", padx=5)
        # like
        self.advert_like_button = ttk.Button(advert_bottom_frame,text="Like")
        self.advert_like_button.grid(row=4, column=0, sticky="w", padx=5)
        
        # edit and delete buttons
        button_frame = ttk.Frame(advert_bottom_frame)
        button_frame.grid(row=0, column=1, rowspan=4, sticky="ne", padx=5, pady=5)

        self.advert_edit_button = ttk.Button(button_frame, text="Edit", state=tk.DISABLED)
        self.advert_edit_button.pack(fill="x", pady=(0,5))

        self.advert_delete_button = ttk.Button(button_frame, text="Delete", state=tk.DISABLED)
        self.advert_delete_button.pack(fill="x")



    def login_button_pressed(self):
        if self.active_user is None:
            win = tk.Toplevel(self)
            
            win.title("Login")
            win.geometry("300x200")

            win.resizable(False, False)

            self.error_message = ttk.Label(win, text="Enter login details below:")
            self.error_message.grid(row=0, column=0, columnspan=2, pady=10)

            
            ttk.Label(win, text="Username:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
            username_entry = ttk.Entry(win)
            username_entry.grid(row=1, column=1, pady=5, padx=5)

            ttk.Label(win, text="Password:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
            password_entry = ttk.Entry(win, show="*")
            password_entry.grid(row=2, column=1, pady=5, padx=5)

            def login_action():
                typed_username = username_entry.get()  
                typed_password = password_entry.get()

                hashed = self.passsword_hash(typed_password)

                # Check login information                
                query_str = "SELECT * FROM Users WHERE username = ? AND password = ?"
                with sqlite3.connect('database.db') as connection:
                    cursor = connection.cursor()
                    query_str = "SELECT * FROM Users WHERE username = ? AND password = ?"
                    cursor.execute(query_str, (typed_username, hashed))
                    result = cursor.fetchone()


                if result:  # SUCCESSFUL LOGIN
                    self.log_in(result)
                    win.destroy()
                else:
                    self.error_message.config(text="Incorrect username or password!")

            # Login button
            ttk.Button(win, text="Login", command=login_action).grid(row=3, column=0, columnspan=2, pady=10)
        
        else:
            self.log_out()

    #TODO     
    def register_button_pressed(self):
        if self.active_user is None:
            print("register")
        else:
            print("settings")


    def log_in(self,result):
        self.user_label.config(text=result[1])
        self.login_button.config(text="Log out")
        self.register_button.config(text="Settings")
        self.active_user = result[1]
    
    def log_out(self):
        result = messagebox.askquestion("askquestion", "Do you really want to log out?") 
        if result == "yes":
            self.user_label.config(text="Not logged in")
            self.login_button.config(text="Login")
            self.register_button.config(text="Register")
            self.active_user = None

    def on_item_selected(self,event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            id = self.fetched_adverts[index][0]

            # print(f"Selected index: {index}, id: {id}")

            if not self.right_side_created:
                self.create_right_side()
                self.right_side_created = True

            self.show_advert_details(id)

    
    def update_categories(self):
        section = self.section_var.get()

        if section != "All":        
            self.category_menu["values"] = ["All"] + self.sections[section]
            self.category_menu.current(0)

        self.update_adverts()


    #does the query
    def update_adverts(self):
        search = self.search_var.get().lower()
        section = self.section_var.get()
        category = self.category_var.get()

        if section == "All":
            query_str = "SELECT id, title FROM Adverts ORDER BY likes DESC;"
        else:
            if category == "All":
                query_str = "SELECT id, title FROM Adverts WHERE section = '"+section+"' ORDER BY likes DESC;"
            else:
                query_str = "SELECT id, title FROM Adverts WHERE category = '"+category+"' ORDER BY likes DESC;"


        # Get Adverts
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            cursor.execute(query_str)
            self.fetched_adverts = cursor.fetchmany(25) #EDIT HERE HOW MANY TO FETCH

        # print(fetched_adverts)
        

        self.update_listbox(self.fetched_adverts)


    def update_listbox(self,content):
        self.listbox.delete(0,tk.END)
        for riadok in content:
            self.listbox.insert(tk.END,riadok[1])

    def show_advert_details(self,advert_id):
        query_str = "SELECT * FROM Adverts WHERE id=?;"

        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            cursor.execute(query_str,(advert_id,))

            advert_result = cursor.fetchone()
            cursor.execute("SELECT * FROM Users WHERE username=?;",(advert_result[3],))
            user_result = cursor.fetchone()
        
        #AFFECT STUFF
        self.advert_title.config(text=advert_result[1])
        self.advert_like_count.config(text="Likes: "+str(advert_result[7])+"👍")
        
        # text field
        self.advert_text_field.config(state=tk.NORMAL)
        self.advert_text_field.delete("1.0",tk.END)
        obsah = self.get_advert_text(advert_result[1])
        
        self.advert_text_field.insert(tk.END,obsah)
        self.advert_text_field.config(state=tk.DISABLED)

        # user details
        self.advert_user.config(text="User: "+user_result[1])
        self.advert_mail.config(text="Email: "+user_result[3])
        self.advert_phone.config(text="Phone: "+str(user_result[4]))
        
        # date
        self.advert_date.config(text="Posted on: "+str(advert_result[2]))

    def get_advert_text(self, title):
        title_hash = self.title_hash(title)
        with open("Adverts/"+title_hash+".dat","rb") as subor:
            obsah = subor.read().decode()
            # print(type(obsah))
            return obsah

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
    # i.insert_user("admin","",0,i.passsword_hash("admin"),"admin")
    
    i.mainloop()
    
    # i.fill_random(0,20)