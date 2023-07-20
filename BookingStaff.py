import tkinter.messagebox
from datetime import datetime, date
from functools import partial
from random import randrange
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

from db_connect import *
from movies import *

bookingConn = getConn()
bookingCur = getCursor()

userConn = sqlite3.connect('customer.db')
userCur = userConn.cursor()

#########################
## Booking Staff Pages ##   
#########################

#Booking Staff Main Page once logged in
class Booking_staff_main(tk.Frame):
    #Booking Staff main menu page. Allows user to update profile, see booking history, and search for films by date
    def __init__(self, master, user):
        super().__init__(master)
        self.master = master
        self.__user = user
        self.defdate1 = StringVar()
        self.controller = None
        self.cinema = StringVar()


        self.user_label = Label(self, text=f"Welcome! {self.__user}")
        self.user_label.grid(row=0, column=0, padx=5, pady=5)

        
        #Button for Updating Profile
        self.up = Button(self.master, font=("Helvetica", 16), text="Update Profile", bg="yellow", command=self.Update_Profile_window)
        self.up.grid(row=1, column=0, padx=5, pady=5)
        #Button for Booking History
        self.bh = Button(self.master, font=("Helvetica", 16), text="Booking History", bg="yellow", command=self.Booking_History_window)
        self.bh.grid(row=2, column=0, padx=5, pady=5)
        #Label for "Search for films by date:"
        self.search_label = Label(self.master, font=("Helvetica", 16), text='Search for films by date:')
        self.search_label.grid(row=3, column=0, padx=5, pady=5)

        # default value
        dates=[]
        cur.execute('SELECT date FROM Show')
        holder = cur.fetchall()
        for date in holder:
            date = str(date)
            date = date.strip("(),'' ")
            if date not in dates:
                dates.append(date)
        dates.sort()
        #dates = ["Monday 01/12/22", "Tuesday 02/12/22", "Wednesday 03/12/22", "Thursday 04/12/22", "Friday 05/12/22", "Saturday 06/12/22", "Sunday 07/12/22" ]
        self.defdate1.set("Pick a date...") 
        self.datelist1 = OptionMenu(master, self.defdate1, *dates)
        self.datelist1.grid(row=4, column=0, padx=5, pady=5)
        self.datelist1.config(width=15)

        bookingCur.execute('SELECT cinemaName FROM Cinema')
        holder = bookingCur.fetchall()
        #print(holder)
        cinemas = []
        for cinema in holder:
            cinema = str(cinema)
            cinema = cinema.strip("(),'' ")
            cinemas.append(cinema)
        #print(cinemas)
        self.cinema.set("Pick a cinema...") 
        self.cities = OptionMenu(master, self.cinema, *cinemas)
        self.cities.grid(row=5, column=0, padx=5, pady=5)
        #Button for Searching films within specified date
        self.searching = Button(self.master, text="Search", command=self.search)
        self.searching.grid(row=6, column=0, padx=5, pady=5)

        userCur.execute('SELECT usertype FROM customers WHERE username=?', [self.__user])
        hold = userCur.fetchone()
        usertype = hold[0]
        print(usertype)

        self.box = Frame(self.master)
        self.box.grid(row=8, column=0, padx=1, pady=1)

        self.show_frame = Frame(self.master)
        self.show_frame.grid(row=9, column=0, padx=10, pady=10)
        
        if usertype == 'admin':
            self.addmovie_button = Button(self.box, text="Add a new movie", command=self.addMovie).grid(row=0, column=0, padx=3, pady=3)
            self.getmovie_button = Button(self.box, text="Get List of Movies", command=self.movielist).grid(row=0, column=1, padx=3, pady=3)
            self.addshow_button = Button(self.box, text="Add a new show", command=self.addshow).grid(row=0, column=2, padx=3, pady=3)
            self.adminreport_button = Button(self.box, text="Generate an admin report", command=self.adminreport).grid(row=0, column=3, padx=3, pady=3)

        if usertype == 'manager':
            self.addcity_button = Button(self.box, text="Add a new city", command=self.addcity).grid(row=0, column=0, padx=3, pady=3)
            self.addcinema_button = Button(self.box, text="Add a new cinema", command=self.addcinema).grid(row=0, column=1, padx=3, pady=3)

        #Button for Logging out
        self.logout_button = Button(self.master, font=("Helvetica", 12), text="Logout", command=self.logout)
        self.logout_button.grid(row=7, column=0, padx=5, pady=5, sticky=E)


    def set_controller(self, controller):
        self.controller = controller

    def addcinema(self):
        self.cinema_frame = Frame(self.master)
        self.cinema_frame.grid(row=9, column=0, padx=10, pady=10)
        self.cinema = StringVar()
        self.city = StringVar()
        bookingCur.execute('SELECT city_name FROM City')
        cities = bookingCur.fetchall()

        cinema_label = Label(self.cinema_frame, text="Cinema Name : ").grid(row=0, column=0, padx=5, pady=5)
        cinema_entry = Entry(self.cinema_frame,textvariable= self.cinema).grid(row=0, column=1, padx=5, pady=5)

        city_label = Label(self.cinema_frame, text="Choose a city : ").grid(row=1, column=0, padx=5, pady=5)
        city_entry = OptionMenu(self.cinema_frame, self.city, *cities).grid(row=1, column=1, padx=5, pady=5)

        confirm_button = Button(self.cinema_frame, text="Confirm", command=self.addCinema).grid(row=2, column=0, padx=5, pady=5)

    def addCinema(self):
        if self.controller:
            city = str(self.city.get())
            city = city.strip(" (),'' ")
            self.controller.addCinema(self.cinema.get(), city)

    def Cinema(self, cinema, city):
        bookingCur.execute('INSERT INTO Cinema (cinemaName, City) VALUES (?,?)', (cinema, city,))
        conn.commit()
        tkinter.messagebox.showinfo(" --- ADDED --- ","A new cinema has been added successfully.", icon="info")

        return 1
    
    def addcity(self):
        self.city_frame = Frame(self.master)
        self.city_frame.grid(row=9, column=0, padx=10, pady=10)
        self.cityname = StringVar()
        self.morningPrice = IntVar()
        self.afternoonPrice = IntVar()
        self.eveningPrice = IntVar()

        cityname_label = Label(self.city_frame, text="City : ").grid(row=0, column=0, padx=5, pady=5)
        cityname_entry = Entry(self.city_frame,textvariable= self.cityname).grid(row=0, column=1, padx=5, pady=5)

        morningprice_label = Label(self.city_frame, text="Enter Price for morning shows : ").grid(row=1, column=0, padx=5, pady=5)
        morningprice_entry = Entry(self.city_frame, textvariable=self.morningPrice).grid(row=1, column=1, padx=5, pady=5)

        afternoonprice_label = Label(self.city_frame, text="Enter Price for afternoon shows : ").grid(row=2, column=0, padx=5, pady=5)
        afternoonprice_entry = Entry(self.city_frame, textvariable=self.afternoonPrice).grid(row=2, column=1, padx=5, pady=5)

        eveningprice_label = Label(self.city_frame, text="Enter Price for evening shows : ").grid(row=3, column=0, padx=5, pady=5)
        eveningprice_entry = Entry(self.city_frame, textvariable=self.eveningPrice).grid(row=3, column=1, padx=5, pady=5)

        confirm_button = Button(self.city_frame, text="Confirm", command=self.addcities).grid(row=4, column=0, padx=5, pady=5)

    def addcities(self):
        if self.controller:
            self.controller.addCity(self.cityname.get(), self.morningPrice.get(), self.afternoonPrice.get(), self.eveningPrice.get())

    def addCity(self, cityname, mPrice, aPrice, ePrice):
        bookingCur.execute('INSERT INTO City (city_name, morning_price, afternoon_price, evening_price) VALUES (?,?,?,?)', (cityname, mPrice, aPrice, ePrice))
        conn.commit()
        tkinter.messagebox.showinfo("---- ADDED ----","A new city has been added successfully.", icon="info")

        return 1

    def addshow(self):
        self.show_frame = Frame(self.master)
        self.show_frame.grid(row=9, column=0, padx=10, pady=10)
        self.showtime = StringVar()
        self.screen = IntVar()
        self.movie = StringVar()
        self.movieID = ""
        self.date = StringVar()
        self.lowerHall = IntVar()
        self.upperHall = IntVar()
        self.vip = IntVar()

        bookingCur.execute('SELECT movieName FROM Movie')
        movies = bookingCur.fetchall()

        movie_label = Label(self.show_frame, text="Movie : ").grid(row=0, column=0, padx=5, pady=5)
        movie_entry = OptionMenu(self.show_frame, self.movie, *movies).grid(row=0, column=1, padx=5, pady=5)

        showtime_label = Label(self.show_frame, text="Enter show time : ").grid(row=1, column=0, padx=5, pady=5)
        showtime_entry = Entry(self.show_frame, textvariable=self.showtime).grid(row=1, column=1, padx=5, pady=5)

        screen_label = Label(self.show_frame, text="Screen : ").grid(row=2, column=0, padx=5, pady=5)
        screen_entry = Entry(self.show_frame, textvariable=self.screen).grid(row=2, column=1, padx=5, pady=5)

        date_label = Label(self.show_frame, text="Date : ").grid(row=3, column=0, padx=5, pady=5)
        date_entry = Entry(self.show_frame, textvariable=self.date).grid(row=3, column=1, padx=5, pady=5)
        
        lowerhall_label = Label(self.show_frame, text="Lower Hall Availability : ").grid(row=4, column=0, padx=5, pady=5)
        lowerhall_entry = Entry(self.show_frame, textvariable=self.lowerHall).grid(row=4, column=1, padx=5, pady=5)
        
        upperhall_label = Label(self.show_frame, text="Upper Hall Availability : ").grid(row=5, column=0, padx=5, pady=5)
        upperhall_entry = Entry(self.show_frame, textvariable=self.upperHall).grid(row=5, column=1, padx=5, pady=5)
        
        vip_label = Label(self.show_frame, text="VIP Availability : ").grid(row=6, column=0, padx=5, pady=5)
        vip_entry = Entry(self.show_frame, textvariable=self.vip).grid(row=6, column=1, padx=5, pady=5)
        
        confirm_button = Button(self.movie_frame, text="Confirm", command=self.addShow).grid(row=7, column=0, padx=5, pady=5)

    def addShow(self):
        if self.controller:
            self.controller.addshowing(self.movie.get(), self.showtime.get(), self.screen.get(), self.date.get(), self.lowerHall.get(), self.upperHall.get(), self.vip.get())

    def addshowing(self, moviename, showtime, screen, date, lowerhall, upperhall, vip):
        bookingCur.execute('SELECT movieID WHERE moiveName=?', [moviename])
        movieid = bookingCur.fetchone()
        bookingCur.execute('INSERT INTO Show (showTime, Screen, movieID, date, lowerHall, upperHall, vip) VALUES (?,?,?,?,?,?,?)', (showtime, screen, movieid[0], date, lowerhall, upperhall, vip))
        conn.commit()
        tkinter.messagebox.showinfo("---- ADDED ----","A new show has been added successfully.", icon="info")

        return 1

    def adminreport(self):
        bookingCur.execute('SELECT movieName FROM Booking')
        movies = bookingCur.fetchall()
        print(movies)

        generate = dict()
        for movie in movies:
            print(movie)
            totalPrice = 0
            bookingCur.execute('SELECT totalPrice FROM Booking WHERE movieName=?', [movie[0]])
            hold = bookingCur.fetchall()
            for i in hold:
                totalPrice += i[0]
            generate[movie[0]] = totalPrice
        topRev = 0
        for x,y in generate.items():
            if y>topRev:
                topRev = y
                toprevFilm = x
            else:
                topRev = topRev
        print(topRev, toprevFilm)

        bookingCur.execute('SELECT totalPrice FROM Booking')
        prices = bookingCur.fetchall()
        
        totalRev = 0
        for price in prices:
            totalRev += price[0]
        
        self.report_frame = Frame(self.master)
        self.report_frame.grid(row=9, column=0, padx=10, pady=10)
        toprevfilm_label = Label(self.report_frame, text=f"Top Revenue Film: {toprevFilm}").grid(row=0, column=0, padx=7, pady=7)
        totalrev_label = Label(self.report_frame, text=f"Total Revenue: {totalRev}").grid(row=1, column=0, padx=7, pady=7)
        return 0

    def movielist(self):
        bookingCur.execute('SELECT * FROM Movie')
        movies = bookingCur.fetchall()

        self.listFrame = Frame(self.master)
        self.listFrame.grid(row=9, column=0, padx=1, pady=1)
        self.movieid_label = Label(self.listFrame, text="Movie ID").grid(row=0, column=0, padx=5, pady=5)
        self.moviename_label = Label(self.listFrame, text="Movie ").grid(row=0, column=1, padx=5, pady=5)
        self.genre_label = Label(self.listFrame, text="Genre ").grid(row=0, column=2, padx=5, pady=5)
        self.rating_label = Label(self.listFrame, text="Rating ").grid(row=0, column=3, padx=5, pady=5)
        self.pg_label = Label(self.listFrame, text="PG ").grid(row=0, column=4, padx=5, pady=5)
        self.description_label = Label(self.listFrame, text="Description ").grid(row=0, column=5, padx=5, pady=5)

        i=1
        for movie in movies:
            self.movieid_view = Label(self.listFrame, text=movie[0]).grid(row=i, column=0, padx=5, pady=5)
            self.moviename_view = Label(self.listFrame, text=movie[1]).grid(row=i, column=1, padx=5, pady=5)
            self.genre_view = Label(self.listFrame, text=movie[2]).grid(row=i, column=2, padx=5, pady=5)
            self.rating_view = Label(self.listFrame, text=movie[3]).grid(row=i, column=3, padx=5, pady=5)
            self.pg_view = Label(self.listFrame, text=movie[4]).grid(row=i, column=0, padx=4, pady=5)
            self.description_view = Label(self.listFrame, text=movie[5]).grid(row=i, column=5, padx=5, pady=5)
            i=i+1

    def addMovie(self):
        self.movie_frame = Frame(self.master)
        self.movie_frame.grid(row=9, column=0, padx=10, pady=10)
        self.movieName = StringVar()
        self.genre = StringVar()
        self.rating = IntVar()
        self.pg = StringVar()
        self.description = StringVar()

        moviename_label = Label(self.movie_frame, text="Enter a movie name : ").grid(row=0, column=0, padx=5, pady=5)
        moviename_entry = Entry(self.movie_frame, textvariable=self.movieName).grid(row=0, column=1, padx=5, pady=5)

        genre_label = Label(self.movie_frame, text="Genre : ").grid(row=1, column=0, padx=5, pady=5)
        genre_entry = Entry(self.movie_frame, textvariable=self.genre).grid(row=1, column=1, padx=5, pady=5)

        rating_label = Label(self.movie_frame, text="Rating : ").grid(row=2, column=0, padx=5, pady=5)
        rating_entry = Spinbox(self.movie_frame, textvariable=self.rating, increment=0.1).grid(row=2, column=1, padx=5, pady=5)
        
        pg_label = Label(self.movie_frame, text="PG : ").grid(row=3, column=0, padx=5, pady=5)
        pg_entry = OptionMenu(self.movie_frame, self.pg, 'Y', 'N').grid(row=3, column=1, padx=5, pady=5)
        
        description_label = Label(self.movie_frame, text="Description : ").grid(row=4, column=0, padx=5, pady=5)
        description_entry = Entry(self.movie_frame, textvariable=self.description).grid(row=4, column=1, padx=5, pady=5)
        
        confirm_button = Button(self.movie_frame, text="Confirm", command=self.confirm).grid(row=5, column=0, padx=5, pady=5)

    def confirm(self):
        if self.controller:
            self.controller.confirmMovie(self.movieName.get(), self.genre.get(), self.rating.get(), self.pg.get(), self.description.get())
    def confirmMovie(self, moviename, genre, rating, pg, description):
        bookingCur.execute('INSERT INTO Movie (movieName, genre, rating, PG, description) VALUES (?,?,?,?,?)', (moviename, genre, rating, pg, description))
        conn.commit()
        tkinter.messagebox.showinfo("---- ADDED ----", "Movie's been added successfully.", icon="info")

        return 1

    def search(self):
        if self.controller:
            #print(self.defdate1.get())
            date =self.defdate1.get()
            self.controller.searchDate(self.__user, date, self.cinema.get())

    def getMovies(self, username, date, cinema):
        user = username
        date = date
        #print(date)
        self.newWindow = Toplevel(self.master)
        model = MovieModel
        view = MovieFrame(self.newWindow, user, date, cinema)
        view.grid(row=0, column=0, padx=5, pady=5)
        controller = movieController(model, view)
        view.setController(controller)
        self.master.withdraw()

        


    def sch(self):
        search_date = self.defdate1.get()
        c2.execute("""SELECT * FROM movies WHERE
                            date = ? ORDER BY time='1pm' DESC,
                                                time='2pm' DESC,
                                                time='3pm' DESC,
                                                time='4pm' DESC,
                                                time='5pm' DESC,
                                                time='6pm' DESC,
                                                time='7pm' DESC,
                                                time='8pm' DESC,
                                                time='9pm' DESC,
                                                time='10pm' DESC """, (search_date,))
        output = c2.fetchall()
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1450x720')
        self.app = SearchResults(self.newWindow, output, search_date)
        self.master.withdraw()

    def Update_Profile_window(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('400x400')
        self.app = Booking_staff_profile(self.newWindow)
        self.master.withdraw()

    def Booking_History_window(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = BookHist(self.newWindow)
        controller = HistController(self.app)
        self.app.setController(controller)
        #self.master.withdraw()

    def logout(self):
        msg = tkinter.messagebox.askyesno('Logout', 'Are you sure you want to log out?')
        if msg:
            #self.newWindow = Toplevel(self.master)
            #self.newWindow.geometry('350x350')
            #self.app = MainPage(self.newWindow)
            self.master.withdraw()

    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'        
        self.username_entry['foreground'] = 'red'
        self.password_entry['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

class BookingController:
    def __init__(self, model):
        self.model = model 

    def searchDate(self, user, date, cinema):
        try:
            self.model.getMovies(user, date, cinema)
        except ValueError as error:
            self.model.show_error(error)

    def confirmMovie(self, moviename, genre, rating, pg, description):
        try:
            self.model.confirmMovie(moviename, genre, rating, pg, description)
        except ValueError as error:
            self.model.show_error(error)

    def addshowing(self, moviename, showtime, screen, date, lowerhall, upperhall, vip):
        try:
            self.model.addshowing(moviename, showtime, screen, date, lowerhall, upperhall, vip)
        except ValueError as error:
            self.model.show_error(error)

    def addCity(self, cityname, mPrice, aPrice, ePrice):
        try:
            self.model.addCity(cityname, mPrice, aPrice, ePrice)
        except ValueError as error:
            self.model.show_error(error)

    def addCinema(self, cinema, city):
        try:
            self.model.Cinema(cinema, city)
        except ValueError as error:
            self.model.show_error(error)





#Search Results page according to date selected on the booking staff home page
class SearchResults(Booking_staff_main):
    def __init__(self, master, output, search_date):
        self.search_date = search_date
        self.master = master
        self.output = output
        self.frame = Frame(self.master)
        self.label = Label(self.master)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)
        self.date = Label(self.master, text='Date', font=("Helvetica", 13), width=8).grid(row=0, column=1, pady='1')
        self.time = Label(self.master, text='Time', font=("Helvetica", 13), width=6).grid(row=0, column=2, pady='1')
        self.title = Label(self.master, text='Title', font=("Helvetica", 13), width=15).grid(row=0, column=3, pady='1')
        self.description = Label(self.master, text='Description', font=("Helvetica", 13), width=30).grid(row=0, column=4, pady='1')
        self.city = Label(self.master, text='City', font=("Helvetica", 13), width=8).grid(row=0, column=5, pady='1')
        self.price = Label(self.master, text='Price', font=("Helvetica", 13), width=8).grid(row=0, column=6, pady='1')
        self.booked = Label(self.master, text='Booked', font=("Helvetica", 13), width=8).grid(row=0, column=7, pady='1')
        self.available = Label(self.master, text='Available', font=("Helvetica", 13), width=8).grid(row=0, column=8, pady='1')
        self.book = Label(self.master, text='Book ticket', font=("Helvetica", 13), width=12).grid(row=0, column=9, pady='1')
        widths = (15, 6, 20, 20, 8, 8, 8, 12)
        for i in self.output:
            for j in i:
                b = Label(self.master, text=j, font=("Helvetica", 11), width=widths[i.index(j)])
                b.grid(row=output.index(i) + 1, column=i.index(j) + 1, pady='1')
            # c2.execute('SELECT booked FROM movies WHERE rowid=?', (output.index(i) + 1,))
            # self.taken = c2.fetchone()[0]  # returns the number of available seats for that movie
            # c2.execute('SELECT date, time FROM movies WHERE date=? AND rowid=?',
            # (self.search_date, output.index(i) + 1,))
            # self.datetime = c2.fetchone()  # returns the date and time of the movie
            
            
            #The variable for bookings in database
            self.taken = i[6]
            #The variable
            self.datetime = (i[0], i[1])
            d = Button(self.master, text='Book', command=partial(self.boo, self.taken, self.datetime), font=("Helvetica", 9))
            d.grid(row=output.index(i) + 1, column=9, pady='1')
        self.back = Button(self.master, font=("Helvetica", 12), text="Back", bg="black", fg="white", command=self.back).grid(row=10, column=1, pady='1')
        self.log = Button(self.master, font=("Helvetica", 12), text="Logout", fg="white", bg='black', command=self.logout).grid(row=10, column=2, pady='1')

    def boo(self, gone, datetime7):
        msg = tkinter.messagebox.askyesno('Book', 'Do you want to confirm this booking?')
        if msg:
            self.gone = gone
            self.datetime = datetime7
            self.usr = username.split('_')
            c3.execute("SELECT * FROM bookings WHERE username = ? AND date = ? AND time = ?", (username, self.datetime[0], self.datetime[1]))
            alr = c3.fetchone()
            if alr:
                tkinter.messagebox.showinfo("---- ERROR ----", "You are already booked into this film", icon="warning")
            elif self.gone == 100:
                tkinter.messagebox.showinfo("---- ERROR ----", "Movie showing full", icon="warning")
            else:
                td_hour = datetime.today().hour - 12
                td_day = date.today().day
                td_month = date.today().month
                td_year = date.today().year
                new_time = int(self.datetime[1][:-2])
                temp_date = self.datetime[0].split()
                new_date = int(temp_date[1][:2])
                # print(new_time, new_date)
                if td_year < 2018:
                    tkinter.messagebox.showinfo("---- ERROR ----", "Date and time of showing has passed!", icon="warning")
                    
                else:
                    with conn2:
                        c2.execute("UPDATE movies SET booked = ?, available = ? WHERE date = ? AND time = ?", (self.gone + 1, 100 - (self.gone + 1), datetime7[0], datetime7[1]))
                    self.newWindow = Toplevel(self.master)
                    self.newWindow.geometry('1096x720')
                    self.app = Booked(self.newWindow, self.datetime)
                    self.master.withdraw()

    def back(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('1096x720')
        self.app = Booking_staff_main(self.newWindow)
        self.master.withdraw()
#This page is used for updating booking staff profile
class Booking_staff_profile(Frame):
    #Allows the customer to update their profile
    def __init__(self, master, user):
        self.master = master
        #self.__user = user
        self.frame = Frame(self.master)
        self.label = Label(self.master)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0)
        self.usr = username.split('_')
        c.execute('SELECT * FROM customers WHERE username = ?', (username,))

        self.title = Label(self.master, text="Please update your details below:", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady='3')
        self.output = c.fetchone()
        
        self.first = Label(self.master, text="First Name:", width='15').grid(row=1, column=0, pady='3')
        self.firstname = Entry(self.master, width='30')
        self.firstname.insert(END, self.output[0])
        self.firstname.grid(row=1, column=1, pady='3')

        self.last = Label(self.master, text="Last Name:", width='15').grid(row=2, column=0, pady='3')
        self.lastname = Entry(self.master, width='30')
        self.lastname.insert(END, self.output[1])
        self.lastname.grid(row=2, column=1, pady='3')

        self.email = Label(self.master, text="Email Address:", width='15').grid(row=3, column=0, pady='3')
        self.emailadd = Entry(self.master, width='30')
        self.emailadd.insert(END, self.output[2])
        self.emailadd.grid(row=3, column=1, pady='3')

        self.ag = Label(self.master, text="Age:", width='15').grid(row=4, column=0, pady='3')
        self.age = Entry(self.master, width='30')
        self.age.insert(END, self.output[3])
        self.age.grid(row=4, column=1, pady='3')

        self.ps1 = Label(self.master, text="Password:", width='15').grid(row=5, column=0, pady='3')
        self.firstpassword = Entry(self.master, width='30', show='*')
        self.firstpassword.insert(END, self.output[5])
        self.firstpassword.grid(row=5, column=1, pady='3')

        self.ps2 = Label(self.master, text="Confirm Password:", width='15').grid(row=6, column=0, pady='3')
        self.secondpassword = Entry(self.master, width='30', show='*')
        self.secondpassword.insert(END, self.output[5])
        self.secondpassword.grid(row=6, column=1, pady='3')
        
        #Button for updating details
        self.update = Button(self.master, text="Update Details", command=self.change).grid(row=7, columnspan=2, pady='3')
        #Button for "Back" which leads back to previous screen
        self.back = Button(self.master, font=("Helvetica", 12), text="Back", fg="white", bg='black', command=self.back).grid(row=8, column=0, pady='3')
        #Button for logging out of the system
        self.log = Button(self.master, font=("Helvetica", 12), text="Logout", fg="white", bg='black', command=self.logout).grid(row=8, column=1, pady='3')

    def change(self):
        msg = tkinter.messagebox.askyesno('Update Profile', 'Confirm changes?')
        if msg:
            new_first = self.firstname.get()
            new_last = self.lastname.get()
            new_email = self.emailadd.get()
            new_age = self.age.get()
            new_firstpassword = self.firstpassword.get()
            new_secondpassword = self.secondpassword.get()
            
            c.execute("""UPDATE customers SET first = ?, last = ?, email = ?, age = ?, password = ? WHERE username = ?""", (new_first, new_last, new_email, new_age, new_firstpassword, username))
            self.newWindow = Toplevel(self.master)
            self.newWindow.geometry('400x400')
            self.app = Booking_staff_main(self.newWindow)
            self.master.withdraw()
            tkinter.messagebox.showinfo("---- SUCCESSFUL ----", "Profile successfully updated.", icon="info")

    def back(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('400x400')
        self.app = Booking_staff_main(self.newWindow)
        self.master.withdraw()
''' 
    def managerback(self):
        self.newWindow = Toplevel(self.master)
        self.newWindow.geometry('400x400')
        self.app = ManagerMain(self.newWindow)
        self.master.withdraw()
'''
    

#The class where booking is done successfully
class Booked(Booking_staff_profile, SearchResults):
    def __init__(self, master, datetime1):
        self.datetime1 = datetime1
        self.master = master
        self.frame = Frame(self.master)
        self.label = Label(self.master)
        self.label.place(x=0, y=0, relwidth=1, relheight=1)
        self.frame.grid(row=0, column=0, pady='1')
        self.usr = username.split('_')   
        c.execute('SELECT * FROM customers WHERE username = ?', (username,))

        self.heading = Label(self.master, text='Booking successful! booking details are below:', width=45, font=("Helvetica", 16)).grid(row=0, columnspan=2, pady='5')

        self.output = c.fetchone()
        self.first = Label(self.master, text="First Name:", width=15).grid(row=1, column=0, pady='3')
        self.firstname = Label(self.master, text=self.output[0], width=30)
        self.firstname.grid(row=1, column=1, pady='3')

        self.last = Label(self.master, text="Last Name:", width=15).grid(row=2, column=0, pady='3')
        self.lastname = Label(self.master, text=self.output[1], width=30)
        self.lastname.grid(row=2, column=1, pady='3')

        self.email = Label(self.master, text="Email Address:", width=15).grid(row=3, column=0, pady='3')
        self.emailadd = Label(self.master, text=self.output[2], width=30)
        self.emailadd.grid(row=3, column=1, pady='3')

        self.ag = Label(self.master, text="Age:", width=15).grid(row=4, column=0, pady='3')
        self.age = Label(self.master, text=self.output[3], width=30)
        self.age.grid(row=4, column=1, pady='3')

        self.da = Label(self.master, text="Date:", width=15).grid(row=5, column=0, pady='3')
        self.date = Label(self.master, text=self.datetime1[0], width=30)
        self.date.grid(row=5, column=1, pady='3')

        self.ti = Label(self.master, text="Time:", width=15).grid(row=6, column=0, pady='3')
        self.time = Label(self.master, text=self.datetime1[1], width=30)
        self.time.grid(row=6, column=1, pady='3')


        c2.execute('''SELECT booked FROM movies WHERE date = ? AND time = ?''', (self.datetime1[0], self.datetime1[1]))

        numb = str(c2.fetchone()[0])
        if len(numb) == 1:
            numb = '0' + str(numb)
        numb0 = int(numb[0])
        numb1 = int(numb[1])
        list_of_rows = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J')

        seat_row = list_of_rows[numb0]
        seat_number = str(seat_row) + str(numb1)

        self.se = Label(self.master, text="Seat Number:", width=15).grid(row=8, column=0, pady='1')
        self.seat = Label(self.master, text=seat_number, width=30)
        self.seat.grid(row=9, column=1, pady='1')
        
        
        #Button for going back
        self.back = Button(self.master, font=("Helvetica", 12), text="Back", fg="white", bg='black', command=self.back).grid(row=10, column=0, pady='1')
        #Button for logging out
        self.log = Button(self.master, font=("Helvetica", 12), text="Logout", fg="white", bg='black', command=self.logout).grid(row=10, column=1, pady='1')

        c.execute('SELECT first, last FROM customers WHERE username = ?', (username,))
        namess = c.fetchall()[0]
        with conn3:
            c3.execute('INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?)', (namess[0], namess[1], self.datetime1[0], self.datetime1[1], seat_number, username))
#This class is where the user could view booking history
class BookHist(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master
        #self.frame = Frame(self.master)
        #self.label = Label(self.master)
        #self.label.place(x=0, y=0, relwidth=1, relheight=1)
        #self.frame.grid(row=0, column=0)
        self.__customerID = StringVar()
        self.controller = None

        self.customer_label = Label(self.master, text='Enter Customer ID : ').grid(row=0, column=0, sticky=W, padx=5, pady=5)
        self.customer_entry = Entry(self.master, textvariable=self.__customerID).grid(row=0, column=1,sticky=E, padx=5, pady=5)
        self.customer_button = Button(self.master, text="Search", command=self.getBooking).grid(row=0, column=3, padx=5, pady=5)
        self.bookingid = None

        '''
        self.date = Label(self.master, text='Date', font=("Helvetica", 16), width='15').grid(row=0, column=0)
        self.time = Label(self.master, text='Time', font=("Helvetica", 16), width='10').grid(row=0, column=1)
        self.title = Label(self.master, text='Title', font=("Helvetica", 16), width='33').grid(row=0, column=2)
        self.seatno = Label(self.master, text='Seat Number', font=("Helvetica", 16), width='15').grid(row=0, column=3)
        self.remove_booking = Label(self.master, text='Remove Booking', font=("Helvetica", 16), width='15').grid(row=0, column=4)

        #The button for going back
        self.back = Button(self.master, font=("Helvetica", 12), text="Back", fg="white", bg='black', command=self.back).grid(row=20, column=0)
        #The button for logging out
        self.log = Button(self.master, font=("Helvetica", 12), text="Logout", fg="white", bg='black', command=self.logout).grid(row=20, column=1)

        '''
        

        
    def setController(self, controller):
        self.controller = controller

    def getBooking(self):
        if self.controller:
            self.controller.bookings(self.__customerID.get())

    def bookingList(self, customerID):
        cur.execute('SELECT * FROM Booking WHERE customerID = ?', [customerID])
        bookings = cur.fetchall()
        if len(bookings)>0:
            self.heading = Label(self.master, text="Bookings", font=("Helvetica", 15)).grid(row=1, column=0, padx=5, pady=5)
            for booking in bookings:
                self.bookingid = booking[0]
                print(self.bookingid)
                self.bookingid_label = Label(self.master, text=f"Booking Reference Number: {booking[0]}").grid(row=2, column=0, padx=5, pady=5)
                self.moviename = Label(self.master, text=f"Movie Name: {booking[1]}").grid(row=3, column=0, padx=5, pady=5)
                self.showtime = Label(self.master, text=f"Show Time: {booking[2]}").grid(row=4, column=0, padx=5, pady=5)
                self.date = Label(self.master, text=f"Date: {booking[4]}").grid(row=5, column=0, padx=5, pady=5)
                self.seatnumber = Label(self.master, text=f"Seat Number: {booking[3]}").grid(row=6, column=0, padx=5, pady=5)
                self.ticket = Label(self.master, text=f"Ticket Type: {booking[5]}").grid(row=7, column=0, padx=5, pady=5)
                self.nooftickets = Label(self.master, text=f"Number of seats booked: {booking[6]}").grid(row=8, column=0, padx=5, pady=5)
                self.price = Label(self.master, text=f"The amount paid: {booking[8]}").grid(row=9, column=0, padx=5, pady=5)
                self.delete_button = Button(self.master, text="Delete this booking", command=self.deletebooking).grid(row=10, column=1, padx=5, pady=5)
        else:
            error = Label(self.master, text="This customer does not have any bookings in place.")
            error.grid(row=11, column=0, padx=5, pady=5)
        print(self.bookingid)

    def deletebooking(self):
        if self.controller:
            self.controller.deletebooking(self.bookingid)

    def remove(self, bookingID):
        #id = bookingID[0]
        msg = tkinter.messagebox.askyesno('Remove', 'Are you sure you want remove this booking?')
        if msg:
            print(id)
            cur.execute('SELECT * FROM Booking WHERE bookingID = ?', [bookingID])
            booking = cur.fetchone()
            print(booking)
            showtime = booking[2]
            showdate = booking[4]
            ticket = booking[5]
            nooftickets = booking[6]
            date = str(showdate)

            '''
            td_hour = datetime.today().hour - 12
            td_day = date.today().day
            td_month = date.today().month
            td_year = date.today().year
            new_time = int(booking[2])
            temp_date = date.split()
            new_date = int(temp_date[1][:2])
            if td_year < 2018 or \
                    td_year == 2018 and td_month > 1 or \
                    td_year == 2018 and td_month == 1 and td_day > new_date or \
                    td_year == 2018 and td_month == 1 and td_day == new_date and td_hour >= new_time:
                tkinter.messagebox.showinfo("---- ERROR ----", "Date and time of showing has passed!", icon="warning")
            else:
            '''
            cur.execute('DELETE FROM Booking WHERE bookingID = ?', [bookingID])
            conn.commit()
            cur.execute('SELECT * FROM Show WHERE showTime = ? AND date=?', (showtime, showdate,))
            show = cur.fetchone()
            if ticket == "lowerHall":
                lowerHall = int(show[4]) + nooftickets
                cur.execute('UPDATE Show SET lowerHall=? WHERE showTime=? AND date=?', (lowerHall, showtime, date,))
                conn.commit()
            elif ticket == "upperHall":
                upperHall = int(show[5]) + nooftickets
                cur.execute('UPDATE Show SET upperHall=? WHERE showTime=? AND date=?', (upperHall, showtime, date,))
                conn.commit()
            else:
                vip = int(show[6]) + nooftickets
                cur.execute('UPDATE Show SET vip=? WHERE showTime=? AND date=?', (vip, showtime, date,))
                conn.commit()
                    
            tkinter.messagebox.showinfo("---- REMOVED ----", "Film removed from booking history.", icon="info")
            self.master.withdraw()
            return 1

                
class HistController:
    def __init__(self,view):
        self.view = view
    
    def bookings(self,customerID):
        try:
            self.view.bookingList(customerID)
        except ValueError as error:
            print('Parameter errors!')

    def deletebooking(self, bookingID):
        try: 
            self.view.remove(bookingID)
        except ValueError as error:
            print('Parameter errors!')