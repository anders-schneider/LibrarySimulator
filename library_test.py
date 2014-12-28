import unittest
from library import *

lib = Library()
lib.open()

class CalendarTest(unittest.TestCase):

    def test_calendar(self):
        print "\nCalendar_test"
        cal = Calendar()
        self.assertEqual(0, cal.get_date())
        cal.advance()
        self.assertEqual(1, cal.get_date())

class BookTest(unittest.TestCase):
    
    def setUp(self):
        global book
        book = Book("Contact", "Carl Sagan")
        self.assertTrue(type(book) is Book)

    def test_get_title(self):
        print "\nGet_title_test"
        self.assertEqual("Contact", book.get_title())

    def test_get_author(self):
        print "\nGet_author_test"
        self.assertEqual("Carl Sagan", book.get_author())

    def test_get_due_date(self):
        print "\nGet_due_date_test"
        self.assertEqual(None, book.get_due_date())

    def test_book_check_out_and_check_in(self):
        print "\nCheck_out_Check_in_test"
        book = Book("Contact", "Carl Sagan")
        self.assertEqual(None, book.get_due_date())
        book.check_out(17)
        self.assertEqual(17, book.get_due_date())
        book.check_in()
        self.assertEqual(None, book.get_due_date())

class PatronTest(unittest.TestCase):
    
    def test_patron(self):
        print "\nPatron_test"
        patron = Patron("Amy Gutmann")
        self.assertEqual("Amy Gutmann", patron.get_name())
        self.assertEqual([], patron.get_books())

class LibraryTest(unittest.TestCase):
    
    def setUp(self):
        lib.open()
        lib.response = ''
        lib.patron_being_served = None

    def test_open(self):
        print "\nOpen_test"
        lib.open()
        self.assertEqual(lib.response, "The library is already open!\n")
    
    def test_list_overdue_books(self):
        print "\nList_overdue_books_test"
        lib.list_overdue_books()
        self.assertEqual(lib.response, "No books are overdue.\n")

    def test_issue_card(self):
        print "\nIssue_card_test"
        lib.issue_card("Andy")
        self.assertEqual(lib.response, "Library card issued to Andy.\nNow serving Andy.\nYou currently have these books checked out: \nNo books found.\n")

    def test_serve(self):
        print "\nServe_test"
        lib.serve("Martha")
        self.assertEqual(lib.response, "Martha does not have a library card.\n")
                         
    def test_check_valid_input(self):
        print "\nCheck_valid_input__test"
        books_to_choose = ["book1", "book2"]
        self.assertEqual(lib.check_valid_input((2,), books_to_choose), (True, ''))
        self.assertEqual(lib.check_valid_input(('a',), books_to_choose), (False, 'Please enter only integer numbers.'))

    def test_check_in_and_check_out(self):
        print "\nLib_Check_in_Check_out_test"
        lib.check_in(1,2)
        self.assertEqual(lib.response, "No patron is currently being served.\n")
        lib.response = ''
        lib.check_out(1,2)
        self.assertEqual(lib.response, "No patron is currently being served.\n")

    def test_search(self):
        print "\nSearch_test"
        lib.search("The")
        self.assertEqual(lib.response, "Search string must contain at least four characters.\n")
        lib.response = ''
        lib.read_book_collection()
        lib.search("20,000")
        self.assertEqual(lib.response,"1: 20,000 Leagues Under the Seas, by Jules Verne\n\n")

    def test_create_numbered_list(self):
        print "\nCreate_numbered_list_test"
        items = [Book("Contact", "Carl Sagan")]
        self.assertEqual(lib.create_numbered_list(items), "1: Contact, by Carl Sagan\n")

    def test_close(self):
        print "\nClose_test"
        lib.is_open = True
        lib.close()
        self.assertFalse(lib.is_open)
        self.assertEqual(lib.response, "Goodnight.\n")


unittest.main()
