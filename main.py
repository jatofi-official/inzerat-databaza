import sqlite3
import hashlib
import datetime
import random
import tkinter as tk
from tkinter import ttk, messagebox
import faker
import os


class Inzeraty(tk.Tk):
    def __init__(self):
        #initialise window
        super().__init__()
        self.title("Adverts")
        self.geometry("800x600")

        self.resizable(False, False)


        # Load sections and categories
        self.load_sections()


        # Create both tables
        self.create_tables()

        # Create widhets
        self.create_widgets()

        # List Adverts
        self.search_adverts()

        self.right_side_created = False
        self.active_user = None

    def create_widgets(self):
        main_frame = tk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # MAIN FRAME
        main_frame.columnconfigure(0, weight=1)

        # TOP FRAME
        top_frame = ttk.Frame(main_frame)
        top_frame.grid(row=0, column=0, sticky="ew", pady=5)

        add_advert_button = ttk.Button(top_frame,text="Add advert",command=self.new_advert_pressed)
        add_advert_button.pack(side=tk.LEFT,padx=5)

        user_adverts_button = ttk.Button(top_frame,text="Show my adverts",command=self.show_my_adverts)
        user_adverts_button.pack(side=tk.LEFT,padx=5)

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
        self.category_menu.bind('<<ComboboxSelected>>', lambda e: self.search_adverts())

        search_button = ttk.Button(search_frame, text="Search",command=self.search_button_pressed)
        search_button.pack(side=tk.LEFT,padx=5)

        # ADVANCED SEARCH FRAME
        advanced_search_frame = ttk.Frame(main_frame)
        advanced_search_frame.grid(row=2, column=0, sticky="ew", pady=(2,5))

        # price
        ttk.Label(advanced_search_frame, text="Price:").pack(side=tk.LEFT, padx=5)
        ttk.Label(advanced_search_frame, text="min").pack(side=tk.LEFT, padx=2)

        self.min_var = tk.StringVar()
        min_price_entry = ttk.Entry(advanced_search_frame, textvariable=self.min_var,width=5)
        min_price_entry.pack(side=tk.LEFT)

        ttk.Label(advanced_search_frame, text="max").pack(side=tk.LEFT, padx=(5,2))

        self.max_var = tk.StringVar()
        max_price_entry = ttk.Entry(advanced_search_frame, textvariable=self.max_var,width=5)
        max_price_entry.pack(side=tk.LEFT)

        # sort by
        ttk.Label(advanced_search_frame, text="Sort by:").pack(side=tk.LEFT, padx=(6,0))
        self.sort_by_var = tk.StringVar()

        sort_by_menu = ttk.Combobox(advanced_search_frame, textvariable=self.sort_by_var, values=["Likes","Price","Title","Date"], state='readonly',width=7)
        sort_by_menu.current(0)
        sort_by_menu.pack(side=tk.LEFT)
        sort_by_menu.bind('<<ComboboxSelected>>', lambda e: self.search_adverts())

        #ascending/descentind
        self.order_by_var = tk.StringVar()

        order_by_menu = ttk.Combobox(advanced_search_frame, textvariable=self.order_by_var, values=["Descending","Ascending"], state='readonly',width=10)
        order_by_menu.current(0)
        order_by_menu.pack(side=tk.LEFT,padx=5)
        order_by_menu.bind('<<ComboboxSelected>>', lambda e: self.search_adverts())




        # BOTOTM FRAME
        self.bottom_frame = ttk.Frame(main_frame)
        self.bottom_frame.grid(row=3, column=0, sticky="nsew", padx=5, pady=5)

        main_frame.rowconfigure(3, weight=1)

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
        self.right_frame = tk.Frame(self.bottom_frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew")

        # Right content 
        # TOP FRAME
        self.advert_top_frame = ttk.Frame(self.right_frame)
        self.advert_top_frame.pack(fill=tk.X)

        self.advert_top_frame.columnconfigure(0, weight=1)
        self.advert_top_frame.columnconfigure(1, weight=0)

        self.advert_title = ttk.Label(self.advert_top_frame,text="",font=("Arial", 16, "bold"),anchor="w")
        self.advert_title.grid(row=0, column=0, sticky="w", padx=5)

        self.advert_price = ttk.Label(self.advert_top_frame,text="",anchor="e")
        self.advert_price.grid(row=0, column=1, sticky="e", padx=5)
        

        # Middle text
        self.advert_text_field = tk.Text(self.right_frame)
        self.advert_text_field.pack(fill=tk.X)
        self.advert_text_field.insert(tk.END,"")
        self.advert_text_field.config(state=tk.DISABLED)

        # BOTTOM FRAME
        self.advert_bottom_frame = ttk.Frame(self.right_frame)
        self.advert_bottom_frame.pack(fill=tk.X)
        self.advert_bottom_frame.columnconfigure(0,weight=1,uniform="half")
        self.advert_bottom_frame.columnconfigure(1,weight=1,uniform="half")
        self.advert_bottom_frame.columnconfigure(2,weight=0)

        #user
        self.advert_user = ttk.Label(self.advert_bottom_frame,text="",anchor="w")
        self.advert_user.grid(row=0, column=0, sticky="w", padx=5,pady=(5,0))
        # email
        self.advert_mail = ttk.Label(self.advert_bottom_frame,text="",anchor="w")
        self.advert_mail.grid(row=1, column=0, sticky="w", padx=5)
        # phone
        self.advert_phone = ttk.Label(self.advert_bottom_frame,text="",anchor="w")
        self.advert_phone.grid(row=2, column=0, sticky="w", padx=5)
        # date
        self.advert_date = ttk.Label(self.advert_bottom_frame,text="",anchor="w")
        self.advert_date.grid(row=3, column=0, sticky="w", padx=5)
        # like count
        self.advert_like_count = ttk.Label(self.advert_bottom_frame,text="",anchor="w")
        self.advert_like_count.grid(row=4, column=0, sticky="w", padx=5)
        
        # section title
        self.advert_section = ttk.Label(self.advert_bottom_frame,text="Section: ",anchor="w")
        self.advert_section.grid(row=0, column=1, sticky="w", padx=5,pady=(5,0))
        # category title
        self.advert_category = ttk.Label(self.advert_bottom_frame,text="Category: ",anchor="w")
        self.advert_category.grid(row=1, column=1, sticky="w", padx=5)

        #like button
        self.advert_like_button = ttk.Button(self.advert_bottom_frame,text="Like",state=tk.DISABLED)
        self.advert_like_button.grid(row=4, column=2, sticky="w", padx=5)
        
        # edit and delete buttons
        self.button_frame = ttk.Frame(self.advert_bottom_frame)
        self.button_frame.grid(row=0, column=2, rowspan=4, sticky="ne", padx=5, pady=5)

        self.advert_edit_button = ttk.Button(self.button_frame, text="Edit", state=tk.DISABLED,command=self.edit_button_pressed)
        self.advert_edit_button.pack(fill="x", pady=(0,5))

        self.advert_delete_button = ttk.Button(self.button_frame, text="Delete", state=tk.DISABLED,command=self.delete_button_pressed)
        self.advert_delete_button.pack(fill="x")

    def delete_right_side(self):
        # RIGHT FRAME
        self.right_frame.destroy()
        # Right content 
        # TOP FRAME
        self.advert_top_frame.destroy()

        self.advert_title.destroy()
        self.advert_like_count.destroy()
        # Middle text
        self.advert_text_field.destroy()
        # BOTTOM FRAME
        self.advert_bottom_frame.destroy()
        
        #user
        self.advert_user.destroy()
        
        # email
        self.advert_mail.destroy()
        # phone
        self.advert_phone.destroy()
        # date
        self.advert_date.destroy()
        # like
        self.advert_like_button.destroy()
        
        # edit and delete buttons
        self.button_frame.destroy()

        self.advert_edit_button.destroy()

        self.advert_delete_button.destroy()

        self.right_side_created = False



    def delete_button_pressed(self):
        result = messagebox.askyesno("Delete advert?","Do you really want to delete advert?")
        if self.active_advert_id is not None:
            if result: # delete advert
                query_str = "DELETE FROM Adverts WHERE id = ?;"
                try:
                    with sqlite3.connect('database.db') as connection:
                        cursor = connection.cursor()

                        cursor.execute(query_str,(self.active_advert_id,))

                        connection.commit()

                    
                    #Hide active advert 
                    self.active_advert_id = None

                    
                    self.delete_advert_file(self.advert_title["text"])

                    

                    #hide active advert text
                    self.delete_right_side()

                    #update search query
                    self.search_adverts()

                except:
                    print("Error deleting advert id:",self.active_advert_id)

    # TODO 
    def edit_button_pressed(self):
        if self.active_advert_id is not None:
            # get data:
            title = self.advert_title["text"]
            price = self.advert_price["text"][:-2]
            section = self.advert_section["text"][9:]
            category = self.advert_category["text"][10:]
            text = self.advert_text_field.get("1.0",tk.END)

            #show window
            # add the advert
            win = tk.Toplevel(self)
            
            win.title("Edit advert")
            win.geometry("500x600")

            win.resizable(False, False)
            # Right content 
            #  ano... dalo by sa to spravit cez grid ale atp i dont care, ked to funguje:)
            # TITLE FRAME
            top_frame = ttk.Frame(win)
            top_frame.pack(fill=tk.X,pady=5)
            ttk.Label(top_frame,text="Edit advert:",font=("Arial", 14, "bold"),anchor="w").pack(side=tk.LEFT,padx=5,pady=5)
            # # MAIN FRAME
            main_frame = ttk.Frame(win)
            main_frame.pack(fill=tk.X,pady=5)

            title_var = tk.StringVar(value="text")
            ttk.Label(main_frame,text="Title:").pack(side=tk.LEFT,padx=5)
            title_entry = ttk.Entry(main_frame, textvariable=title_var,width=40)
            title_entry.pack(side=tk.LEFT, padx=5)

            ttk.Label(main_frame,text="€").pack(side=tk.RIGHT,padx=5)

            price_var = tk.StringVar(value=price)
            price_entry = ttk.Entry(main_frame, textvariable=price_var,width=10)
            price_entry.pack(side=tk.RIGHT, padx=(5,2))
            ttk.Label(main_frame,text="Price:").pack(side=tk.RIGHT,padx=5)

            print((title,price))

            # CATEGORY FRAME
            category_frame = ttk.Frame(win)
            category_frame.pack(fill=tk.X,pady=5)

            ttk.Label(category_frame,text="Section:").pack(side=tk.LEFT,padx=(5,2))
            section_var = tk.StringVar()
            section_menu = ttk.Combobox(category_frame, textvariable=section_var, values=list(self.sections.keys()), state='readonly')
            
            #get current
            index = list(self.sections.keys()).index(section)

            section_menu.current(index)
            section_menu.pack(side=tk.LEFT)        
            section_menu.bind('<<ComboboxSelected>>', lambda e: change_categories())


            ttk.Label(category_frame,text="Category:").pack(side=tk.LEFT,padx=(5,2))
            category_var = tk.StringVar()
            category_menu = ttk.Combobox(category_frame, textvariable=category_var, values=[], state='readonly',width=25)

            #get current
            # z nejakeho HROZNEHO dovodu to robi presne to co chcem... ale nezobrazi toc
            category_menu.config(values=self.sections[section_var.get()])
            index2 = list(self.sections[section]).index(category)
            category_menu.current(index2)
            category_menu.pack(side=tk.LEFT)


            def change_categories():
                # print("change_categories")
                category_menu.config(values=self.sections[section_var.get()])
                category_menu.current(0)
            

            # Middle text
            advert_text_field = tk.Text(win)
            advert_text_field.pack(fill=tk.X,padx=5,pady=5)
            advert_text_field.insert(tk.END,"")

            advert_text_field.insert("1.0",text)

            # BOTTOM FRAME
            # bottom_frame = ttk.Frame(win)
            # bottom_frame.pack(fill=tk.X)

            
            def update_action():
                title = title_var.get()
                price = price_var.get()

                if not price.strip().isnumeric():
                    messagebox.showerror("Error","Price must be a number")
                    return False
                else:
                    price = int(price)
                section = section_var.get()
                category = category_var.get()
                
                text = advert_text_field.get("1.0",tk.END)

                if len(text)<2:
                    messagebox.showerror("Error","Text too short")
                    return False

                result = self.update_advert(title,self.active_user,price,section,category,text)

                if result is True:
                    win.destroy()
                    self.show_my_adverts()
                    messagebox.showinfo("Success","Succesfully created advert")

                else:
                    messagebox.showerror("Error",result)

    def search_button_pressed(self):
        self.search_adverts()

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
  
    def register_button_pressed(self):
        if self.active_user is None:
            win = tk.Toplevel(self)
            
            win.title("Register")
            win.geometry("300x240")

            win.resizable(False, False)

            self.error_message = ttk.Label(win, text="Enter personal details below:",anchor="w")
            self.error_message.grid(row=0, column=0, columnspan=2, pady=10)

            
            ttk.Label(win, text="Full name:").grid(row=1, column=0, pady=5, padx=5, sticky="e")
            name_entry = ttk.Entry(win)
            name_entry.grid(row=1, column=1, pady=5, padx=5)

            ttk.Label(win, text="Email:").grid(row=2, column=0, pady=5, padx=5, sticky="e")
            email_entry = ttk.Entry(win)
            email_entry.grid(row=2, column=1, pady=5, padx=5)

            ttk.Label(win, text="Phone (optional):").grid(row=3, column=0, pady=5, padx=5, sticky="e")
            phone_entry = ttk.Entry(win)
            phone_entry.grid(row=3, column=1, pady=5, padx=5)

            ttk.Label(win, text="Password:").grid(row=4, column=0, pady=5, padx=5, sticky="e")
            password_entry = ttk.Entry(win, show="*")
            password_entry.grid(row=4, column=1, pady=5, padx=5)

            ttk.Label(win, text="Username (optional):").grid(row=5, column=0, pady=5, padx=5, sticky="e")
            username_entry = ttk.Entry(win)
            username_entry.grid(row=5, column=1, pady=5, padx=5)

            def register_action():
                typed_name = name_entry.get()
                typed_email = email_entry.get()
                typed_phone = phone_entry.get()
                username = username_entry.get()  
                typed_password = password_entry.get()

                if username == "":
                    
                    username = "_".join(typed_name.lower().split(" "))+str(random.randint(0,1000))

                    while not self.check_valid_username(username):
                        if username is None:
                            username = "_".join(typed_name.lower().split(" "))+str(random.randint(0,1000))
                else:
                    if not self.check_valid_username(username):
                        self.error_message.config(text="Username already exists")
                        return "Username already exists"

                result = self.create_user(typed_name,typed_email,typed_phone,typed_password,username)
                if result is not True:
                    self.error_message.config(text=result)

                else:  # SUCCESSFUL LOGIN
                    if username_entry.get() =="":
                        messagebox.showinfo("New Username","Your automatically generated username is:\n"+username)
                    self.log_in([0,typed_name,username])
                    win.destroy()

            # Login button
            ttk.Button(win, text="Login", command=register_action).grid(row=6, column=0, columnspan=2, pady=10)
        
        else:
            result = messagebox.askyesno("Delete user?","Do you really want to delete your account?")
            if result is True:
                self.delete_user(self.active_user)
                self.log_out(True)

    def log_in(self,result):
        self.user_label.config(text=result[1])
        self.login_button.config(text="Log out")
        self.register_button.config(text="Delete user")
        self.active_user = result[2]

        #update current advert
        if self.right_side_created:
            if self.advert_user["text"]== "User: "+self.active_user:
                self.advert_edit_button.config(state=tk.NORMAL)
                self.advert_delete_button.config(state=tk.NORMAL)
            self.advert_like_button.config(state=tk.NORMAL)


        # print(result[2])
        self.show_my_adverts()
    
    def log_out(self,was_deleted = False):
        if was_deleted is False:
            result = messagebox.askquestion("askquestion", "Do you really want to log out?") 
        else:
            result = "yes"
        if result == "yes":
            self.user_label.config(text="Not logged in")
            self.login_button.config(text="Login")
            self.register_button.config(text="Register")

            #update current advert
            if self.right_side_created:
                if self.advert_user["text"]== "User: "+self.active_user:
                    self.active_user = None 
                    if was_deleted is True:
                        print("user was deleted and active advert belongs to user")
                        self.delete_right_side()
                        return
                    else:
                        self.advert_edit_button.config(state=tk.DISABLED)
                        self.advert_delete_button.config(state=tk.DISABLED)
                    
                self.advert_like_button.config(state=tk.DISABLED)

            
        

    #When list item is selected
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

        self.search_adverts()

    def show_my_adverts(self):
        if self.active_user is None:
            messagebox.showwarning("Not logged in","You are not logged in")
        else:
            query_str = "SELECT id,title FROM Adverts WHERE user='"+self.active_user+"' ORDER BY likes DESC;"
            # Get Adverts
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()

                cursor.execute(query_str)
                self.fetched_adverts = cursor.fetchmany(30) #EDIT HERE HOW MANY TO FETCH

            # print(fetched_adverts)
            

            self.update_listbox(self.fetched_adverts)

    #does the query
    def search_adverts(self):
        search = self.search_var.get().lower()
        section = self.section_var.get()
        category = self.category_var.get()
        
        sort_raw = self.sort_by_var.get()

        sort_by = sort_raw.lower()

        if sort_raw =="Date":
            sort_by = "date_created"

        order_by = self.order_by_var.get()
        if order_by == "Descending":
            order_by = "DESC"
        else:
            order_by = "ASC"
        
        try:    
            min_price = int(self.min_var.get().strip())
        except:
            min_price = 0
        
        try:
            max_price = int(self.max_var.get().strip())
        except:
            max_price = None

        
        price_str = "AND price BETWEEN "+str(min_price)+" AND "+str(max_price)+" "

        if max_price is None:
            price_str = "AND price >= "+str(min_price)

        if section == "All":
            query_str = "SELECT id, title FROM Adverts WHERE title LIKE '%' || ? || '%' "+price_str+" ORDER BY "+sort_by+" "+order_by+";"
        else:
            if category == "All":
                query_str = "SELECT id, title FROM Adverts WHERE section = '"+section+"' AND title LIKE '%' || ? || '%' "+price_str+" ORDER BY "+sort_by+" "+order_by+";"
            else:
                query_str = "SELECT id, title FROM Adverts WHERE category = '"+category+"' AND title LIKE '%' || ? || '%' "+price_str+" ORDER BY "+sort_by+" "+order_by+";"


        # Get Adverts
        with sqlite3.connect('database.db') as connection:
            cursor = connection.cursor()

            cursor.execute(query_str,(search,))
            self.fetched_adverts = cursor.fetchmany(30) #EDIT HERE HOW MANY TO FETCH

        # print(fetched_adverts)
        

        self.update_listbox(self.fetched_adverts)


    def update_listbox(self,content):
        self.listbox.delete(0,tk.END)
        for riadok in content:
            self.listbox.insert(tk.END,riadok[1])

    #display data on advert
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

        self.advert_price.config(text=str(advert_result[4])+" €")

        self.advert_like_count.config(text="Likes: "+str(advert_result[7])+"👍")

        self.advert_section.config(text="Section: "+advert_result[5])
        
        self.advert_category.config(text="Category: "+advert_result[6])

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

        #check if user is logged in
        if self.active_user is not None:
            self.advert_like_button.config(state=tk.NORMAL)            

            # check is active user is the same as creator
            if self.active_user == advert_result[3]:
                self.advert_edit_button.config(state=tk.NORMAL)
                self.advert_delete_button.config(state=tk.NORMAL)
                self.active_advert_id = advert_id
            else:
                self.advert_edit_button.config(state=tk.DISABLED)
                self.advert_delete_button.config(state=tk.DISABLED) 
                self.active_advert_id = None

    def get_advert_text(self, title):
        try:
            title_hash = self.title_hash(title)
            with open("Adverts/"+title_hash+".dat","rb") as subor:
                obsah = subor.read().decode()
                # print(type(obsah))
                return obsah
        except:
            messagebox.showerror("Error","Error loading advert text. Check if file exists")
            return ""

    def new_advert_pressed(self):
        if self.active_user is None:
        # if False:
            messagebox.showwarning("Not logged in","You need to be logged in to create adverts!")
        else:
            # add the advert
            win = tk.Toplevel(self)
            
            win.title("Add advert")
            win.geometry("500x600")

            win.resizable(False, False)
            # Right content 
            #  ano... dalo by sa to spravit cez grid ale atp i dont care, ked to funguje:)
            # TITLE FRAME
            top_frame = ttk.Frame(win)
            top_frame.pack(fill=tk.X,pady=5)
            ttk.Label(top_frame,text="Create new advert:",font=("Arial", 14, "bold"),anchor="w").pack(side=tk.LEFT,padx=5,pady=5)

            # MAIN FRAME
            main_frame = ttk.Frame(win)
            main_frame.pack(fill=tk.X,pady=5)

            ttk.Label(main_frame,text="Title:").pack(side=tk.LEFT,padx=5)
            title_var = tk.StringVar()
            title_entry = ttk.Entry(main_frame, textvariable=title_var,width=40)
            title_entry.pack(side=tk.LEFT, padx=5)

            ttk.Label(main_frame,text="€").pack(side=tk.RIGHT,padx=5)

            price_var = tk.StringVar()
            price_entry = ttk.Entry(main_frame, textvariable=price_var,width=10)
            price_entry.pack(side=tk.RIGHT, padx=(5,2))
            ttk.Label(main_frame,text="Price:").pack(side=tk.RIGHT,padx=5)

            # CATEGORY FRAME
            category_frame = ttk.Frame(win)
            category_frame.pack(fill=tk.X,pady=5)

            ttk.Label(category_frame,text="Section:").pack(side=tk.LEFT,padx=(5,2))
            section_var = tk.StringVar()
            section_menu = ttk.Combobox(category_frame, textvariable=section_var, values=list(self.sections.keys()), state='readonly')
            section_menu.current(5)
            section_menu.pack(side=tk.LEFT)        
            section_menu.bind('<<ComboboxSelected>>', lambda e: change_categories())


            ttk.Label(category_frame,text="Category:").pack(side=tk.LEFT,padx=(5,2))
            category_var = tk.StringVar()
            category_menu = ttk.Combobox(category_frame, textvariable=category_var, values=[], state='readonly',width=25)
            category_menu.pack(side=tk.LEFT)

            def change_categories():
                category_menu.config(values=self.sections[section_var.get()])
                category_menu.current(0)
            
            change_categories()

            # Middle text
            advert_text_field = tk.Text(win)
            advert_text_field.pack(fill=tk.X,padx=5,pady=5)
            advert_text_field.insert(tk.END,"")

            # BOTTOM FRAME
            bottom_frame = ttk.Frame(win)
            bottom_frame.pack(fill=tk.X)

            

            def create_action():
                title = title_var.get()
                price = price_var.get()

                if not price.strip().isnumeric():
                    messagebox.showerror("Error","Price must be a number")
                    return False
                else:
                    price = int(price)
                section = section_var.get()
                category = category_var.get()
                
                text = advert_text_field.get("1.0",tk.END)

                if len(text)<2:
                    messagebox.showerror("Error","Text too short")
                    return False

                result = self.create_advert(title,datetime.date.today(),self.active_user,price,section,category,text)

                if result is True:
                    win.destroy()
                    self.show_my_adverts()
                    messagebox.showinfo("Success","Succesfully created advert")

                else:
                    messagebox.showerror("Error",result)
                    
                


            # Login button
            result = ttk.Button(bottom_frame, text="Create",width=15,command=create_action).pack(side=tk.LEFT,padx=5,pady=5)
                              
            

    def create_tables(self):
        os.makedirs("Adverts",exist_ok=True)
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
            return "Password must contain at least 8 characters"
        
        #hash password
        hashed = self.passsword_hash(password)

        

        

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


    def delete_user(self,username):
        try:
            #insert into database
            with sqlite3.connect('database.db') as connection:
                cursor = connection.cursor()

                # Insert a record into the Students table
                delete_query = "DELETE FROM Users WHERE username = ?;"
                

                cursor.execute(delete_query, (username,))

                #delete all adverts by user
                search_query = "SELECT id,title FROM Adverts WHERE user = ?;"

                cursor.execute(search_query,(username,))

                results = cursor.fetchall()
                for result in results:
                    cursor.execute("DELETE FROM Adverts WHERE id=?;",(result[0],))
                    self.delete_advert_file(result[1])

                # Commit the changes automatically
                connection.commit()

            self.search_adverts()
            
            return True
        except Exception as e:
            print("Error deleting from database: ",e)
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
            return True
        
        return "Error creating advert"
            

    def create_advert_file(self,title,text):
        nazov = self.title_hash(title)
        with open("Adverts/"+nazov+".dat","wb") as subor:
            byte_text = text.encode()
            subor.write(byte_text)

    def delete_advert_file(self,title):
        # Delete file
        filename = self.title_hash(title)
        
        try:
            os.remove("Adverts/"+filename+".dat")
        except Exception as e:
            print(e)

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

    def update_advert(self,title,user,price,section,category,text):
        pass
        
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
    # i.create_advert("I want to sell my Laptop",datetime.date.today(),"admin",9999,"PC","Desktop","This is my very special pc, I built it lorem ipsum lorem ipsum")
    i.log_in([0,"admin","admin"])
    i.mainloop()
    