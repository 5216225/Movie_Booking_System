from db_connect import *
import tkinter as tk
from tkinter import *
from booking import *
from login import *


conn = getConn()
cur = getCursor()

userConn = sqlite3.connect('customer.db')
userCur = userConn.cursor()

class MovieModel:
    def __init__(self, movieID, moviename, genre, description, pg, rating):
        
        self.__movieID = movieID
        self.__moviename = moviename
        self.__genre = genre
        self.__description = description
        self.__pg = pg
        self.__rating = rating
        
    def getmovieID(self):
        return self.__movieID

    def getMovieName(self):
        return self.__moviename

    def getGenre(self):
        return self.__genre

    def getDescription(self):
        return self.__description

    def getPG(self):
        return self.__pg

    def getRating(self):
        return self.__rating

    #def getMovie(self, moviename, )


class MovieView(tk.Frame):
    def __init__(self, container, movieID, movieName, genre, rating, pg, description, user, date):
        super().__init__(container)

        self.movieID = movieID
        self.container = container
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.user = user
        self.date = date
        self.showtimes = ""

        userCur.execute('SELECT usertype FROM customers WHERE username=?', [self.user])
        hold = userCur.fetchone()
        usertype = hold[0]

        self.border = tk.Frame(self, background="black")
        self.border.grid(row=1, column=0, padx=1, pady=1)
        self.frame = tk.Frame(self.border)
        self.frame.grid(padx=1, pady=1)

        self.movieName = movieName
        self.genre = genre
        self.rating = rating
        self.pg = pg
        self.description = description
        '''
        self.date_label = Label(self, text=str(self.date))
        self.date_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        self.user_label = Label(self, text=str(self.user))
        self.user_label.grid(row=0, column=0, sticky=E, padx=5, pady=5)

        
        '''
        
        
        self.movie_name_label = Label(self.frame, text=str(self.movieName), font=("bold"))
        self.movie_name_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)

        #retrieve this data from db
        self.rating_label = Label(self.frame, text="IMDb Rating: 8.5, Action, Drama, 2022, PG-13, 2h 10m")
        self.rating_label.grid(row=2, sticky=tk.W, column=0, padx=5, pady=5)

        #self.description_label = ttk.Label(self.frame, text="After more than thirty years of service as one of the Navy's top aviators, Pete Mitchell is where he belongs,\n pushing the envelope as a courageous test pilot and dodging the advancement\n in rank that would ground him.")
        self.description_label = Label(self.frame, text=self.description )
        self.description_label.grid(row=3, sticky=tk.W, column=0, padx=5, pady=5)

        self.cast_label = Label(self.frame, text="Cast: Tom Cruise, Jennifer Conelly, Miles Teller")
        self.cast_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)

        self.showings_label = Label(self.frame, text="Showings: ", font=("bold"))
        self.showings_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.show_frame = Frame(self.frame, borderwidth=1)
        self.show_frame.grid(row=6, column=0, padx=10, pady=10)

        cur.execute('SELECT * FROM Show WHERE movieID = ?',[movieID])
        shows = cur.fetchall()
        i=1
        for show in shows:
            showtime = show[0]
            #print(showtime)
            availability = int(show[4]) + int(show[5]) + int(show[6])

            self.shows_label = Label(self.show_frame, text=f"Show {i}", relief=RAISED)
            self.shows_label.grid(row=7, column=i, padx=5, pady=5)

            self.showtime = Label(self.show_frame, text=f"{showtime} [{availability} seats available]")
            self.showtime.grid(row=8, column=i, padx=5, pady=5)
            cur.execute('SELECT bookingID FROM Booking WHERE showTime = ? AND movieName =? AND date=?', (showtime, movieName, date))
            bookings = cur.fetchall()
            if usertype == 'admin':
                self.booking_label = Label(self.show_frame, text=f"Bookings: {len(bookings)}")
                self.booking_label.grid(row=9, column=i, padx=5, pady=5)
                self.delete_button = Button(self.show_frame, text="Delete Show").grid(row=10, column=i, padx=3, pady=3)
                self.update_buttton = Button(self.show_frame, text="Update Show").grid(row=11, column=i, padx=3, pady=3)
            i=i+1

            

    def setController(self, controller):
        self.controller = controller



class MovieFrame(tk.Frame):
    def __init__(self, container, username, date, cinema):
        super().__init__(container)

        self.container = container
        self.username = username
        self.date = date
        self.cinema = cinema
        self.controller = None
        #self.nextdayIndex = None
        #self.previousdayIndex = None

        cur.execute('SELECT * FROM Show WHERE date = ?', [date])
        shows = cur.fetchall()
        movieid = []
        movieID = []
        movies = []
        for show in shows:
            movieid.append(show[2])
        for item in movieid:
            if item not in movieID:
                movieID.append(item)
        for id in movieID:
            cur.execute('SELECT * FROM Movie WHERE movieID = ?', (id,))
            temp = cur.fetchone()
            movies.append(temp)
        
        #frame = Frame(self).grid(row=0, column=0, padx=5, pady=5)
        date_label = Label(self, text=str(date))
        date_label.grid(row=0, column=0, sticky=W, padx=5, pady=5)

        user_label = Label(self, text=str(self.username))
        user_label.grid(row=1, column=0, sticky=E, padx=5, pady=5)

        cinema_label = Label(self, text=str(self.cinema))
        cinema_label.grid(row=0, column=0, sticky=E, padx=5, pady=5)

        i=2
        for movie in movies:
            
            movieID = movie[0]
            movieName = movie[1]
            genre = movie[2]
            rating = movie[3]
            PG = movie[4]
            description = movie[5]
            #model = MovieModel(moviename=movieName, genre=genre, rating=rating, pg=PG, description=description)
            view = MovieView(self, movieID=movieID, movieName=movieName, genre=genre, rating=rating, pg=PG, description=description, user=self.username, date=self.date)
            view.grid(row=i, column=0, padx=10, pady=10)
            i=i+1
        #print(i)
        #footer = Frame(self).grid(row=7, column=0, padx=5, pady=5)
        self.box = Frame(self)
        self.box.grid(row=6, column=0, padx=1, pady=1)

        self.dates = []
        cur.execute('SELECT date FROM Show')
        holder = cur.fetchall()
        for date in holder:
            date = str(date)
            date = date.strip("(),'' ")
            if date not in self.dates:
                self.dates.append(date)
        self.dates.sort()
        index = 0
        for i in self.dates:
            if date == i:
                thisDayIndex = index
            index = index + 1
        self.nextdayIndex = thisDayIndex+1
        self.previousdayIndex = thisDayIndex-1

        self.menu_button = Button(self.box, text="Main Menu", command=self.main).grid(row=0, column=0, padx=3, pady=3)
        self.booking_button = Button(self.box, text="Proceed to Booking", command=self.booking).grid(row=0, column=1, padx=3, pady=3)
        self.nextDay = Button(self.box, text="Next Day", command=self.nextdayButton).grid(row=0, column=2, padx=3, pady=3)
        self.previousDay = Button(self.box, text="Previous Day", command=self.previousButton).grid(row=0, column=3, padx=3, pady=3)

    def setController(self, controller):
        self.controller = controller
    
    def main(self):
        if self.controller:
            self.controller.mainmenu(self.username)
    
    def mainmenu(self):
        self.newWindow = Toplevel(self.container)
        model = User
        view = userView(self.newWindow)
        view.grid(row=0, column=0, padx = 10, pady = 10)       

        controller = Login_Controller(model, view)

        view.set_controller(controller)
        self.container.withdraw()



    def booking(self):
        if self.controller:
            
            self.controller.book(self.username, self.cinema)

    def nextdayButton(self):
        if self.controller:
            self.controller.next(self.username, self.dates[self.nextdayIndex], self.cinema)
    
    def previousButton(self):
        if self.controller:
            self.controller.next(self.username, self.dates[self.previousdayIndex], self.cinema)
    
    def nextdayWindow(self, user, date, cinema):
        self.newWindow = Toplevel(self.container)
        model = MovieModel
        view = MovieFrame(self.newWindow, user, date, cinema)
        view.grid(row=0, column=0, padx=5, pady=5)
        controller = movieController(model, view)
        view.setController(controller)
        self.master.withdraw()


    def bookingWindow(self, user, cinema):
        self.newWindow = Toplevel(self.container)
        model = Booking
        view = Booking_View(self.newWindow, user, cinema)
        view.grid(row=0, column=0, padx = 10, pady = 10)
        controller = Booking_Controller(model, view)
        view.setController(controller)
        self.container.withdraw()

        
class movieController:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def book(self, username, cinema):
        self.view.bookingWindow(username, cinema)

    def next(self, username, date, cinema):
        self.view.nextdayWindow(username, date, cinema)
    
    def mainmenu(self, username):
        self.view.mainmenu(username)


    

    #def getMovie(self)
        
        





'''
class movieApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('List of Movies showing')
        #self.geometry("1000x800")
        #self.resizable(0,0)
        self.config(bg='#F25252')
        border = tk.Frame(self)
        border.pack()
        
        frame = tk.Text(border)
        frame.grid(row=0, column=0)
        v = tk.Scrollbar(border, orient='vertical')
        v.grid(row=0, column=1)
        #v = tk.Scrollbar(frame, orient='vertical')
        #v.bind()
        frame.config(yscrollcommand=v.set)
        v.config(command=frame.yview)

        # create a model
        cur.execute('SELECT * FROM Movie')
        movies = cur.fetchall()
        i=0
        for movie in movies:
            
            movieName = movie[1]
            genre = movie[2]
            rating = movie[3]
            PG = movie[4]
            description = movie[5]
            model = MovieModel(moviename=movieName, genre=genre, rating=rating, pg=PG, description=description)
            view = MovieView(border, movieName=movieName, genre=genre, rating=rating, pg=PG, description=description)
            view.grid(row=i, column=0, padx=10, pady=10)
            frame.insert(tk.END, view)
            i=i+1
        # create a view and place it on the root window
        #view = MovieView(self)
        #view.grid(row=0, column=0, padx=10, pady=10)

        # create a controller
        controller = movieController(model, view)
        #view.config(yscrollcommand=h.set)
        #h.config(command=view.yview)

        # set the controller to view
        view.setController(controller)


if __name__ == '__main__':
    app = movieApp()
    app.mainloop()  

        

'''


