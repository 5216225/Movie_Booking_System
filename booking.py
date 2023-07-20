import tkinter as tk
from tkinter import *
from datetime import datetime
from db_connect import *
import random
from login import *

conn = getConn()
cur = getCursor()


class Booking:
    def __init__(self, moviename, seatnumber, showID, date, ticketType, noofTickets):
        self.__bookingID = ""
        self.__moviename = moviename
        self.__seatnumber = seatnumber
        self.__showID = showID
        self.__date = date
        self.__ticketType = ticketType
        self.__nooftickets = noofTickets
        self.__availability = ""
    
    def setDate(self, date):
        self.__date = date

    def getDate(self):
        return self.__date

    def getMovie(self):
        return self.__moviename

    def setSeats(self, seatnumber):
        self.__seatnumber = seatnumber

    def getSeats(self):
        return self.__seatnumber
    
    def setShow(self, showID):
        self.__showID = showID
    
    def getShow(self):
        return self.__showID

    def getDate(self):
        return self.__date
    
    def getTicketType(self):
        return self.__ticketType

    def getnoofTickets(self):
        return self.__nooftickets
    
    #fix this
    def getAvailability(self, movieName, date, ticket, showTime):
        cur.execute('SELECT movieID from Movie WHERE movieName = ?', [movieName])
        movieID = cur.fetchone()
        #print(movieID)
        movieID = str(movieID)
        movieID = movieID.strip("(), ")
        cur.execute('SELECT * FROM Show WHERE movieID=? AND showTime=? AND date=?',(movieID, showTime, date,))
        holder = cur.fetchall()
        print(holder)
        if len(holder)>0:
            return 1
        else:
            print('The show is all booked up.')
            return 0
    
    def registerbooking(self, moviename, showtime, date, ticketType, nooftickets, totalPrice, cName):
        seatrows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        row = random.choice(seatrows)
        number = random.randint(1,20)
        seatNo = []
        if nooftickets>1:
            for i in range(nooftickets):
                seat_number = str(row) + str(number)
                seatNo.append(seat_number)
                number = number+1
        else:
            seatNo = str(row) + str(number)
        
        print(seatNo)
        seatNum = ''
        if len(seatNo)>1:
            for seat in seatNo:
                seatNum = seatNum + ' ' + seat
        else:
            seatNum = str(seatNo[0])
        

        
        
        cID = random.randint(10000, 90000)
        cur.execute('SELECT customerID FROM Booking WHERE customerID = ?', [cID])
        id = cur.fetchall()
        if len(id)>0:
            customerID = random.randint(0, 9000)
        else:
            customerID = cID
        
        dob = datetime.today().strftime('%Y-%m-%d')

        
        query = 'INSERT INTO Booking (movieName, showTime, seatNumber, date, ticket_type, noofTickets, customerID, totalPrice, cName, dob) VALUES (?,?,?,?,?,?,?,?,?,?)'
        cur.execute(query,(moviename, showtime, seatNum, date, ticketType, nooftickets, customerID, totalPrice,cName,dob,))
        conn.commit()
        cur.execute('SELECT movieID FROM Movie WHERE movieName=?', [moviename])
        movieID = cur.fetchone()
        movieID = str(movieID)
        movieID = movieID.strip(" (),'' ")
        cur.execute('SELECT lowerHall, upperHall, vip FROM Show WHERE showTime=? AND movieID=? AND date=?', (showtime, movieID, date))
        availability = cur.fetchone()
        print(availability)
        if ticketType == 'lowerHall':
            lowerHall = int(availability[0]) - nooftickets
            cur.execute('UPDATE Show SET lowerHall=? WHERE showTime=? AND movieID=? AND date=?', (lowerHall, showtime, movieID, date,))
            conn.commit()
        elif ticketType == 'upperHall':
            upperHall = int(availability[1]) - nooftickets
            cur.execute('UPDATE Show SET upperHall=? WHERE showTime=? AND movieID=? AND date=?', (upperHall, showtime, movieID, date,))
            conn.commit()
        else:
            vip = int(availability[2]) - nooftickets
            cur.execute('UPDATE Show SET vip=? WHERE showTime=? AND movieID=? AND date=?', (vip, showtime, movieID, date,))
            conn.commit()

        return 1




class Booking_View(tk.Frame):
    def __init__(self, container, user, cinema):
        super().__init__(container)

        self.container = container
        #self.columnconfigure(0, weight=1)
        #self.columnconfigure(1, weight=5)
        self.user = user
        self.cinema = cinema

        self.__date = StringVar()
        self.__moviename = StringVar()
        self.__seatNumber = StringVar()
        self.__showTime = StringVar()
        self.__ticketType = StringVar()
        self.__noofTickets = IntVar()
        self.__availability = StringVar()
        self.__totalPrice = IntVar()
        #c stands for customer
        self.__CName = StringVar() 
        self.__CPhone = StringVar()
        self.__CEmail = StringVar()
        self.__CCard = StringVar()
    

        self.heading = Label(self, text="Horizon Cinemas").grid(column=0, row=0)
        self.border = Frame(self).grid(row=0, column=1, padx=1, pady=1)

        self.user_label = Label(self.border, text=str(self.user)).grid(column=1, row=0, sticky=E)
        self.cinema_label = Label(self.border, text=str(self.cinema)).grid(column=1, row=0, sticky=E)


        
        #cal = DateEntry(self, textvariable)
        #cal.grid(padx=10, pady=10)
        cur.execute('SELECT movieName FROM Movie')
        holder = cur.fetchall()
        movies = []
        for movie in holder:
            movie = str(movie)
            movie = movie.strip("(),'' ")
            movies.append(movie)


        cur.execute('SELECT showTime FROM Show')
        temp = cur.fetchall()
        shows = []
        dates = []
        for item in temp:
            if item not in shows:
                item = str(item)
                item = item.strip("(),'' ")
                shows.append(item)
        shows.sort()
        cur.execute('SELECT date FROM Show')
        holder = cur.fetchall()
        for date in holder:
            date = str(date)
            date = date.strip("(),'' ")
            if date not in dates:
                dates.append(date)
        dates.sort()
        #seats = ["Lower Hall", "Upper Hall", "VIP"]
    
        self.date_label = Label(self, text="Select Date : ")
        self.date_label.grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.date_entry = OptionMenu(self, self.__date, *dates)
        self.date_entry.grid(row=2, column=1, sticky=tk.E, padx=5, pady=5 )

        #turn this into drop down list
        self.movie_label = Label(self, text="Select Film : ")
        self.movie_label.grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.movie_entry = OptionMenu(self, self.__moviename, *movies)
        self.movie_entry.grid(row=3, column=1, sticky=tk.E, padx=5, pady=5)

        self.show_label = Label(self, text="Select Showing : ")
        self.show_label.grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.show_entry = OptionMenu(self, self.__showTime, *shows)
        self.show_entry.grid(row=4, column=1, sticky=tk.E, padx=5, pady=5)
        
        #turn this into choice
        self.ticket_label = Label(self, text="Select Ticket Type : ")
        self.ticket_label.grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.ticket_container=tk.Frame(self).grid(row=5, column=1)
        self.ticket_entry1 = Radiobutton(self, text="Lower Hall", variable=self.__ticketType, value="lowerHall" )
        self.ticket_entry1.grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)
        self.ticket_entry2 = Radiobutton(self, text="Upper Hall", variable=self.__ticketType, value="upperHall" )
        self.ticket_entry2.grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)
        self.ticket_entry3 = Radiobutton(self, text="VIP", variable=self.__ticketType, value="vip" )
        self.ticket_entry3.grid(row=5, column=1, sticky=tk.E, padx=5, pady=5)

        #drop down list
        self.noofticket_label = Label(self, text="Select # of Ticket : ")
        self.noofticket_label.grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.noofticket_entry = OptionMenu(self, self.__noofTickets, '1', '2', '3', '4', '5', '6')
        self.noofticket_entry.grid(row=6, column=1, sticky=tk.E, padx=5, pady=5)
        
        self.ticket_button = Button(self, text="Check Availability and Price", command=self.checkAvailability)
        self.ticket_button.grid(row=7, column=0, padx=5, pady=5)

        self.message_label = Label(self, text='                                    ', foreground='black')
        self.message_label.grid(column=1, row=8, padx=5, pady=5)
        

    def setController(self, controller):
        self.controller = controller

    def checkAvailability(self):
        if self.controller:
            self.controller.checkAvailability(self.__moviename.get(), self.__date.get(), self.__ticketType.get(), self.__showTime.get(), self.cinema, self.__noofTickets.get())

    def getuserdetails(self, movieName, date, ticket, showTime, cinema, nooftickets):
        cur.execute('SELECT movieID from Movie WHERE movieName = ?', [movieName])
        movieID = cur.fetchone()
        movieID = str(movieID)
        movieID = movieID.strip("(), ")

        cur.execute('SELECT * FROM Show WHERE movieID=? AND showTime=? AND date=?', (movieID, showTime, date,))
        holder = cur.fetchone()
        self.__availability = 0
        if ticket == "lowerHall":
            self.__availability = holder[4]
        elif ticket == "upperHall":
            self.__availability = holder[5]
        else:
            self.__availability = holder[6]
        
        cur.execute('SELECT City FROM Cinema where cinemaName=?', [cinema])
        city = cur.fetchone()
        city = str(city)
        city = city.strip("(), ")
        print(city)
        
        cur.execute('SELECT * FROM City WHERE city_name=?', [city])
        prices = cur.fetchone()
        prices = [0, 5, 6, 7]

        print(prices)
        morning = datetime.strptime('12:00', '%H:%M')
        afternoon = datetime.strptime('17:00', '%H:%M')

        time = datetime.strptime(showTime, '%H:%M')
        if time<morning:
            ticketprice = prices[1]
        elif morning<=time<=afternoon:
            ticketprice = prices[2]
        else:
            ticketprice = prices[3]
        
        if ticket == "lowerHall":
            price = ticketprice
        elif ticket == "upperHall":
            price = ticketprice + (ticketprice * 0.2)
        else:
            price = (ticketprice + ticketprice * 0.2) + ((ticketprice + ticketprice * 0.2)*0.2)
        
        print(price)
        total = float(nooftickets) * float(price)
        print(total)
        self.__totalPrice = total

        
        self.availability_label = Label(self, text="Availability : ")
        self.availability_label.grid(row=8, column=0, sticky=tk.W, padx=5, pady=5)
        self.availability = Label(self, text=self.__availability)
        self.availability.grid(row=8, column=1, sticky=tk.E, padx=5, pady=5)

        self.price_label = Label(self, text="Total Price : ")
        self.price_label.grid(row=9, column=0, sticky=tk.W, padx=5, pady=5)
        self.totalPrice = Label(self, text=self.__totalPrice)
        self.totalPrice.grid(row=9, column=1, sticky=tk.E, padx=5, pady=5)
        
        self.cName_label = Label(self, text="Name : ")
        self.cName_label.grid(row=10, column=0, sticky=tk.W, padx=5, pady=5)
        self.cName_entry = Entry(self, text=self.__CName)
        self.cName_entry.grid(row=10, column=1, sticky=tk.E, padx=5, pady=5)

        self.cPhone_label = Label(self, text="Phone : ")
        self.cPhone_label.grid(row=11, column=0, sticky=tk.W, padx=5, pady=5)
        self.cPhone_entry = Entry(self, text=self.__CPhone)
        self.cPhone_entry.grid(row=11, column=1, sticky=tk.E, padx=5, pady=5)

        self.cEmail_label = Label(self, text="Email : ")
        self.cEmail_label.grid(row=12, column=0, sticky=tk.W, padx=5, pady=5)
        self.cEmail_entry = Entry(self, text=self.__CEmail)
        self.cEmail_entry.grid(row=12, column=1, sticky=tk.E, padx=5, pady=5)

        self.card_label = Label(self, text="Card Number : ")
        self.card_label.grid(row=13, column=0, sticky=tk.W, padx=5, pady=5)
        self.card_entry = Entry(self, text=self.__CCard)
        self.card_entry.grid(row=13, column=1, sticky=tk.E, padx=5, pady=5)

        self.expiry_label = Label(self, text="Expiry : ")
        self.expiry_label.grid(row=14, column=0, sticky=tk.W, padx=5, pady=5)
        self.expiry_entry = Entry(self)
        self.expiry_entry.grid(row=14, column=1, sticky=tk.E, padx=5, pady=5)

        self.cvv_label = Label(self, text="CVV : ")
        self.cvv_label.grid(row=15, column=0, sticky=tk.W, padx=5, pady=5)
        self.cvv_entry = Entry(self)
        self.cvv_entry.grid(row=15, column=1, sticky=tk.E, padx=5, pady=5)

        self.main_button = Button(self, text="Main Menu", command=self.main_menu)
        self.main_button.grid(row=16, column=0, sticky=tk.W, padx=5, pady=5)
        self.book_button = Button(self, text="Book Now", command=self.book)
        self.book_button.grid(row=16, column=1, sticky=tk.E, padx=5, pady=5)
        

    def book(self):
        if self.controller:
            self.controller.bookNow(self.__moviename.get(), self.__showTime.get(), self.__date.get(), self.__ticketType.get(), self.__noofTickets.get(), self.__totalPrice, self.__CName.get())
    
    def printReceipt(self, moviename, showtime, date, ticketType, nooftickets, totalPrice, cName):
        self.border = tk.Frame(self, background="black")
        self.border.grid(row=0, column=2, padx=1, pady=1)
        self.frame = tk.Frame(self.border)
        self.frame.grid(padx=1, pady=1)

        self.receipt_heading = Label(self.frame, text="Booking Receipt")
        self.receipt_heading.grid(row=0, column=0, padx=5, pady=5)

        cur.execute('SELECT bookingID, seatNumber, customerID, dob FROM Booking WHERE movieName=? AND showTime=? AND date=? AND cName=?', (moviename, showtime, date, cName,))
        holder = cur.fetchone()
        bookingID = holder[0]
        seatNo = holder[1]
        cID = holder[2]
        dob = holder[3]

        cur.execute('SELECT movieID FROM Movie WHERE movieName=?',[moviename])
        hold = cur.fetchone()
        movieID = hold[0]

        cur.execute('SELECT Screen FROM Show WHERE showTime=? AND movieID=? AND date=?', (showtime, movieID, date))
        temp = cur.fetchone()
        screen = temp[0]

        self.cid_label = Label(self.frame, text=f"Your Customer ID: {cID}")
        self.cid_label.grid(row=0, column=1, sticky=E, padx=5, pady=5)

        self.bookingid_label = Label(self.frame, text=f"Booking Reference Number: {bookingID}")
        self.bookingid_label.grid(row=1, column=0, padx=5, pady=5)

        self.movie_label = Label(self.frame, text=f"for {moviename}")
        self.movie_label.grid(row=1, column=1, padx=5, pady=5)

        self.showtime = Label(self.frame, text=f"Time: {showtime} on {date}")
        self.showtime.grid(row=2, column=0, padx=5, pady=5)
        self.screen  = Label(self.frame, text=f"Screen Number: {screen}")
        self.screen.grid(row=2, column=1, padx=5, pady=5)

        self.seatno_label = Label(self.frame, text=f"Seat Number/s: {seatNo}")
        self.seatno_label.grid(row=3, column=0, padx=5, pady=5)
        self.type = Label(self.frame, text=f"Seat Type: {ticketType}")
        self.type.grid(row=3, column=1, padx=5, pady=5)
        
        self.price = Label(self.frame, text=f"Amount Paid: {totalPrice} for {nooftickets} seat(s).")
        self.price.grid(row=4, column=0, padx=5, pady=5)

        self.bookingDate = Label(self.frame, text=f"Date of Booking: {dob}")
        self.bookingDate.grid(row=4, column=1, padx=5, pady=5)




    def main_menu(self):
        self.newWindow = Toplevel(self.container)
        model = User
        view = userView(self.newWindow)
        view.grid(row=0, column=0, padx = 10, pady = 10)       

        controller = Login_Controller(model, view)

        view.set_controller(controller)
        self.container.withdraw()
    
    def hide_message(self):
        self.message_label['text'] = ''
    
    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'        
        self.message_label.after(3000, self.hide_message)

class Booking_Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def checkAvailability(self, movieName, date, ticket, showTime, cinema, nooftickets):
        try:
            if self.model.getAvailability(self, movieName, date, ticket, showTime):
                self.view.getuserdetails(movieName, date, ticket, showTime, cinema, nooftickets)
            else:
                self.view.show_error('The given movie or time is not available. Please try again.')
        except ValueError as error:
            self.view.show_error('The given movie or time is not available. Please try again.')

    def bookNow(self, moviename, showtime, date, ticketType, nooftickets, totalPrice, cName):
        try:
            if self.model.registerbooking(self,moviename, showtime, date, ticketType, nooftickets, totalPrice, cName):
                self.view.printReceipt(moviename, showtime, date, ticketType, nooftickets, totalPrice, cName)
            else:
                self.view.show_error('Booking cannot be registered!')
        except ValueError as error:
            self.view.show_error()




