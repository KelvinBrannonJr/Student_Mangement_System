import sqlite3
import sys

from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QGridLayout, \
    QLineEdit, QPushButton, QMainWindow, QTableWidget, QTableWidgetItem, QDialog, \
    QVBoxLayout, QComboBox, QToolBar, QStatusBar, QMessageBox

from PyQt6.QtGui import QAction, QIcon

from PyQt6.QtCore import Qt


# Database connection class
class DatabaseConnection:
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        # Establish connection to database and create cursor
        connection = sqlite3.connect(self.database_file)
        cursor = connection.cursor()

        # return connection and cursor, destructure variables in creation of instances
        return connection, cursor

    def close_connection(self, connection, cursor):

        # Commit changes to db and close connections, refresh app table
        return connection.commit(), cursor.close(), connection.close(), student_management_sys.load_data()


# App Main Window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(600, 400)

        # Menu items
        file_menu_item = self.menuBar().addMenu("&File")
        utility_menu_item = self.menuBar().addMenu("&Utility")
        help_menu_item = self.menuBar().addMenu("&Help")

        # Add student menu item and action with toolbar icon binding to action
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # About menu item and action
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.triggered.connect(self.about)

        # SEARCH item and action with toolbar icon binding to action
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        search_action.triggered.connect(self.search)
        utility_menu_item.addAction(search_action)

        # Toolbar widget and elements, toolbar is also movable
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Statusbar widget and elements
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # QTableWidget attributes
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("Id", "Name", "Course", "Mobile"))

        # To hide default vertical numbers not associated with SQL database
        self.table.verticalHeader().setVisible(False)

        # Detect if cell is clicked
        self.table.cellClicked.connect(self.cell_clicked)

        # Set a center layout widget to QTableWidget instance
        self.setCentralWidget(self.table)

    # Cell clicked method
    def cell_clicked(self):
        # Edit button
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        # Delete button
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # Find children of statusbar widgets and remove appending children
        # Prevent duplications of widgets for every cell click
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)

        # Add widgets after cell is clicked
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    # Load SQL Database data in PyQt
    def load_data(self):
        # Connect SQL database
        connection, cursor = DatabaseConnection().connect()
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

    def edit(self):
        edit_dialog = EditDialog()
        edit_dialog.exec()

    def delete(self):
        delete_dialog = DeleteDialog()
        delete_dialog.exec()

    def about(self):
        about_dialog = AboutDialog()
        about_dialog.exec()


# Dialog Attributes for Insert
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
        connection, cursor = DatabaseConnection().connect()

        # Use the cursor to destructure and INSERT reference variables into related db columns
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (?, ?, ?)",
                       (name, course, mobile))

        # Commit changes, Close connection to database and cursor
        DatabaseConnection().close_connection(connection, cursor)

        # Close window after entry
        self.close()


# Dialog Attributes for Search
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
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.search_student)
        search_layout.addWidget(search_btn)

        self.setLayout(search_layout)

    # Search Student method
    def search_student(self):
        # Reference to field values stored in variables
        name = self.search_student_name.text()

        # Connect to database and create cursor
        connection, cursor = DatabaseConnection().connect()

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

        # Close dialog after search
        self.close()


# Dialog Attributes for Edit
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set Window Attributes
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        # Get table row and column of student to edit
        index = student_management_sys.table.currentRow()

        # Get ID from selected Row
        self.student_id = student_management_sys.table.item(index, 0).text()

        # Get student name
        student_name = student_management_sys.table.item(index, 1).text()

        # Get Course name
        course_name = student_management_sys.table.item(index, 2).text()

        # Get Mobile number
        mobile_number = student_management_sys.table.item(index, 3).text()

        # Add Student Name widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Add Course ComboBox widget
        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        # Add Mobile Number widget
        self.mobile_number = QLineEdit(mobile_number)
        self.mobile_number.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile_number)

        # Submit button
        submit_btn = QPushButton("Update")
        submit_btn.clicked.connect(self.update_student)
        layout.addWidget(submit_btn)

        self.setLayout(layout)

    # Update method
    def update_student(self):
        connection, cursor = DatabaseConnection().connect()

        # Destructure table rows and UPDATE with new values from references in edit fields
        cursor.execute("UPDATE students SET name = ?, course = ?, mobile = ? WHERE id = ?",
                       (self.student_name.text(),
                        self.course_name.itemText(self.course_name.currentIndex()),
                        self.mobile_number.text(), self.student_id))

        # Commit changes, Close connection to database and cursor
        DatabaseConnection().close_connection(connection, cursor)

        # Close dialog after update
        self.close()


# Dialog Attributes for Delete
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()

        # Set Window Attributes
        self.setWindowTitle("Delete Student Data")

        layout = QGridLayout()
        confirmation = QLabel("Are you sure you want to delete?")
        yes = QPushButton("Yes")
        no = QPushButton("No")

        layout.addWidget(confirmation, 0, 0, 1, 2)
        layout.addWidget(yes, 1, 0)
        layout.addWidget(no, 1, 1)
        self.setLayout(layout)

        yes.clicked.connect(self.delete_student)
        no.clicked.connect(self.close)

    # Delete Method
    def delete_student(self):
        # Connect to database
        connection, cursor = DatabaseConnection().connect()

        # Get table row and column of student to edit
        index = student_management_sys.table.currentRow()

        # Get ID from selected Row
        student_id = student_management_sys.table.item(index, 0).text()

        # Execute SQL DELETE query using student ID
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id, ))

        # Commit changes, Close connection to database and cursor
        DatabaseConnection().close_connection(connection, cursor)

        # Create a message box to relay deletion was successful
        confirmation_widget = QMessageBox()
        confirmation_widget.setWindowTitle("Success")
        confirmation_widget.setText("The Record Deleted Successfully!")
        confirmation_widget.exec()

        # Close delete dialog window
        self.close()


# About Inheriting from 'QMessageBox' simple child version of a QDialog
class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        # Content for about section
        content = "I built this academic management app as I learned PyQt6 and it's component libraries. " \
                  "I used object oriented architecture to keep my code organized and scalable." \
                  " A SQL database was used store records and 'CRUD' methods were used to managed it's contents."

        # Use set text to content
        self.setText(content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    student_management_sys = MainWindow()
    student_management_sys.show()
    student_management_sys.load_data()
    sys.exit(app.exec())
