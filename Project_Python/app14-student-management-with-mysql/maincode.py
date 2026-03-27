import sys
import mysql.connector

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit, QPushButton,
    QMainWindow, QTableWidget, QTableWidgetItem, QDialog, QComboBox, QToolBar,
    QStatusBar, QMessageBox
)


# -----------------------------
# Database Connection (MySQL)
# -----------------------------
class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="admin", database="school"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )


# -----------------------------
# Main Window
# -----------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu_item = self.menuBar().addMenu("&File")
        help_menu_item = self.menuBar().addMenu("&Help")
        edit_menu_item = self.menuBar().addMenu("&Edit")

        # Add Student to File
        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu_item.addAction(add_student_action)

        # Add About To Help
        about_action = QAction("About", self)
        help_menu_item.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)
        about_action.triggered.connect(self.about)

        # Add Search to Edit
        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu_item.addAction(search_action)
        search_action.triggered.connect(self.search)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Course", "Mobile"])
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)

        # Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # Status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Detect a cell where you click on (row, column)
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self, row, column):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # Remove old buttons from status bar
        for child in self.findChildren(QPushButton):
            self.statusbar.removeWidget(child)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)

    def load_data(self):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, course, mobile FROM students")
            result = cursor.fetchall()

            self.table.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.table.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            cursor.close()
            connection.close()
        except Exception as e:
            self.show_error(f"Load data failed:\n{e}")

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()

    def about(self):
        dialog = AboutDialog()
        dialog.exec()

    def show_error(self, message: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(message)
        msg.exec()


# -----------------------------
# About Dialog
# -----------------------------
class AboutDialog(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        content = """
This app was created by Long Vibol in the course "The Python Mega Course".
        """.strip()
        self.setText(content)


# -----------------------------
# Edit Dialog
# -----------------------------
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Update Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        index = main_window.table.currentRow()
        if index < 0:
            self._warn("Please select a row first.")
            self.close()
            return

        # Get values from selected row
        self.student_id = main_window.table.item(index, 0).text()
        student_name = main_window.table.item(index, 1).text()
        course_name = main_window.table.item(index, 2).text()
        mobile = main_window.table.item(index, 3).text()

        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit(mobile)
        self.mobile.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile)

        button = QPushButton("Update")
        button.clicked.connect(self.update_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def update_student(self):
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute(
                "UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s",
                (
                    self.student_name.text(),
                    self.course_name.currentText(),
                    self.mobile.text(),
                    self.student_id
                )
            )
            connection.commit()
            cursor.close()
            connection.close()

            main_window.load_data()
            self.close()
        except Exception as e:
            self._error(f"Update failed:\n{e}")

    def _warn(self, text: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(text)
        msg.exec()

    def _error(self, text: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(text)
        msg.exec()


# -----------------------------
# Delete Dialog
# -----------------------------
class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()
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

    def delete_student(self):
        index = main_window.table.currentRow()
        if index < 0:
            self._warn("Please select a row first.")
            return

        student_id = main_window.table.item(index, 0).text()

        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
            connection.commit()
            cursor.close()
            connection.close()

            main_window.load_data()
            self.close()

            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setText("The record was deleted successfully!")
            msg.exec()

        except Exception as e:
            self._error(f"Delete failed:\n{e}")

    def _warn(self, text: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(text)
        msg.exec()

    def _error(self, text: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(text)
        msg.exec()


# -----------------------------
# Insert Dialog
# -----------------------------
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        self.course_name = QComboBox()
        courses = ["Biology", "Math", "Astronomy", "Physics"]
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)

        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("Mobile Number")
        layout.addWidget(self.mobile)

        button = QPushButton("Register")
        button.clicked.connect(self.add_student)
        layout.addWidget(button)

        self.setLayout(layout)

    def add_student(self):
        name = self.student_name.text().strip()
        course = self.course_name.currentText()
        mobile = self.mobile.text().strip()

        if not name:
            self._warn("Name is required.")
            return

        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)",
                (name, course, mobile)
            )
            connection.commit()
            cursor.close()
            connection.close()

            main_window.load_data()
            self.close()
        except Exception as e:
            self._error(f"Insert failed:\n{e}")

    def _warn(self, text: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Warning")
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(text)
        msg.exec()

    def _error(self, text: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(text)
        msg.exec()


# -----------------------------
# Search Dialog
# -----------------------------
class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(160)

        layout = QVBoxLayout()

        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        button = QPushButton("Search")
        button.clicked.connect(self.search_student)
        layout.addWidget(button)

        button2 = QPushButton("Search (Starts with)")
        button2.clicked.connect(self.search_student_startswith)
        layout.addWidget(button2)

        self.setLayout(layout)

    def search_student(self):
        name = self.student_name.text().strip()
        if not name:
            return

        # Highlight in table (client-side)
        main_window.table.clearSelection()
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        # Optional DB query (server-side)
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, course, mobile FROM students WHERE name = %s", (name,))
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            connection.close()
        except Exception as e:
            self._error(f"Search failed:\n{e}")

    def search_student_startswith(self):
        name = self.student_name.text().strip()
        if not name:
            return

        # Highlight rows in the table that start with the search text
        main_window.table.clearSelection()
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchStartsWith)
        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)

        # Optional DB query for matching records (starts-with)
        try:
            connection = DatabaseConnection().connect()
            cursor = connection.cursor()
            cursor.execute("SELECT id, name, course, mobile FROM students WHERE name LIKE %s", (name + "%",))
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            connection.close()
        except Exception as e:
            self._error(f"Search (Starts with) failed:\n{e}")

    def _error(self, text: str):
        msg = QMessageBox(self)
        msg.setWindowTitle("Error")
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setText(text)
        msg.exec()


# -----------------------------
# App start
# -----------------------------
app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
main_window.load_data()
sys.exit(app.exec())
