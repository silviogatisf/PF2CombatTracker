import sys

from PyQt5 import QtCore
from PyQt5.QtCore import (QSize, Qt)

from PyQt5.QtGui import (QIcon, QBitmap, QPixmap)
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QToolBar, QStatusBar, QMainWindow, QMdiArea, QLabel, QApplication,
                             QComboBox, QVBoxLayout, QHBoxLayout, QToolBox, QGridLayout, QTextEdit, QWidget, QRadioButton,
                             QCheckBox, QScrollArea, QBoxLayout)
from PyQt5 import (QtWidgets, QtGui, Qt)

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
        self.tools = QToolBar()
        self.addToolBar(self.tools)
        self.tools.setIconSize(QSize(24,24))
        self.tools.setFixedHeight(36)
        self.tools.setStyleSheet("QToolBar{spacing:5px;}")

#        folderOpen = QtWidgets.QAction(QtGui.QIcon("add_pack.ico"), "Open Folder", tools)   #Dunno how to use it... but shows an icon instead of text, Might be useful
#        tools.addAction(folderOpen)

        # BTN Add char
        self.addCharBtn = QPushButton()
        self.addCharBtn.setIcon(QIcon('addchar.png'))
        self.tools.addWidget(self.addCharBtn)

        # BTN Monster
        self.addMonBtn = QPushButton()
        self.addMonBtn.setIcon(QIcon('monster.png'))
        self.tools.addWidget(self.addMonBtn)

        #BTN Remove char
        self.removeCharBtn = QPushButton()
        self.removeCharBtn.setIcon(QIcon('removechar.png'))
        self.tools.addWidget(self.removeCharBtn)

        # BTN Sort
        self.sortBtn = QPushButton()
        self.sortBtn.setIcon(QIcon('sort.png'))
        self.tools.addWidget(self.sortBtn)

        # CondCombo
        self.tools.addWidget(QLabel('Condition: '))
        self.cond = QComboBox()
        self.tools.addWidget(self.cond)
        self.cond.addItems(['Cond1', 'Cond2', 'Cond3', 'Cond4', 'Cond5', 'Cond6', 'Cond7', 'Cond8', 'Cond9']) #Add all buttons in the dropdown menu
        self.condVal = QComboBox(self)
        self.tools.addWidget(self.condVal)
        self.condVal.addItems(['Value', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.btnApplyCond = QPushButton('Apply')
        self.tools.addWidget(self.btnApplyCond)

        # ValueCombo
        self.tools.addWidget(QLabel('Effect: '))
        self.tools.addWidget(QLineEdit('Type here'))
        self.effecRounds = QComboBox(self)
        self.tools.addWidget(self.effecRounds)
        self.effecRounds.addItems(['Value', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.btnApplyEffect = QPushButton('Apply')
        self.tools.addWidget(self.btnApplyEffect)

    def _createCentralWidget(self):
        """Central Widget"""
        layout = QVBoxLayout()
        scroll = QScrollArea()          # Scroll Area which contains the widgets
        widget = QWidget()              # Widget that contains the collection of Vertical Box
        vbox = QVBoxLayout()            # The Vertical Box that contains _charLayout


        layout.addItem(self._roundWidget())             #Calling RoundInfo widget
        layout.addWidget(scroll)

        charNum = 5
        x = 0
        while x < charNum:                             #Routine to call add X characters
            x = x + 1
            vbox.addItem(self._charWidget())         #Calling character widget

        """Scroll Area Properties"""
        widget.setLayout(vbox)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)


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

        charDisplayLayout2 = QHBoxLayout()
        charDisplayLayout2.setSpacing(10)

        charName = QLabel(f"<h1>{'Personagem'}</h1>")  # to be defined from a list with all characters in combat
        charDisplayLayout2.addWidget(charName)
        charDisplayLayout2.addStretch(1)
        charDisplayGrid = QGridLayout()
        charDisplayLayout2.addLayout(charDisplayGrid)

        """Defining all the widgets"""
        hp = QLabel('HP')           #Title HP
        hpMod = QLabel('HP MOD')    #Title HP MOD
        hpDisplay = QLabel('100')   #Amount of HP, must be a variable to be changeable
        hpModLine = QLineEdit()     #Place to write the amount of HP to be deducted
        hpModLine.setFixedWidth(40)
        hpApply = QPushButton('Apply')
        hpApply.setFixedWidth(40)
        ac = QLabel('AC')           #Title AC
        acTotal = QLabel('AC Total')#Title AC Total
        acDisplay = QLabel('120')   #Amout of AC, must be a variable to be changeable
        acTotalLine = QLineEdit()   #Plave to write a valor of AC
        acTotalLine.setFixedWidth(40)
        acApply = QPushButton('Apply')
        acApply.setFixedWidth(40)
        init = QLabel('Init')       #Title Init
        initLine = QLineEdit()      #Place to write Init, should be saved in a variable to be able to order characters
        initLine.setFixedWidth(40)

        """Placing all the widgets in a grid format"""
        charDisplayGrid.addWidget(hp, 0, 0)
        charDisplayGrid.addWidget(hpMod, 0, 1)
        charDisplayGrid.addWidget(ac, 0, 3)
        charDisplayGrid.addWidget(acTotal, 0, 4)
        charDisplayGrid.addWidget(init, 0, 6)
        charDisplayGrid.addWidget(hpDisplay, 1, 0)
        charDisplayGrid.addWidget(hpModLine, 1, 1)
        charDisplayGrid.addWidget(hpApply, 1, 2)
        charDisplayGrid.addWidget(acDisplay, 1, 3)
        charDisplayGrid.addWidget(acTotalLine, 1, 4)
        charDisplayGrid.addWidget(acApply, 1, 5)
        charDisplayGrid.addWidget(initLine, 1, 6)

        """Placing conditions and effects"""
        charDisplayLayout3 = QHBoxLayout()
        cond = QLabel('Condition 1')
        condPlus = QPushButton('+')
        condPlus.setFixedWidth(20)
        condMinus = QPushButton('-')
        condMinus.setFixedWidth(20)
        reactionBtn = QPushButton('Reaction icon')

        isCond = 1                                      #Variable to check if there is condition

        if isCond == True:
            charDisplayLayout3.addWidget(cond)
            charDisplayLayout3.addWidget(condPlus)
            charDisplayLayout3.addWidget(condMinus)

        charDisplayLayout3.addStretch(1)
        charDisplayLayout3.addWidget(reactionBtn)

        #Free space to write
        charDisplayLayout4 = QHBoxLayout()
        editText = QTextEdit()
        charDisplayLayout4.addWidget(editText)


        # # Setting character layout
        self.charlayout = QVBoxLayout()
        #self.charlayout.addLayout(charDisplayLayout1)
        self.charlayout.addLayout(charDisplayLayout2)
        self.charlayout.addLayout(charDisplayLayout3)
        self.charlayout.addLayout(charDisplayLayout4)
        self.setLayout(self.charlayout)

        return self.charlayout

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Let's roll the dice")
        self.setStatusBar(status)

conditionData = {
    'NA':'NA',
    'Blinded': ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Broken(object)' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Clumsy' : ['NA', '1', '2', '3', '4', '5'],
    'Concealed' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Confused' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Controled' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Dazzled' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Deafened' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Doomed' : ['NA', '1', '2', '3', '4', '5'],
    'Drained' : ['NA', '1', '2', '3', '4', '5'],
    'Dying' : ['NA', '1', '2', '3', '4', '5'],
    'Encumbered' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Enfleebed' : ['NA', '1', '2', '3', '4', '5'],
    'Fascinated' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Fatigued' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Flat-Footed' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Fleeing' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Friendly' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Frightened' : ['NA', '1', '2', '3', '4', '5'],
    'Grabbed' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Helpful' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Hidden' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Hostile' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Immobilized' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Indifferent' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Invisible' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Observed' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Persistent Damage' : ['NA', '1d4', '2d4', '3d4', '1d6', '2d6', '3d6', '1d8', '2d8', 'other'],
    'Petrified' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Prone' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Quickened' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Restrained' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Sickened' : ['NA', '1', '2', '3', '4', '5'],
    'Slowed' : ['NA', '1', '2', '3', '4', '5'],
    'Stunned' : ['NA', '1', '2', '3', '4', '5'],
    'Stupefied' : ['NA', '1', '2', '3', '4', '5'],
    'Unconscious' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Undetected': ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Unfriendly' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Unnoticed' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
    'Wounded' : ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other'],
}

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())