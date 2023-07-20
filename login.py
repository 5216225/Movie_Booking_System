from tkinter import *
import tkinter as tk
import sqlite3
import re
from BookingStaff import *

conn = sqlite3.connect('customer.db')
cur = conn.cursor()

#User class
class User:
    def __init__(self):
        self.__user = ""
        self.__password = ""
        self.__usertype = ""
    
    def getUser(self):
        return self.__user

    def setUser(self, user):
        self.__user = user
    
    def getPassword(self):
        return self.__password

    def setUsertype(self, usertype):
        self.__usertype = usertype

    def getUsertype(self):
        return self.__usertype

    def setPassword(self, password):
        self.__password = password
    
    def getPasswordLength(self):
        return len(self.getPassword())

    def saveUserNamePassword(self, un, pw): #save username and password in database
            query = 'INSERT INTO customers (username, password) VALUES (? , ?);'
            cur.execute(query, (un, pw))
            conn.commit()
            print('Username and password successfully saved')
            return 1

    def findUser(self, un):
        cur.execute('SELECT * FROM customers WHERE username = ?;', [un])
        record = cur.fetchall()
        
        if len(record)>0:
            print('record exists')
            return 1    #record exists
        else:
            print('record does not exist')
            return 0    #record does not exist   

    def checkUserNamePassword(self, un, pw): 
        query = 'SELECT * FROM customers WHERE username = ? AND password = ?;'
        cur.execute(query, (un, pw))
        record = cur.fetchall()
        
        if len(record)>0:
            print('record exists')
            return 1    #record exists
        else:
            print('record does not exist')
            return 0    #record does not exist   

        
    def __str__(self):
        print("User: " + self.getUser() + " Password: " + self.getPassword())

class userView(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        #self.container = container
        self.container = container
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
  
        self.__username = StringVar()
        self.__password = StringVar()
        self.username_label = Label(self, text="Username:")
        self.username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        self.username_entry = Entry(self, textvariable=self.__username)
        self.username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
        self.password_label = Label(self, text="Password:")
        self.password_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.password_entry = Entry(self, textvariable=self.__password, show="*")
        self.password_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)
        self.login_button = Button(self, text="Login", command=self.login)
        self.login_button.grid(column=0, row=3, sticky=tk.E, padx=5, pady=5)
        self.signup_button = Button(self, text="SignUp", command=self.signup)
        self.signup_button.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

        self.message_label = Label(self, text='                                    ', foreground='black')
        self.message_label.grid(column=1, row=4, padx=5, pady=5)           

        self.controller = None

        
    def getUsername(self):
        return self.__username

    def getPassword(self):
        return self.__password

    def set_controller(self, controller):
        self.controller = controller
    
    def show_success(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

        self.username_entry.delete(0,'end')
        self.password_entry.delete(0,'end')
        self.username_entry['foreground'] = 'black'
        self.password_entry['foreground'] = 'black'
        self.__username.set('')
        self.__password.set('')
    
    def hide_message(self):
        self.message_label['text'] = ''
    
    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'        
        self.username_entry['foreground'] = 'red'
        self.password_entry['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)
    
    
    def nextwindow(self, username):
        user = username
        self.newWindow = Toplevel(self.container)
        view = Booking_staff_main(self.newWindow, user)
        view.grid(row=0, column=0, padx = 10, pady = 10)
        controller = BookingController(view)
        view.set_controller(controller)
       
        self.container.withdraw()
    
    

    def login(self):
        if self.controller:
            self.controller.login(self.__username.get(), self.__password.get())
              
    def signup(self):
        if self.controller:
            self.controller.signup(self.__username.get(), self.__password.get())

class Login_Controller:
    def __init__(self, model, view):
        self.model = model 
        self.view = view

    def signup(self, username, password):        
        try:
            if self.model.findUser(self,username):
                self.view.show_error('The given username already exists.')   
            else:
                if self.model.saveUserNamePassword(self, username, password): #save username and password
                    print('username and password saved')                        
                    self.view.show_success(f'The username {username} and password saved!')
                else:
                    print('username and password could not be saved!')                        
                    self.view.show_error(f'The username {username} and password could not be saved!')      
                    
        except ValueError as error:
            self.view.show_error(error)


    def login(self, username, password):
        try:
    
            if self.model.checkUserNamePassword(self, username, password): 
                print('username and password found')
                self.view.show_success('Successful login!')
                self.view.nextwindow(username)
            else:
                print('username or password does not exist')
                self.view.show_error('Login failed!')
                
            
        except ValueError as error:
            self.view.show_error(error)
