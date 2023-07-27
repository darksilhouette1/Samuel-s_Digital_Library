from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
import MySQLdb

from PyQt5.uic import loadUiType

ui,_ = loadUiType('mylibrary.ui')

class MainApp(QMainWindow ,ui):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.Handel_UI_Changes()
        self.Handel_Button()

        self.Show_Author()
        self.Show_Category()
        self.Show_Publisher()

        self.Show_Category_Combobox()
        self.Show_Author_Combobox()
        self.Show_Publisher_Combobox()


    def Handel_UI_Changes(self):
        self.Hiding_Themes()
        self.tabWidget.tabBar().setVisible(False)

    def Handel_Button(self):
        self.pushButton_3.clicked.connect(self.Show_Themes)
        self.pushButton_15.clicked.connect(self.Hiding_Themes)

        self.pushButton.clicked.connect(self.Open_Books_Tab)
        self.pushButton_2.clicked.connect(self.Open_Settings_Tab)

        self.pushButton_4.clicked.connect(self.Add_New_Book)
        self.pushButton_6.clicked.connect(self.Search_Books)
        self.pushButton_5.clicked.connect(self.Edit_Books)
        self.pushButton_7.clicked.connect(self.Delete_Books)

        self.pushButton_8.clicked.connect(self.Add_Category)
        self.pushButton_9.clicked.connect(self.Add_Author)
        self.pushButton_10.clicked.connect(self.Add_Publishser)


    def Show_Themes(self):
        self.groupBox.show()

    def Hiding_Themes(self):
        self.groupBox.hide()

        ######################
        #####opening_tabs#####


    def Open_Books_Tab(self):
        self.tabWidget.setCurrentIndex(0)

    def Open_Settings_Tab(self):
        self.tabWidget.setCurrentIndex(1)


        ######################
        #####Books#####

    def Add_New_Book(self):
        self.db = MySQLdb.connect(host='localhost', user ='root' , password ='123456', db ='library' )
        self.cur = self.db.cursor()

        book_title = self.lineEdit_2.text()
        book_description = self.textEdit.toPlainText()
        book_code = self.lineEdit.text()
        book_category = self.comboBox.currentIndex()
        book_author = self.comboBox_2.currentIndex()
        book_publisher = self.comboBox_3.currentIndex()
        book_price = self.lineEdit_3.text()

        self.cur.execute('''
            INSERT INTO book (book_name, book_description, book_code, book_category, book_author, book_publisher, book_price)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        ''' ,(book_title, book_description, book_code,book_category, book_author, book_publisher, book_price))

        self.db.commit()
        self.statusBar().showMessage('New Book Added')

        self.lineEdit_2.setText('')
        self.textEdit.setPlainText('')
        self.lineEdit.setText('')
        self.comboBox.setCurrentIndex(0)
        self.comboBox_2.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(0)
        self.lineEdit_3.setText('')


    def Search_Books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_7.text()

        sql = '''SELECT * FROM book WHERE book_name = %s'''
        self.cur.execute(sql , [(book_title)])

        data = self.cur.fetchone()

        print(data)
        self.lineEdit_6.setText(data[1])
        self.textEdit_2.setPlainText(data[2])
        self.lineEdit_4.setText(data[3])
        self.comboBox_5.setCurrentIndex(data[4])
        self.comboBox_6.setCurrentIndex(data[5])
        self.comboBox_4.setCurrentIndex(data[6])
        self.lineEdit_5.setText(str(data[7]))


    def Edit_Books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_6.text()
        book_description = self.textEdit_2.toPlainText()
        book_code = self.lineEdit_4.text()
        book_category = self.comboBox_5.currentIndex()
        book_author = self.comboBox_6.currentIndex()
        book_publisher = self.comboBox_4.currentIndex()
        book_price = self.lineEdit_5.text()

        search_book_title = self.lineEdit_7.text()

        self.cur.execute('''
            UPDATE book SET book_name=%s,book_description=%s,book_code=%s,book_category=%s,book_author=%s,book_publisher=%s,book_price=%s WHERE book_name = %s                            
        ''', (book_title,book_description,book_code,book_category,book_author,book_publisher,book_price, search_book_title))

        self.db.commit()
        self.statusBar().showMessage('book updated')

    def Delete_Books(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        book_title = self.lineEdit_7.text()


        warning = QMessageBox.warning(self, 'Delete Book', "are you sure you want to delete this book", QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
            sql = '''DELETE FROM book WHERE book_name = %s '''
            self.cur.execute(sql, [(book_title)])
            self.db.commit()
            self.statusBar().showMessage('Book Deleted')


    ################################################
    ###################settings#####################

    def Add_Category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db ='library')
        self.cur = self.db.cursor()

        category_name = self.lineEdit_8.text()

        self.cur.execute('''
            INSERT INTO category (category_name) VALUES (%s)
        ''' , (category_name,))

        self.db.commit()
        self.statusBar().showMessage('New Category Added')
        self.lineEdit_8.setText('')
        self.Show_Category()
        self.Show_Category_Combobox()


    def Show_Category(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()


        if data:
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row, form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget.setItem(row, column , QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)




    def Add_Author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        author_name = self.lineEdit_9.text()

        self.cur.execute('''
            INSERT INTO authors (author_name) VALUES (%s)
        ''', (author_name,))
        self.lineEdit_9.setText('')
        self.db.commit()
        self.statusBar().showMessage('New Author Added')
        self.Show_Author()
        self.Show_Author_Combobox()

    def Show_Author(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT author_name FROM authors''')
        data = self.cur.fetchall()


        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)

    def Add_Publishser(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        publisher_name = self.lineEdit_10.text()

        self.cur.execute('''
            INSERT INTO publisher (publisher_name) VALUES (%s)
        ''', (publisher_name,))
        self.lineEdit_10.setText('')
        self.db.commit()
        self.statusBar().showMessage('New Publisher Added')
        self.Show_Publisher()
        self.Show_Publisher_Combobox()

    def Show_Publisher(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()


        if data:
            self.tableWidget_3.setRowCount(0)
            self.tableWidget_3.insertRow(0)
            for row, form in enumerate(data):
                for column, item in enumerate(form):
                    self.tableWidget_3.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget_3.rowCount()
                self.tableWidget_3.insertRow(row_position)

    ###############################################################
    ###################show settings data in ui#####################

    def Show_Category_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT category_name FROM category''')
        data = self.cur.fetchall()

        self.comboBox.clear()
        for category in data:
            self.comboBox.addItem(category[0])
            self.comboBox_5.addItem(category[0])


    def Show_Author_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT author_name FROM authors''')
        data = self.cur.fetchall()

        self.comboBox_2.clear()
        for author in data:
            self.comboBox_2.addItem(author[0])
            self.comboBox_6.addItem(author[0])

    def Show_Publisher_Combobox(self):
        self.db = MySQLdb.connect(host='localhost', user='root', password='123456', db='library')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT publisher_name FROM publisher''')
        data = self.cur.fetchall()

        self.comboBox_3.clear()
        for publisher in data:
            self.comboBox_3.addItem(publisher[0])
            self.comboBox_4.addItem(publisher[0])


def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()