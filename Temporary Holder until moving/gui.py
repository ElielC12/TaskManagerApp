# Logan Gardner
# Shoping Cart App
# Started 11/12 Added Some features
# Finsihed 11/13 Finshied Functionality

import datetime
from PySide6.QtGui import QKeyEvent, QColor, QFont, QIcon
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QWidget, QListWidget, QListWidgetItem, QHBoxLayout, QGridLayout, QLineEdit, QPushButton, QAbstractItemView, QDialog, QDialogButtonBox, QMessageBox, QDateEdit, QComboBox, QSpacerItem, QSizePolicy, QInputDialog, QStyle, QStyleFactory
from PySide6.QtCore import Qt, QDate, QTimer
import os, json
import backend

class ListItemWithId(QListWidgetItem):
    def __init__(self, id: int, label: str):
        super().__init__()
        self.id = id
        self.label = label
        self.setText(label)


class ConfirmDelete(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wait!!!")
        backend.checkForFile()

        QBtn = (
            QDialogButtonBox.Yes | QDialogButtonBox.Cancel
        )

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("Are you sure you want to delete the selected items?")
        layout.addWidget(message)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

class MyWindow(QMainWindow):
    def __init__(self):
            
        super().__init__()
        self.setWindowTitle("Trackit")
        self.setWindowIcon(QIcon('pencil-icon.png'))
        self.resize(800, 500)

        self.CatSort = False
        self.curName = ''
        self.selectedRows = []
        
        pageLayout = QVBoxLayout()

        #Add Top add section 
        self.AddEntries = QGridLayout() # Name Input
        self.AddName = QLineEdit()
        self.AddName.setMaxLength(14)
        self.AddName.setMinimumWidth(100)
        self.AddName.setPlaceholderText('Name')
        self.AddName.textChanged.connect(self.setAddName)
        self.AddDate = QDateEdit() # Date Input 
        self.AddDate.dateChanged.connect(self.setAddDate)
        self.curDate = self.AddDate.text()
        self.AddCat = QComboBox() # Category Input
        self.AddCat.setMinimumWidth(160)
        with open(f'storage.json', 'r') as storage: # Adds Categorys from JSON
            storage = json.load(storage)
            cats = storage['cats']
            for cat in cats:
                self.AddCat.addItem(cat, cats.index(cat))
        self.curCat = self.AddCat.currentText()
            # Example of how to remove Category for add and deletion later
            # for cat in cats:
            #     if cats.index(cat) == 2:
            #         self.AddCat.removeItem(2)
                
        self.AddCat.currentIndexChanged.connect(self.setAddCat)
        self.AddButton = QPushButton("+")

        self.AddButton.clicked.connect(self.addItem)
        self.AddEntries.addWidget(self.AddName, 0, 0, 1, 1)
        self.AddEntries.addWidget(self.AddDate, 0, 1, 1, 1)
        self.AddEntries.addWidget(self.AddCat, 0, 2, 1, 1)
        self.AddEntries.addWidget(self.AddButton, 0, 3, 1, 1)
        
        self.addEntriesWidget = QWidget()

        self.addEntriesWidget.setLayout(self.AddEntries)
        pageLayout.addWidget(self.addEntriesWidget)

        #Add list section
        self.list = QListWidget()
        self.list.setSelectionMode(QAbstractItemView.ExtendedSelection)
        # if os.path.exists(f'{os.path.abspath(__file__)[:-6]}storage.txt'):
        self.sort()
        self.refreshItems()

        self.list.itemDoubleClicked.connect(self.editItem)
        self.list.currentItemChanged.connect(self.printThis)
        self.list.setStyleSheet("""
            QListWidget::item {
                font-size: 20px;
                color: black;
                font-family: Courier;
            }
        """)
        pageLayout.addWidget(self.list)
        
        #Add Bottom Button section
        self.DeleteButton = QPushButton('-')
        self.DeleteButton.clicked.connect(self.removeItem)
        pageLayout.addWidget(self.DeleteButton)

        

        MainPage = QWidget()
        MainPage.setLayout(pageLayout)

        Sidebar = QWidget()
        sidebarLayout = QVBoxLayout()
        Sidebar.setLayout(sidebarLayout)
        Sidebar.setObjectName('Sidebar')
        

        mainLayout = QHBoxLayout()
        mainLayout.addWidget(MainPage)
        # mainLayout.addWidget(QPushButton())
        mainLayout.addItem(QSpacerItem(50, 0, QSizePolicy.Fixed, QSizePolicy.Expanding))
        mainLayout.addWidget(Sidebar)

        self.CatToggle = QPushButton()
        self.CatToggle.clicked.connect(self.toggleSort)
        self.CatToggle.setText('Category Sort Off')

        sidebarLayout.addWidget(self.CatToggle)
        sidebarLayout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        self.newCatName = QLineEdit()
        self.newCatName.setMaxLength(11)
        self.newCatName.setPlaceholderText("New Category Name")
        sidebarLayout.addWidget(self.newCatName)

        self.addNewCat = QPushButton()
        self.addNewCat.clicked.connect(self.addNwCat)
        self.addNewCat.setText('Add New Category')
        sidebarLayout.addWidget(self.addNewCat)

        self.removeCat = QPushButton()
        self.removeCat.clicked.connect(self.removeCurCat)
        self.removeCat.setText('Remove Current Category')
        sidebarLayout.addWidget(self.removeCat)

        
        self.timer = QTimer()
        self.timer.timeout.connect(self.timerCycle)
        self.timer.start(60000)

        mainWidget = QWidget()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)
        # self.setCentralWidget(MainPage)

        self.setStyleSheet("""
    QLineEdit, QDateEdit, QComboBox {
        font-size: 15pt;
        background-color: white;
        padding: 5px;
        color: black;
    }
                           
    QDateEdit {
        width: 130px;                    
    }

    QMainWindow {
        background-color: #808080;
    }
                           
    QListWidget {
        background-color: #808080;
        border: 2px solid black;
        border-radius: 10px;
        padding: 5px;
    }
        
    QPushButton{
        background-color: white;
        color: black;
        font-size: 15pt;
    }
                           
    QWidget#Sidebar {
        margin-left: 10px;
    }
""")

    def timerCycle(self):
        self.sort()
        self.clearList()
        self.refreshItems()
        print('cycle')

    def addItem(self):  # Correctly adds an item even to the JSON.
                        # PLEASE NOTE the Date adder will change to be a date input not text,
                        # and the dropdown for the categories is also being added still.
        if self.curName != '':
            # self.list.addItem(self.curName + "-------" + self.AddDate.text())
            # self.list.sortItems(order=Qt.AscendingOrder)
            backend.addToJSON(backend.createID(), self.AddName.text(), self.AddDate.text(), self.AddCat.currentText())
            self.AddName.setText('')
            self.AddDate.setDate(QDate())
            self.sort()
            self.clearList()
            self.refreshItems()

    # These next 3 make it easy to modify the properties in the other methods
    def setAddName(self, text):
        self.curName = text
    
    def setAddDate(self, text):
        self.curDate = text
        
    def setAddCat(self, text):
        self.curCat = text

    def removeItem(self): 

        query = QMessageBox.question(self, "Wait!!!", 'Are you sure you want to delete the selected items?')
        if query == QMessageBox.Yes:
            # for item in self.list.selectedItems():
            #     self.list.takeItem(self.list.row(item))
            for item in self.list.selectedItems():
                backend.removeFromJSON(item.id)
            self.sort()
            self.clearList()
            self.refreshItems()


    def editItem(self, item):

        input = QDialog()
        input.setWindowTitle('Edit Assignent')
        input.setWindowIcon(QIcon('pencil-icon.png'))
        inputLayout = QVBoxLayout()

        top = QLabel('Edit Selected Item')
        top.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inputLayout.addWidget(top)

        rename = QLineEdit()
        rename.setMaxLength(14)
        inputLayout.addWidget(rename)
        reDate = QDateEdit()
        inputLayout.addWidget(reDate)
        reCat = QComboBox() # Category Input

        itemData = backend.getInfo(item.id)[0]
        name = itemData['name']
        date = itemData['date'].split('/')
        y = int(date[2])
        m = int(date[0])
        d = int(date[1])
        cat = itemData['category']
        rename.setText(name)
        reDate.setDate(QDate(y, m, d))
        reCat.setCurrentText(cat)

        with open(f'storage.json', 'r') as storage: # Adds Categorys from JSON
            storage = json.load(storage)
            cats = storage['cats']
            for cat in cats:
                reCat.addItem(cat, cats.index(cat))
        input.setLayout(inputLayout)
        inputLayout.addWidget(reCat)


        def accept():
            backend.editJSONItem(item.id, rename.text(), reDate.text(), reCat.currentText())
            self.sort()
            self.clearList()
            self.refreshItems()
            input.close()
        def reject():
            input.close()
        
        aOD = (QDialogButtonBox.Save | QDialogButtonBox.Cancel)
        saveDiscardBox = QDialogButtonBox(aOD)
        saveDiscardBox.accepted.connect(accept)
        saveDiscardBox.rejected.connect(reject)
        inputLayout.addWidget(saveDiscardBox)


        # if input.exec():
        #     print('REMOVE')
        # else:
        #     print('none')
        # for self.list.selectedItems():

    def clearList(self):
        """Clears the Gui's List of List items. DOES NOT remove the items from JSON
        """
        for item in range(self.list.count()):
            self.list.takeItem(0)
        
    def refreshItems(self):
        """ Adds Items from JSON File
        """
        with open(f'storage.json', 'r') as storage:
            storage = json.load(storage)
            items = storage["items"]
            for item in items:
                # self.list.addItem(item["name"] + "-------" + item["date"])
                newitem = ListItemWithId(item["id"], f"{item["category"]:<12}" + f"{item["name"]:<15}" + f'{item["date"]:<8}' )
                backend.sortByDate()
                
                # Start Color
                today = datetime.datetime.now()
                curAssignmentDate = datetime.datetime.strptime(item["date"], "%m/%d/%Y")
                if curAssignmentDate - today < datetime.timedelta(days=2):
                    newitem.setBackground(QColor(242, 71, 38))
                elif curAssignmentDate - today < datetime.timedelta(days=7):
                    newitem.setBackground(QColor(250, 199, 16))
                elif curAssignmentDate - today > datetime.timedelta(days=7):
                    newitem.setBackground(QColor(11, 167, 137))
                else:
                    newitem.setBackground(QColor(0, 0 ,255))
                font = QFont()
                font.setPointSize(13)
                font.setFamily('Courier New')
                newitem.setFont(font)
                self.list.addItem(newitem)

    def printThis(self, current, previous): # Dont remember what this does or if its needed
        self.selectedRows.append(self.list.row(current))

    def keyPressEvent(self, event: QKeyEvent) -> None: #For PySide interacton with keys to action
        if event.key() == Qt.Key_Delete or event.key() == Qt.Key_Backspace:
            self.removeItem()
        if event.key() == Qt.Key_Return:
            self.addItem()

    def closeEvent(self, event): #Old May not be needed. Runs when program closes. May be useful
        with open(f'{os.path.abspath(__file__)[:-6]}storage.txt', 'w') as storage:    
            for count in range(self.list.count()):
                storage.write(self.list.item(count).text() + '\n')
                os.path.abspath(__file__)
    
    def toggleSort(self):
        if self.CatSort:
            self.CatSort = False
            self.CatToggle.setText('Category Sort Off')
        else:
            self.CatSort = True
            self.CatToggle.setText('Category Sort On')
        self.sort()
        self.clearList()
        self.refreshItems()

    def addNwCat(self):
        """
        Adds Category to JSON list and clears category name input
        """
        backend.addCategory(self.newCatName.text())
        self.newCatName.setText('')
        with open(f'storage.json', 'r') as storage: # Adds Categorys from JSON
                storage = json.load(storage)
                cats = storage['cats']
                for item in range(len(cats) + 1):
                    self.AddCat.removeItem(0)
                for cat in cats:
                    self.AddCat.addItem(cat, cats.index(cat))
        self.sort()
        self.clearList()
        self.refreshItems()
    
    def removeCurCat(self):
        """
        Remove cur Category from JSON and replace the Cat of every item with that category with None
        """
        if self.AddCat.currentText() != 'None':
            backend.removeCategory(self.AddCat.currentText())
            with open(f'storage.json', 'r') as storage: # Adds Categorys from JSON
                storage = json.load(storage)
                cats = storage['cats']
                for item in range(len(cats) + 1):
                    self.AddCat.removeItem(0)
                for cat in cats:
                    self.AddCat.addItem(cat, cats.index(cat))
            self.curCat = self.AddCat.currentText()
            self.sort()
            self.clearList()
            self.refreshItems()

    def sort(self):
        if self.CatSort:
            backend.sortByCategoryAndDate()
        else:
            backend.sortByDate()

if __name__ == '__main__':
    app = QApplication()
    w = MyWindow()
    w.show()
    app.exec()