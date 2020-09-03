import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QToolBar, QStatusBar, QMainWindow, QWidget, QVBoxLayout, QLabel, QApplication, QComboBox)
from PyQt5 import (QtWidgets, QtGui)

class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle('Pathfinder 2E Combat Tracker')

        # Definição geral do layout
        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)
        # self.setCentralWidget(QMdiArea())   #QMdiArea permite criar multiplos widget no setCentralWidget
        # - Certo, mas o app da gente não precisa de um mainwidget dividido. Podemos ter um layout vertical com partes separadas, como no exemplo da calculadora
        # que tem o display e os botões. A parte debaixo, onde vai entrar os caracteres que tem que ser escolável. (até copiei o código de lá na cara dura)
        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        self.setGeometry(300, 300, 680, 600)

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
        cond = QComboBox(self)    #Define dropdown menu
        tools.addWidget(QLabel('Condition: '))
        tools.addWidget(cond)
        cond.addItems(['Cond1', 'Cond2', 'Cond3', 'Cond4', 'Cond5', 'Cond6', 'Cond7', 'Cond8', 'Cond9']) #Add all buttons in the dropdown menu
        condVal = QComboBox(self)
        tools.addWidget(condVal)
        condVal.addItems(['Value', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        tools.addAction(QIcon(), 'Apply')
        tools.addWidget(QLabel('Effect: '))
        tools.addWidget(QLineEdit('Type here'))
        effecRounds = QComboBox(self)
        tools.addWidget(effecRounds)
        effecRounds.addItems(['Value', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        tools.addAction(QIcon(), 'Apply')

    def _createRoundLayout(self):
        """Cria a parte de round no programa"""

        # Contador de rounds
        self.roundNumber = 0
        self.roundCont = QLabel('<h1>Round</h1> ' + str(self.roundNumber))

        # linha com o turno e as ações


    def _createStatusBar(self):
        """Status bar"""
        status = QStatusBar()
        status.showMessage("Let's roll the dice")
        self.setStatusBar(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())