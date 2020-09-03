import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QToolBar, QStatusBar, QMainWindow, QMdiArea, QLabel, QApplication,
                             QComboBox, QVBoxLayout, QHBoxLayout, QToolBox, QGridLayout, QTextEdit, QWidget, QRadioButton,
                             QCheckBox)
from PyQt5 import (QtWidgets, QtGui)

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Pathfinder 2E Combat Tracker')
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        self._createCentralWidget()
        self.setGeometry(300, 300, 750, 600)

    def _createMenu(self):
        """"Main menu"""
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction(QIcon(), 'Load')
        self.menu.addAction(QIcon(), 'Save')
        self.menu.addAction(QIcon(), 'About')
        self.menu.addAction(QIcon(), '&Exit', self.close)

    def _createToolBar(self):
        """Toolbar"""
        tools = QToolBar()
        self.addToolBar(tools)

#        folderOpen = QtWidgets.QAction(QtGui.QIcon("add_pack.ico"), "Open Folder", tools)   #Dunno how to use it... but shows an icon instead of text, Might be useful
#        tools.addAction(folderOpen)
        tools.addAction('Add Char')
        tools.addAction('Add Monster')
        tools.addAction('Remove Char')
        tools.addAction('Reorder Init')

        cond = QComboBox(self)                               #Define dropdown menu
        tools.addWidget(QLabel('Condition: '))
        tools.addWidget(cond)
        cond.addItems(['Cond1', 'Cond2', 'Cond3', 'Cond4', 'Cond5', 'Cond6', 'Cond7', 'Cond8', 'Cond9']) #Add all buttons in the dropdown menu
        condVal = QComboBox(self)
        tools.addWidget(condVal)
        condVal.addItems(['Value', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        btnApplyCond = QPushButton('Apply')
        tools.addWidget(btnApplyCond)

        tools.addWidget(QLabel('Effect: '))
        tools.addWidget(QLineEdit('Type here'))
        effecRounds = QComboBox(self)
        tools.addWidget(effecRounds)
        effecRounds.addItems(['Value', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        btnApplyEffect = QPushButton('Apply')
        tools.addWidget(btnApplyEffect)

    def _createCentralWidget(self):
        """Central Widget"""
        layout = QVBoxLayout()

        layout.addItem(self._roundWidget())             #Calling RoundInfo widget

        charNum = 5
        x = 0
        while x < charNum:                             #Routine to call add X characters
            x = x + 1
            layout.addItem(self._charWidget())         #Calling character widget


        centraWid = QWidget()
        centraWid.setLayout(layout)
        self.setCentralWidget(centraWid)              #Changed from QMdiArea to Qwidget, still confused on how to use it

    def _roundWidget(self):
        """Top Widget: Informations before characters, called on _createCentralWidget"""
        toplayout = QHBoxLayout()

        toplayout.addWidget(QLabel("Round 1"))

        toplayout.addWidget(QLabel("Character 1 turn"))

        toplayout.addWidget(QPushButton('Previous Char'))
        toplayout.addWidget(QCheckBox())
        toplayout.addWidget(QCheckBox())
        toplayout.addWidget(QCheckBox())
        toplayout.addWidget(QPushButton('Next Char'))
        return toplayout

    def _charWidget(self):
        """Characte Widget: Information of character Called on _createCentralWidget"""
        charlayout = QHBoxLayout()

        charlayout.addWidget(QLabel('Character 1 '))

        charlayout.addWidget(QLabel('HP: 100% '))
        charlayout.addWidget(QLabel('HP MOD: '))
        charlayout.addWidget(QLineEdit())
        charlayout.addWidget(QPushButton('Apply'))

        charlayout.addWidget(QLabel('AC: 100% '))
        charlayout.addWidget(QLabel('AC MOD'))
        charlayout.addWidget(QLineEdit())
        charlayout.addWidget(QPushButton('Apply'))

        charlayout.addWidget(QLabel('Init: '))
        charlayout.addWidget(QLineEdit())
        return charlayout

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Let's roll the dice")
        self.setStatusBar(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())