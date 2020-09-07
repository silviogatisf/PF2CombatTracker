import sys

from PyQt5 import (QtWidgets, QtGui, Qt, QtCore)
from functools import partial
from PyQt5.QtCore import (QSize, Qt)
from PyQt5.QtGui import (QIcon, QBitmap, QPixmap)
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QToolBar, QStatusBar, QMainWindow, QMdiArea, QLabel, QApplication,
                             QComboBox, QVBoxLayout, QHBoxLayout, QToolBox, QGridLayout, QTextEdit, QWidget, QRadioButton,
                             QCheckBox, QScrollArea, QBoxLayout, QSizePolicy)

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
        addCharBtn = QPushButton()
        addCharBtn.setIcon(QIcon('addchar.png'))
        self.tools.addWidget(addCharBtn)
        addCharBtn.clicked.connect(self.addChar)

        # BTN Monster
        addMonBtn = QPushButton()
        addMonBtn.setIcon(QIcon('monster.png'))
        self.tools.addWidget(addMonBtn)

        #BTN Remove char
        removeCharBtn = QPushButton()
        removeCharBtn.setIcon(QIcon('removechar.png'))
        self.tools.addWidget(removeCharBtn)
        removeCharBtn.clicked.connect(self.removeChar)

        # BTN Sort
        sortBtn = QPushButton()
        sortBtn.setIcon(QIcon('sort.png'))
        self.tools.addWidget(sortBtn)

        # Condition label
        self.tools.addWidget(QLabel('Condition: '))

        # condCombo
        self.condCombo = QComboBox()

        # Add condCombo data
        for condition in conditionList:
            self.condCombo.addItem(condition)
        # Connect combo
        self.condCombo.currentIndexChanged.connect(self._updateCondVal)
        #add combo to toolbar
        self.tools.addWidget(self.condCombo)

        # CondValueCombo
        self.comboVal = QComboBox()
        self.comboVal.addItems(conditionGeneralValue)
        self.tools.addWidget(self.comboVal)

        # Btn apply Condition
        self.btnApplyCond = QPushButton('Apply')
        self.tools.addWidget(self.btnApplyCond)

        # Effect Combo
        self.tools.addWidget(QLabel('Effect: '))
        self.tools.addWidget(QLineEdit('Type here'))
        self.effecRounds = QComboBox(self)
        self.tools.addWidget(self.effecRounds)
        self.effecRounds.addItems(['Value', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.btnApplyEffect = QPushButton('Apply')
        self.tools.addWidget(self.btnApplyEffect)

    # Upadate comboVal function
    def _updateCondVal(self):
        condition = self.condCombo.currentText()
        # ordinaryCombo1 = QComboBox
        # ordinaryCombo2 = QComboBox
        # ordinaryCombo3 = QComboBox
        if condition in conditionGeneral:
            self.comboVal.clear()
            for val1 in conditionGeneralValue:
                self.comboVal.addItem(val1)
        elif condition in conditionCount:
            self.comboVal.clear()
            for val2 in conditionCountValue:
                self.comboVal.addItem(val2)
        else:
            self.comboVal.clear()
            for val3 in persistentDamageValue:
                self.comboVal.addItem(val3)

    def addChar(self):
        self.charCount = self.charCount + 1
        self.populateCharWidget()

    def removeChar(self):
        if self.charCount > 1:
            self.charCount = self.charCount - 1
            self.populateCharWidget()
        else:
            pass

    def _createCentralWidget(self):
        """Central Widget"""
        layout = QVBoxLayout()

        scroll = QScrollArea()          # Scroll Area which contains the widgets
        widget = QWidget()              # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()            # The Vertical Box that contains _charLayout

        self.vbox.setObjectName("vbox")
        self.charCount = 2

        layout.addWidget(self._roundWidget())           #Calling RoundInfo widget
        layout.addWidget(scroll)

        self.populateCharWidget()

        """Scroll Area Properties"""
        widget.setLayout(self.vbox)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)

        centraWid = QWidget()
        centraWid.setLayout(layout)
        self.setCentralWidget(centraWid)              #Changed from QMdiArea to Qwidget, still confused on how to use it

    def populateCharWidget(self):
        for i in reversed(range(self.vbox.count())):
            self.vbox.itemAt(i).widget().setParent(None)

        x = 0
        while x < self.charCount:  # Routine to call add X characters
            x = x + 1
            self.vbox.addWidget(self._charWidget())  # Calling character widget

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
        turnDisplay.setFixedHeight(20)
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
        self.toplayoutWidget = QWidget()
        self.toplayoutWidget.setFixedHeight(85)
        self.toplayout = QVBoxLayout()
        self.toplayoutWidget.setLayout(self.toplayout)
        self.toplayout.addLayout(roundDisplayLayout1)
        self.toplayout.addLayout(roundDisplayLayout2)

        self.setLayout(self.toplayout)
        return self.toplayoutWidget

    def textEdited(self):
        # If the input is left empty, revert back to the label showing
        if not self.charNameEdit.text():
            self.charNameEdit.hide()
            self.charName.setText(f"<h1>{'Personagem'}</h1>")
            self.charName.show()
        elif self.charNameEdit.text():
            self.charName.setText(f"<h1>{self.charNameEdit.text()}</h1>")
            self.charNameEdit.hide()
            self.charName.show()

    def _charWidget(self):
        """Characte Widget: Information of character Called on _createCentralWidget"""

        """Placing editable characters name"""


        self.charNameEdit = QLineEdit()
        #self.charNameEdit.setPlaceholderText('Nome do Personagem')
        self.charNameEdit.hide()
        self.charNameEdit.editingFinished.connect(self.textEdited)
        self.charName = BuddyLabel(self.charNameEdit)
        self.charName.setText(f"<h1>{'Personagem'}</h1>")  # to be defined from a list with all characters in combat
        self.charName.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

        charDisplayLayout2 = QHBoxLayout()
        charDisplayLayout2.setSpacing(10)
        charDisplayLayout2.addWidget(self.charName)
        charDisplayLayout2.addWidget(self.charNameEdit)
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
        reactionBtn = QPushButton(self)
        reactionBtn.resize(24,24)
        reactionBtn.setIcon(QIcon('reaction.png'))
        reactionBtn.setIconSize(QSize(24,24))

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
        charlayout = QVBoxLayout()
        charlayoytWidget = QWidget()
        charlayoytWidget.setLayout(charlayout)
        charlayout.addLayout(charDisplayLayout2)
        charlayout.addLayout(charDisplayLayout3)
        charlayout.addLayout(charDisplayLayout4)

        return charlayoytWidget

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Let's roll the dice")
        self.setStatusBar(status)

# ConditionData
conditionList = ['NA', 'Blinded', 'Broken(object)', 'Clumsy', 'Concealed','Confused', 'Controled', 'Dazzled', 'Deafened', 'Doomed','Drained', 'Dying', 'Encumbered', 'Enfleebed', 'Fascinated', 'Fatigued', 'Flat-Footed', 'Fleeing', 'Friendly', 'Frightened', 'Grabbed', 'Helpful', 'Hidden', 'Hostile', 'Immobilized', 'Indifferent', 'Invisible', 'Observed', 'Persistent Damage', 'Petrified', 'Prone', 'Quickened', 'Restrained', 'Sickened', 'Slowed', 'Stunned', 'Stupefied', 'Unconscious', 'Undetected', 'Unfriendly', 'Unnoticed', 'Wounded']
conditionGeneral = ['NA', 'Blinded', 'Broken(object)', 'Concealed','Confused', 'Controled', 'Dazzled', 'Deafened', 'Encumbered', 'Fascinated', 'Fatigued', 'Flat-Footed', 'Fleeing', 'Friendly', 'Grabbed', 'Helpful', 'Hidden', 'Hostile', 'Immobilized', 'Indifferent', 'Invisible', 'Observed', 'Petrified', 'Prone', 'Quickened', 'Restrained', 'Unconscious', 'Undetected', 'Unfriendly', 'Unnoticed']
conditionCount = ['Clumsy', 'Doomed','Drained', 'Dying', 'Enfleebed', 'Frightened', 'Sickened', 'Slowed', 'Stunned', 'Stupefied', 'Wounded']
# valueData
conditionGeneralValue = ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other']
conditionCountValue = ['NA', '1', '2', '3', '4', '5']
persistentDamageValue = ['NA', '1d4', '2d4', '3d4', '1d6', '2d6', '3d6', '1d8', '2d8', 'other']

class personagem():
    def __init__(self, name, ac, hp, init, cond, effect, footnote, reaction, turnBool, actionNumber, parent = None):
        super(personagem, self).__init__(parent)
        self.name = name
        self.ac = ac
        self.hp = hp
        self.init = init
        self.effect = effect
        self.footnote = footnote
        self.reaction = reaction
        self.turnBool = turnBool
        self.actionNumber = actionNumber



# Make a custom label widget (mostly for its mousePressEvent) Used to hide characters name
class BuddyLabel(QLabel):
    def __init__(self, buddy, parent = None):
        super(BuddyLabel, self).__init__(parent)
        self.buddy = buddy

    # When it's clicked, hide itself and show its buddy
    def mousePressEvent(self, event):
        self.hide()
        self.buddy.show()
        self.buddy.setFocus() # Set focus on buddy so user doesn't have to click again

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())