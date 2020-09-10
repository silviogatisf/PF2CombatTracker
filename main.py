import sys

from PyQt5.QtCore import (QSize, QRegExp)
from PyQt5.QtGui import (QIcon, QPixmap, QRegExpValidator)
from PyQt5.QtWidgets import (QPushButton, QLineEdit, QToolBar, QStatusBar, QMainWindow, QLabel, QApplication,
                             QComboBox, QVBoxLayout, QHBoxLayout, QMessageBox, QGridLayout, QTextEdit, QWidget,
                             QScrollArea, QSizePolicy, QRadioButton)

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

        # BTN Add char
        addCharBtn = QPushButton()
        addCharBtn.setIcon(QIcon('addchar.png'))
        self.tools.addWidget(addCharBtn)
        addCharBtn.clicked.connect(self._addChar)

        #BTN Remove char
        removeCharBtn = QPushButton()
        removeCharBtn.setIcon(QIcon('removechar.png'))
        self.tools.addWidget(removeCharBtn)
        removeCharBtn.clicked.connect(self._removeChar)

        # BTN Sort
        sortBtn = QPushButton()
        sortBtn.setIcon(QIcon('sort.png'))
        self.tools.addWidget(sortBtn)
        sortBtn.clicked.connect(self.orderList)

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
        self.effecRounds.addItems(conditionGeneralValue)
        self.btnApplyEffect = QPushButton('Apply')
        self.tools.addWidget(self.btnApplyEffect)

    # Upadate comboVal method
    def _updateCondVal(self):
        condition = self.condCombo.currentText()
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

    # Sort char method
    def orderList(self):
        """Crashing!!!"""
        initList = []

        for k in reversed(range(self.charBox.count())):
            self.charBox.removeWidget(self.charBox.itemAt(k))

        for i in self.charList:
            initList.append(i.init)

        initList.sort(reverse=True)

        for f in initList:
            for j in self.charList:
                if f == j.init:
                    self.charBox.addWidget(j.createWidget(j.position))

    # addchar method
    def _addChar(self):
        self.charCount = self.charCount + 1
        self._populateCharWidget(True)

    # removeChar method
    def _removeChar(self):
        if self.charCount > 1:
            self.charCount = self.charCount - 1
            self._populateCharWidget(False)
        else:
            pass

    # MainWindow CentralWidget definition
    def _createCentralWidget(self):
        """Central Widget"""
        centralWid = QWidget()

        # Scroll area and wrap widget definition
        charScroll = QScrollArea()          # Scroll Area which contains the wrapWidget and charWidgets
        charWrapWidget = QWidget()              # Widget that contains the collection of Vertical Box
        # Char widget vertical layout box
        self.charBox = QVBoxLayout()            # The Vertical Box that contains _charLayout
        self.charBox.setObjectName('charBox')
        self.charBox.addStretch(1)
        self.charCount = 1
        self.charList = []

        # Central layout of the Central widget
        layout = QVBoxLayout()
        layout.addWidget(self._roundWidget())           #Calling RoundInfo widget
        layout.addWidget(charScroll)

        for i in range(self.charCount):
            self._populateCharWidget(True)

        """Scroll Area Properties"""
        charWrapWidget.setLayout(self.charBox)
        charWrapWidget.setLayout(self.charBox)
        charScroll.setWidgetResizable(True)
        charScroll.setWidget(charWrapWidget)

        # centralWidget layout definition
        centralWid.setLayout(layout)
        self.setCentralWidget(centralWid)

    # PopulateCharWidget Method
    def _populateCharWidget(self, signal):

        if signal:
            per = personagem()
            per.position = int(len(self.charList))
            self.charList.append(per)
            self.charBox.addWidget(per.createWidget(per.position))  # Calling character widget
            print(self.charBox.count())
        elif not signal:
            self.charList.pop()
            self.charBox.itemAt(self.charBox.count()-1).widget().setParent(None)

    # RoundWidget definition
    def _roundWidget(self):
        """Top Widget: Informations before characters, called on _createCentralWidget"""

        # Round counter interface
        roundNumber = 0 # VAI PUXAR DA CLASSE RODADA QUE VAI ITERAR TODA VEZ QUE O TURNO DE TODOS OS PERSONAGENS FOREM IGUAL A RODADA + 1
        roundDisplay = QLabel(f"<h1>ROUND: {roundNumber}</h1>")
        # First line of roundDisplay layout
        roundDisplayLayout1 = QHBoxLayout()
        roundDisplayLayout1.addWidget(roundDisplay)
        roundDisplayLayout1.addStretch(1)

        # creates the line with the char's turn, actions e buttons to advance and return an turn / slash round
        # char's turn display
        charTurnDisplay = QLabel("<h2>Character's turn<h2>") # VAI PUXAR DO JOGADOR QUE ESTIVER COM O ATRIBUTO TURN = TRUE
       # improvised solution to align the label with the rest of the layout
        charTurnDisplay.setFixedHeight(20)
        charTurnDisplayLayout = QVBoxLayout()
        charTurnDisplayLayout.addStretch(10)
        charTurnDisplayLayout.addWidget(charTurnDisplay)
        charTurnDisplayLayout.addStretch(10)

        # previous turn button
        previousTurn = QPushButton(self)
        previousTurn.resize(24,24)
        previousTurn.setIcon(QIcon('circle-left.png'))
        previousTurn.setIconSize(QSize(24,24))

        # actions icons
        actionsNumber = 3 # TAMBÉM VAI PUXAR DO JOGADOR QUE ESTIVER COM O ATRIBUTO TURN = TRUE
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
        roundDisplayLayout2.addLayout(charTurnDisplayLayout)
        roundDisplayLayout2.addStretch(1)
        roundDisplayLayout2.addWidget(previousTurn)
        roundDisplayLayout2.addSpacing(10)
        roundDisplayLayout2.addLayout(actionLayout)
        roundDisplayLayout2.addWidget(nextTurn)

        # roundDisplay widget definition
        self.roundTopLayoutWidget = QWidget()
        self.roundTopLayoutWidget.setFixedHeight(85)
        # roundDisplayLayoutTop
        self.roundTopLayout = QVBoxLayout()
        self.roundTopLayoutWidget.setLayout(self.roundTopLayout)
        self.roundTopLayout.addLayout(roundDisplayLayout1)
        self.roundTopLayout.addLayout(roundDisplayLayout2)

        self.setLayout(self.roundTopLayout)
        return self.roundTopLayoutWidget

    # statusBar definition
    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Let's roll the dice")
        self.setStatusBar(status)

    # personagem class definition
class personagem(QWidget):
    def __init__(self, parent = None):
        super(personagem, self).__init__(parent)
        self.name = 'Personagem '
        self.ac = 0
        self.hp = 0
        self.init = 0
        # self.cond = {}
        # self.effect
        # self.footnote
        # self.reaction
        # self.turnBool
        self.actionNumber = 0
        self.position = 0

    # personagem label x lineEditmethod
    def textEdited(self):
        # If the input is left empty, revert back to the label showing
        if not self.charNameEdit.text():
            print(123312)
            self.charNameEdit.hide()
            self.charName.setText(f"<h1>{'Personagem' + str(self.position)}</h1>")
            self.charName.show()
        elif self.charNameEdit.text():
            self.charName.setText(f"<h1>{self.charNameEdit.text()}</h1>")
            self.charNameEdit.hide()
            self.charName.show()

    # HPmod calculation method
    def sumHP(self):
        hpModEmptyValue = 'Please, insert an HP MOD value'
        try:
            self.hp = self.hp + int(self.hpModLine.text())
        except Exception:
            self.messageBox = QMessageBox.warning(self, 'HP MOD', hpModEmptyValue)
        else:
            if self.hp < 0:
                self.hpDisplay.setText('0')
                self.hpModLine.setText('')
            else:
                self.hpDisplay.setText(str(self.hp))
                self.hpModLine.setText('')

    # ACTotal calculation method
    def sumAC(self):
        acModEmptyValue = 'Please, insert an AC TOTAL value'
        try:
            self.ac = self.ac + int(self.acTotalLine.text())
        except Exception:
            self.messageBox = QMessageBox.warning(self, 'AC TOTAL', acModEmptyValue)
        else:
            if self.ac < 0:
                self.acDisplay.setText('0')
                self.acTotalLine.setText('')
            else:
                self.acDisplay.setText(str(self.ac))
                self.acTotalLine.setText('')

    # personagem interface and layoyt method
    def createWidget(self, position):
        print(position)
        layoutV = QVBoxLayout()
        widgetMain = QWidget()
        widgetMain.setLayout(layoutV)
        layoutH1 = QHBoxLayout()
        widget1 = QWidget()
        widget1.setLayout(layoutH1)
        widget2 = QWidget()
        layoutH2 = QHBoxLayout()
        widget2.setLayout(layoutH2)
        widget3 = QWidget()
        layoutH3 = QHBoxLayout()
        widget3.setLayout(layoutH3)
        layoutV.addWidget(widget1)
        layoutV.addWidget(widget2)
        layoutV.addWidget(widget3)

        #Placing editable character name
        self.charNameEdit = QLineEdit()
        self.charNameEdit.setPlaceholderText('Nome do Personagem ')
        self.charNameEdit.hide()
        self.charNameEdit.editingFinished.connect(self.textEdited)
        self.charName = BuddyLabel(self.charNameEdit)
        self.charName.setText(f"<h1>{self.name + str(position)}</h1>")  # to be defined from a list with all characters in combat
        self.charName.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self.btn = QRadioButton()

        layoutH1.setSpacing(10)
        layoutH1.addWidget(self.btn)
        layoutH1.addWidget(self.charName)
        layoutH1.addWidget(self.charNameEdit)
        layoutH1.addStretch(1)
        charDisplayGrid = QGridLayout()
        layoutH1.addLayout(charDisplayGrid)

        """Defining all the widgets"""
        validador = QRegExpValidator(QRegExp("-?[0-9]{4}"))
        hp = QLabel('HP')           #Title HP
        hpMod = QLabel('HP MOD')    #Title HP MOD
        self.hpDisplay = QLabel(str(self.hp))   #Amount of HP, must be a variable to be changeable
        self.hpModLine = QLineEdit()     #Place to write the amount of HP to be deducted
        self.hpModLine.setValidator(validador)
        self.hpModLine.setFixedWidth(40)
        self.hpApply = QPushButton('Apply')
        self.hpApply.setFixedWidth(40)
        self.hpApply.clicked.connect(self.sumHP)
        ac = QLabel('AC')           #Title AC
        acTotal = QLabel('AC Total')#Title AC Total
        self.acDisplay = QLabel(str(self.ac))   #Amout of AC, must be a variable to be changeable
        self.acTotalLine = QLineEdit()   #Plave to write a valor of AC
        self.acTotalLine.setValidator(validador)
        self.acTotalLine.setFixedWidth(40)
        self.acApply = QPushButton('Apply')
        self.acApply.clicked.connect(self.sumAC)
        self.acApply.setFixedWidth(40)
        init = QLabel('Init')       #Title Init
        self.initLine = QLineEdit()      #Place to write Init, should be saved in a variable to be able to order characters
        self.initLine.setValidator(validador)
        self.initLine.setFixedWidth(40)
        self.initLine.editingFinished.connect(self.sumHP)


        """Placing all the widgets in a grid format"""
        charDisplayGrid.addWidget(hp, 0, 0)
        charDisplayGrid.addWidget(hpMod, 0, 1)
        charDisplayGrid.addWidget(ac, 0, 3)
        charDisplayGrid.addWidget(acTotal, 0, 4)
        charDisplayGrid.addWidget(init, 0, 6)
        charDisplayGrid.addWidget(self.hpDisplay, 1, 0)
        charDisplayGrid.addWidget(self.hpModLine, 1, 1)
        charDisplayGrid.addWidget(self.hpApply, 1, 2)
        charDisplayGrid.addWidget(self.acDisplay, 1, 3)
        charDisplayGrid.addWidget(self.acTotalLine, 1, 4)
        charDisplayGrid.addWidget(self.acApply, 1, 5)
        charDisplayGrid.addWidget(self.initLine, 1, 6)

        """Placing conditions and effects"""
        cond = QLabel('Condition 1')
        condPlus = QPushButton('+')
        condPlus.setFixedWidth(20)
        condMinus = QPushButton('-')
        condMinus.setFixedWidth(20)
        reactionBtn = QPushButton(self)
        reactionBtn.resize(24, 24)
        reactionBtn.setIcon(QIcon('reaction.png'))
        reactionBtn.setIconSize(QSize(24, 24))

        isCond = 1  # Variable to check if there is condition

        if isCond == True:
            layoutH2.addWidget(cond)
            layoutH2.addWidget(condPlus)
            layoutH2.addWidget(condMinus)

        layoutH2.addStretch(1)
        layoutH2.addWidget(reactionBtn)

        # Free space to write
        editText = QTextEdit()
        layoutH3.addWidget(editText)

        # # Setting character layout
        charlayout = QVBoxLayout()
        charlayoytWidget = QWidget()
        charlayoytWidget.setLayout(charlayout)
        charlayout.addWidget(widget1)
        charlayout.addWidget(widget2)
        charlayout.addWidget(widget3)

        return charlayoytWidget

# hide label, show line edit, edit label class
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

# ConditionData
conditionList = ['NA', 'Blinded', 'Broken(object)', 'Clumsy', 'Concealed','Confused', 'Controled', 'Dazzled', 'Deafened', 'Doomed','Drained', 'Dying', 'Encumbered', 'Enfleebed', 'Fascinated', 'Fatigued', 'Flat-Footed', 'Fleeing', 'Friendly', 'Frightened', 'Grabbed', 'Helpful', 'Hidden', 'Hostile', 'Immobilized', 'Indifferent', 'Invisible', 'Observed', 'Persistent Damage', 'Petrified', 'Prone', 'Quickened', 'Restrained', 'Sickened', 'Slowed', 'Stunned', 'Stupefied', 'Unconscious', 'Undetected', 'Unfriendly', 'Unnoticed', 'Wounded']
conditionGeneral = ['NA', 'Blinded', 'Broken(object)', 'Concealed','Confused', 'Controled', 'Dazzled', 'Deafened', 'Encumbered', 'Fascinated', 'Fatigued', 'Flat-Footed', 'Fleeing', 'Friendly', 'Grabbed', 'Helpful', 'Hidden', 'Hostile', 'Immobilized', 'Indifferent', 'Invisible', 'Observed', 'Petrified', 'Prone', 'Quickened', 'Restrained', 'Unconscious', 'Undetected', 'Unfriendly', 'Unnoticed']
conditionCount = ['Clumsy', 'Doomed','Drained', 'Dying', 'Enfleebed', 'Frightened', 'Sickened', 'Slowed', 'Stunned', 'Stupefied', 'Wounded']
# valueData
conditionGeneralValue = ['NA', '1 round', '2 rounds', '3 rounds', '4 rounds', '5 rounds', '6 rounds', '10 rounds', '20 rounds', 'other']
conditionCountValue = ['NA', '1', '2', '3', '4', '5']
persistentDamageValue = ['NA', '1d4', '2d4', '3d4', '1d6', '2d6', '3d6', '1d8', '2d8', 'other']

# window creation
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())