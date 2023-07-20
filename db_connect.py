import sqlite3 
from random import randrange
from tkinter import *


conn = sqlite3.connect('mainDB.db')

cur = conn.cursor()

def getCursor():
    return cur

def getConn():
    return conn

def Customer_Database_Initialiser():
    '''Initialises the database for customers'''
    global conn
    conn = sqlite3.connect('customer.db')
    global c
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS customers(
                first text,
                last text,
                email text,
                age integer,
                username text,
                password text
                )''')

    def create():
        cust = iter([line.rstrip('\n') for line in open('customers.txt', 'r')])
        for i in cust:
            j = i.split(': ')
            k = j[0].split('_')
            c.execute('INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?)',
                      (k[0], k[1], str(j[0] + '@simpsons.com'), randrange(10, 60), j[0], j[1]))

    # create() # Uncomment this line if you want to create the databases again from scratch
    conn.commit()

def Films_Database_Initialiser():
    '''Initialises the database for the film showings'''
    global conn2
    conn2 = sqlite3.connect('movies.db')
    global c2
    c2 = conn2.cursor()
    c2.execute('''CREATE TABLE IF NOT EXISTS movies(date text, time text,
                title text,
                description text,
                booked integer,
                available integer
                )''')

    def create():
        mov = iter([line.rstrip('\n') for line in open('MOVIES.txt', 'r')])
        for i in mov:
            j = i.split(': ')
            c2.execute('INSERT INTO movies VALUES (?, ?, ?, ?, ?, ?)', (j[0], j[1], j[4], j[5], j[2], j[3]))

    # create() # Uncomment this line if you want to create the databases again from scratch
    conn2.commit()

def Bookings_Database_Initialiser():
    '''Initlaises the database for film bookings'''
    global conn3
    conn3 = sqlite3.connect('bookings.db')
    global c3
    c3 = conn3.cursor()
    c3.execute('''CREATE TABLE IF NOT EXISTS bookings(first text, last text, date text, time text, seatno text, username text)''')
    conn3.commit()
