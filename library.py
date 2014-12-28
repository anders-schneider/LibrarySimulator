# Classes and methods for a simple library program
# Authors: Dave Matuszek, Anders Schneider and Martha Trevino
#--------------------------------------------------------------

import sys

class Calendar(object):
    """Keeps track of the durrent date (as an integer)."""
    
    def __init__(self):
        """Creates the initial calendar."""
        self.day = 0

    def get_date(self):
        """Returns (as a positive integer) the current date."""
        return self.day

    def advance(self):
        """Advances this calendar to the next date."""
        self.day += 1

#--------------------------------------------------------------
book_id = 1
class Book(object):
    """Represents one copy of a book. There may be many copies
       of a book with the same title and author.
       Each book has:
         * An id (a unique integer)
         * A title
         * An author (one string, even if many authors)
         * A due date (or None if the book is not checked out.)."""

    def __init__(self, title, author):
        """Creates a book, not checked out to anyone."""
        global book_id
        self.id = book_id
        book_id += 1
        self.title = title
        self.author = author

    def get_id(self):
        """Returns the id of this book."""
        return self.id

    def get_title(self):
        """Returns the title of this book."""
        return self.title

    def get_author(self):
        """Returns the author(s) of this book, as a single string."""
        return self.author

    def get_due_date(self):
        """If this book is checked out, returns the date on
           which it is due, else returns None."""
        try:
            return self.due_date
        except AttributeError:
            return None

    def check_out(self, due_date):
        """Sets the due date for this book."""
        self.due_date = due_date

    def check_in(self):
        """Clears the due date for this book (sets it to None)."""
        self.due_date = None

    def __str__(self):
        """Returns a string representation of this book,
        of the form: title, by author"""
        return self.title + ', by ' + self.author

    def __eq__(self, other):
        """Tests if this book equals the given parameter. Not
        required by assignment, but fairly important."""
        return self.title == other.title and self.author == other.author

#--------------------------------------------------------------

class Patron(object):
    """Represents a patron of the library. A patron has:
         * A name
         * A set of books checked out"""

    def __init__(self, name):
        """Constructs a new patron, with no books checked out yet."""
        self.name = name
        self.book_list = []

    def get_name(self):
        """Returns this patron's name."""
        return self.name

    def get_books(self):
        """Returns the set of books checked out to this patron."""
        return self.book_list

    def take(self, book):
        """Adds a book to the set of books checked out to this patron."""
        self.book_list.append(book)

    def give_back(self, book):
        """Removes a book from the set of books checked out to this patron."""
        self.book_list.remove(book)

    def __str__(self):
        """Returns the name of this patron."""
        return self.name

#--------------------------------------------------------------
    
class OverdueNotice(object):
    """Represents a message that will be sent to a patron."""

    def __init__(self, set_of_books):
        """Takes note of all the books checked out to some patron."""
        self.set_of_books = set_of_books

    def __str__(self):
        """From a set of books, returns a multi-line string giving
           the dates on which the books were or will be due.
           This should only be called when at least one of the books
           is overdue, but ALL the patron's books are listed, with
           their due dates, and the overdue ones specially marked."""

        string = ''
        for book in self.set_of_books:
            string += str(book) + ", DUE DATE: day " + str(book.get_due_date())

            if book.get_due_date() - calendar.get_date() < 0:
                string += " (**OVERDUE**)"

            string += "\n"

        return string
        

#--------------------------------------------------------------

class Library(object):
    """Provides operations available to the librarian."""
    
    def __init__(self):
        """Constructs a library, which involves reading in a
           list of books that are in this library's collection."""
        
        # Create a global calendar, to be used by many classes
        global calendar
        calendar = Calendar()
        
        # Initialize some instance variables for _this_ library
        self.is_open = False            # Is library open?
        self.collection = []            # List of all Books
        self.patrons = {}               # Set of all Patrons
        self.patron_being_served = None # Current patron
        self.response = ''              # Accumulated messages to print
        
    def read_book_collection(self):
        """Read in the book collection."""
        file = open('collection.txt')
        for line in file:
            if len(line) > 1:
                tuple = eval(line.strip())
                self.collection.append(Book(tuple[0], tuple[1]))
        file.close()

    def open(self):
        """Opens this library for business at the start of a new day."""
        if self.is_open:
            self.talk("The library is already open!")
        else:
            self.is_open = True
            calendar.advance()
            self.talk("Today is day " + str(calendar.get_date()) + ".")

    def list_overdue_books(self):
        """Returns a nicely formatted, multiline string, listing the names
           of patrons who have overdue books, and for each such patron, the
           books that are overdue. Or, it returns the string "No books are
           overdue."""
        if self.is_open:
            if self.patrons:
                for patron in self.patrons:
                    book_list = self.patrons[patron].get_books()

                    over_due_books = False
                    for book in book_list:
                        if book.get_due_date() - calendar.get_date() < 0:
                            over_due_books = True
                            break

                    if over_due_books:
                        overdue_notice = OverdueNotice(book_list)
                        self.talk("Dear " + str(patron) + ",\nYou have the following books:")
                        self.talk(str(overdue_notice))
                    else:
                        self.talk("No books are overdue.")
            else:
                self.talk("No books are overdue.")
        else:
            self.talk("The library is not open.")
                
    def issue_card(self, name_of_patron):
        """Allows the named person the use of this library. For
           convenience, immediately begins serving the new patron."""
        if self.is_open:
            if name_of_patron in self.patrons:
                self.talk(name_of_patron + " already has a library card.")
            else:
                self.patrons.update({name_of_patron : Patron(name_of_patron)})
                self.talk("Library card issued to " + name_of_patron + ".")
            self.serve(name_of_patron)
        else:
            self.talk("The library is not open.")

    def serve(self, name_of_patron):
        """Saves the given patron in an instance variable. Subsequent
           check_in and check_out operations will refer to this patron,
           so that the patron's name need not be entered many times."""

        if self.is_open: 
            if name_of_patron in self.patrons:
                self.patron_being_served = self.patrons[name_of_patron]
                self.talk("Now serving " + name_of_patron + ".")
                self.patron_books = self.patron_being_served.get_books()
                self.found_books = []

                books_string = 'You currently have these books checked out: \n'

                books_string += self.create_numbered_list(self.patron_books)
                
                self.talk(books_string)
                    
            else:
                self.talk(name_of_patron + " does not have a library card.")
        else:
            self.talk("The library is not open.")

    def check_valid_input(self, book_numbers, books_to_choose):
        """Checks if the book numbers that the user enters, to check in
           or out books, are valid."""
        for num in book_numbers:
            if type(num) != int:
                return False, "Please enter only integer numbers."
            elif num < 1 or num > len(books_to_choose) or num > 10:
                return False, "One of the numbers you entered does not match a book on the list. Try again."
        return True, ''

    def check_in(self, *book_numbers):
        """Accepts books being returned by the patron being served,
           and puts them back "on the shelf"."""
        if self.is_open and self.patron_being_served:
            (valid_input, message) = self.check_valid_input(book_numbers, self.patron_books)
            if valid_input:
                copy_patron_books = list(self.patron_books)
                for num in book_numbers:
                    this_book = copy_patron_books[num - 1]
                    this_book.check_in()
                    self.patron_being_served.give_back(this_book)
                    self.talk(this_book.get_title() + " returned to shelves.")
            else:
                self.talk(message)
        elif not self.is_open:
            self.talk("The library is not open.")
        elif not self.patron_being_served:
            self.talk("No patron is currently being served.")

    def search(self, string):
        """Looks for books with the given string in either the
           title or the author's name, and creates a globally
           available numbered list in self.found_books."""
        if len(string) >= 4:
            self.found_books = []
            for book in self.collection:
                if string.lower() in book.get_title().lower() or string.lower() in book.get_author().lower():
                    if not book.get_due_date() and (not self.found_books
                                                    or not book == self.found_books[-1]):
                        self.found_books.append(book)

            numbered_found_books = self.create_numbered_list(self.found_books)
            self.talk(numbered_found_books)
        else:
            self.talk("Search string must contain at least four characters.")

    def create_numbered_list(self, items):
        """Creates and returns a numbered list of the given items,
           as a multiline string. Returns "Nothing found." if the
           list of items is empty."""
        length = len(items)
        numbered_list_str = ''
        i = 1
        if items:
            if length <= 10:
                for book in items:
                    numbered_list_str += str(i) + ": " + str(book) 
                    i += 1
                    if not book.get_due_date():
                        numbered_list_str += "\n"
                    elif book.get_due_date() == calendar.get_date():
                        numbered_list_str += " (due today!)\n"
                    elif book.get_due_date() - calendar.get_date() < 0:
                        numbered_list_str += " (**OVERDUE**)\n"
                    else:
                        numbered_list_str += " (due on day " + str(book.get_due_date()) + ")\n"
                return numbered_list_str
            else:
                for book in items[0:10]:
                    numbered_list_str += str(i) + ": " + str(book) + "\n"
                    i += 1
                numbered_list_str += "...and " + str(length - 10) + " more."
                return numbered_list_str
        else:
            return "No books found."
                
    def check_out(self, *book_numbers):
        """Checks books out to the patron currently being served.
           Books will be due seven days from "today".
           Patron must have a library card, and may have not more
           than three books checked out at a time."""

        if self.is_open and self.patron_being_served:
            if self.found_books:
                (valid_input, message) = self.check_valid_input(book_numbers, self.found_books)
                if valid_input:
                    if len(self.patron_being_served.get_books()) + len(book_numbers) > 3:
                        self.talk("Sorry, " + str(self.patron_being_served) + " already has 3 books checked out.")

                    else:
                        for num in book_numbers:
                            this_book = self.found_books[num - 1]
                            this_book.check_out(calendar.get_date() + 7)
                            self.patron_being_served.take(this_book)
                            self.talk(this_book.get_title() + ", checked out to " + str(self.patron_being_served) + ".")
                else:
                   self.talk(message)
            else:
                self.talk("Please search for books before trying to check a book out.")
        elif not self.is_open:
            self.talk("The library is not open.")
        elif not self.patron_being_served:
            self.talk("No patron is currently being served.")
            

    def close(self):
        """Closes the library for the day."""
        if self.is_open:
            self.is_open = False
            self.patron_being_served = None
            self.found_books = []
            self.talk("Goodnight.")
        else:
            self.talk("The library is not open.")

    def quit(self):
        pass

    def help(self):
        self.talk("""
help()
     Repeat this list of commands.
open()
     Opens the library for business; do this once each morning.
     
list_overdue_books()
     Prints out information about books due yesterday.
     
issue_card("name_of_patron")
     Allows the named person the use of the library.
     
serve("name_of_patron")
     Sets this patron to be the current patron being served.
     
search("string")
     Searches for any book or author containing this string
     and displays a numbered list of results.
     
check_out(books...)
     Checks out books (by number) to the current patron.
     
check_in(books...)
     Accepts returned books (by number) from the current patron.
     
close()
     Closes the library at the end of the day.

quit()
     Closes the library for good. Hope you never have to use this!""")

    # ----- Assorted helper methods (of Library) -----

    def talk(self, message):
        """Accumulates messages for later printing. A newline is
           appended after each message."""
        self.response += message + '\n'

    # Feel free to add any more helper methods you would like

#--------------------------------------------------------------

def main():
    library = Library()
    library.read_book_collection()
    print len(library.collection), 'books in collection.'
    print "Ready for input. Type 'help()' for a list of commands.\n"
    command = '\0'
    while command != 'quit()':
        try:
            command = raw_input('Library command: ').strip()
            if len(command) == 0:
                print "What? Speak up!\n"
            else:
                eval('library.' + command)
                print library.response
                library.response = ''
        except AttributeError, e:
            print "Sorry, I didn't understand:", command
            print "Type 'help()' for a list of the things I do understand.\n"
        except RuntimeError, e:
            print e
        except Exception, e:
            print "Unexpected error:", e
    print "The library is now closed for renovations."
    
if __name__ == '__main__':
    main()
