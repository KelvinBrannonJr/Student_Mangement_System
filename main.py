import sqlite3
import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox

from PyQt6.QtGui import QAction

from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        # Menu items
        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add student menu item and action
        add_student_action = QAction("Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # About menu item and action
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)

        # Edit menu item and action
        search_action = QAction("Search", self)
        search_action.triggered.connect(self.search)
        edit_menu_item.addAction(search_action)

        # QTableWidget attributes
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))

        # To hide default vertical numbers not associated with SQL database
        self.table.verticalHeader().setVisible(False)

        # Set a center layout widget to QTableWidget instance
        self.setCentralWidget(self.table)

    def load_data(self):
        # Connect SQL database
        connection = sqlite3.connect("database.db")
        results = connection.execute("SELECT * FROM students")

        # Initialize table number to 0
        self.table.setRowCount(0)

        # Iterate through row numbers
        for row_number, row_data in enumerate(results):

            # Every index insert a row cell with a row number
            self.table.insertRow(row_number)

            # Iterate through column numbers
            for column_number, column_data in enumerate(row_data):

                # Every index of a row number and column number add column data
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(column_data)))

        # Close the database connection
        connection.close()

    # Insert new data method call
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        search_dialog = SearchDialog()
        search_dialog.exec()


# Dialog for the Insert method
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set Window Attributes
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Add Student Name widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add Course ComboBox widget
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        # Add Mobile Number widget
        self.mobile_number = QLineEdit()
        self.mobile_number.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile_number)

        # Submit button
        submit_btn = QPushButton("Register")
        submit_btn.clicked.connect(self.add_student)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    # Add Student method
    def add_student(self):
        # Reference to field values stored in variables
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        mobile = self.mobile_number.text()

        # Connect to database and create cursor
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # Use the cursor to destructure and INSERT reference variables into related db columns
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))

        # Commit changes and close cursor and db connection
        connection.commit()
        cursor.close()
        connection.close()
        student_management_sys.load_data()


# Search Dialog Attributes
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set Window Attributes
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        search_layout = QVBoxLayout()

        # Search Student Name widget
        self.search_student_name = QLineEdit()
        self.search_student_name.setPlaceholderText("Name")
        search_layout.addWidget(self.search_student_name)

        # Search button
        search_btn = QPushButton("Register")
        search_btn.clicked.connect(self.search_student)
        search_layout.addWidget(search_btn)

        self.setLayout(search_layout)

    # Search Student method
    def search_student(self):
        # Reference to field values stored in variables
        name = self.search_student_name.text()

        # Connect to database and create cursor
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()

        # Select all fields that contained query of student name in database
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name, ))
        rows = list(result)
        print(rows)

        # Select all fields in Main window table and find match of student name
        items = student_management_sys.table.findItems(name, Qt.MatchFlag.MatchFixedString)

        # Highlight all names that match query and print item row to console
        for item in items:
            print(item)
            student_management_sys.table.item(item.row(), 1).setSelected(True)

        # Close cursor and connection to db
        cursor.close()
        connection.close()

app = QApplication(sys.argv)
student_management_sys = MainWindow()
student_management_sys.show()
student_management_sys.load_data()
sys.exit(app.exec())
