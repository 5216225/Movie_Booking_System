import unittest
from home import *
from login import *
from booking import *
from BookingStaff import *
from movies import *

class Testing(unittest.TestCase):
    def test_addingShow(self):
        app = Booking_staff_main
        self.assertTrue(app.addshowing)
    
    def test_addingMovie(self):
        app = Booking_staff_main
        self.assertTrue(app.confirmMovie)
    
    def test_addingCity(self):
        app = Booking_staff_main
        self.assertTrue(app.addCity)

    def test_addingCinema(self):
        app = Booking_staff_main
        self.assertTrue(app.Cinema)

    def test_registerUser(self):
        user = userView
        self.assertTrue(user.signup)

    def test_login(self):
        user = userView
        self.assertTrue(user.login)

    def test_availability(self):
        book = Booking_View
        self.assertTrue(book.checkAvailability)

    def test_booking(self):
        book = Booking_View
        self.assertTrue(book.book)

    def test(self):
        self.assertEqual(Home(),'self induced error so should fail')

    def addCity(self):
        self.assertEqual(1, 0 , 'should fail')

if __name__ == '__main__':
    unittest.main()