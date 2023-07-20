import tkinter as tk
from tkinter import *
from db_connect import *
from login import *

class Home(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Horizon Cinemas")
        #self.geometry('300x300')

        self.frame = Frame(self).grid(row=0, column=0)

        self.login_button = Button(self, text="Login", command=self.login).grid(row=0, column=0, padx=50, pady=30)
        self.register_button = Button(self, text="Register", command=self.reg).grid(row=1, column=0, padx=50, pady=30)

    def login(self):
        self.newWindow = Toplevel(self)
        model = User
        view = userView(self.newWindow)
        view.grid(row=0, column=0, padx = 10, pady = 10)       

        controller = Login_Controller(model, view)

        view.set_controller(controller)
        self.withdraw()

    def reg(self):
        self.newWindow = Toplevel(self)
        model = User
        view = userView(self.newWindow)
        view.grid(row=0, column=0)
        controller = Login_Controller(model, view)
        view.set_controller(controller)
        self.withdraw()



if __name__ == '__main__':
    app = Home()
    app.mainloop()