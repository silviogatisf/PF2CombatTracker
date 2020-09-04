import sys

from PyQt5 import QtCore
from PyQt5.QtCore import (QSize, Qt)
from PyQt5.QtGui import (QIcon, QBitmap, QPixmap)
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

        layout.addStretch(1)


        centraWid = QWidget()
        centraWid.setLayout(layout)
        self.setCentralWidget(centraWid)              #Changed from QMdiArea to Qwidget, still confused on how to use it

    def _roundWidget(self):
        """Top Widget: Informations before characters, called on _createCentralWidget"""

        # creates the round counter
        roundNumber = 0
        roundDisplay = QLabel(f"<h1>ROUND: {roundNumber}</h1>") # aqui eu tou usando f-string, é uma coisa do python3 pra colocar jogar a variável dentro da string de uma maneira mais fácil.
        # layout of the first line of roundDisplay
        roundDisplayLayout1 = QHBoxLayout()
        # roundDisplay.setLayout(roundDisplayLayout1)
        roundDisplayLayout1.addWidget(roundDisplay)
        roundDisplayLayout1.addStretch(1) # isso daqui é um espaçador para empurrar o label pra esquerda

        # creates the line with the char's turn, actions e buttons to advance and return an turn / slash round
        turnDisplay = QLabel("<h2>Character's turn<h2>") # essa parada ta de placeholder, a gente tem que colocar o personagem a partir da função que determina o turno do personagem.
        turnDisplayLayout = QVBoxLayout()
        turnDisplayLayout.addStretch(10)
        turnDisplayLayout.addWidget(turnDisplay)
        turnDisplayLayout.addStretch(10)

        # previous turn button
        previousTurn = QPushButton(self)
        previousTurn.resize(24,24)
        previousTurn.setIcon(QIcon('circle-left.png'))
        previousTurn.setIconSize(QSize(24,24))

        # actions logic
        actionsNumber = 3 # por default o jogador deve ter 3 ações, as condições do personagem vão interferir nisso.
        # actions layout
        actionLayout = QHBoxLayout()
        for action in range(0, actionsNumber):
            actionsIcon = QLabel(self)
            actionsIconPixmap = QPixmap('action.png')
            actionsIcon.setPixmap(actionsIconPixmap)
            actionLayout.addWidget(actionsIcon)
            actionLayout.addSpacing(10)

        # next turn button
        nextTurn = QPushButton(self)
        nextTurn.resize(24,24)
        nextTurn.setIcon(QIcon('circle-right.png'))
        nextTurn.setIconSize(QSize(24,24))

        # layout of the second line of the roundDysplay
        roundDisplayLayout2 = QHBoxLayout()
        roundDisplayLayout2.addLayout(turnDisplayLayout)
        roundDisplayLayout2.addStretch(1)
        roundDisplayLayout2.addWidget(previousTurn)
        roundDisplayLayout2.addSpacing(10)
        roundDisplayLayout2.addLayout(actionLayout)
        roundDisplayLayout2.addWidget(nextTurn)

        # toplayout of roundisplay
        self.toplayout = QVBoxLayout()
        self.toplayout.addLayout(roundDisplayLayout1)
        self.toplayout.addLayout(roundDisplayLayout2)

        self.setLayout(self.toplayout)
        return self.toplayout

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