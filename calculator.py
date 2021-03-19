import sys

from functools import partial

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout

class PyCalculator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Calculator")
        self.setFixedSize(235, 235)

        self.generalLayout = QVBoxLayout()
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        self._createDisplay()
        self._createButtons()

    def _createDisplay(self):
        self.display = QLineEdit()

        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)

        self.generalLayout.addWidget(self.display)

    def _createButtons(self):
        self.buttons = {}
        buttonsLayout = QGridLayout()

        # button: position on layout
        # this buttons variable is going to be used for defining the layout
        # != self.buttons
        buttons = {
            "7" : (0,0), "8" : (0,1), "9" : (0,2), "/" : (0,3), "c" : (0,4),
            "4" : (1,0), "5" : (1,1), "6" : (1,2), "*" : (1,3), "(" : (1,4),
            "1" : (2,0), "2" : (2,1), "3" : (2,2), "-" : (2,3), ")" : (2,4),
            "0" : (3,0), "00": (3,1), "." : (3,2), "+" : (3,3), "=" : (3,4)
        }

        for btnText, pos in buttons.items():
            self.buttons[btnText] = QPushButton(btnText)
            self.buttons[btnText].setFixedSize(40, 40)
            buttonsLayout.addWidget(self.buttons[btnText], pos[0], pos[1])
        
        self.generalLayout.addLayout(buttonsLayout)

    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()

    def displayText(self):
        return self.display.text()

    def clearDisplay(self):
        self.setDisplayText("")

class PyCalculatorBrain:
    def __init__(self, view, error_message="ERROR"):
        self._view = view
        self._connectSignals()
        self._error_message = error_message

    def _evaluateExpression(self, expression):
        try:
            result = str(eval(expression, {}, {}))
        except Exception:
            result = self._error_message
        return result

    def _calculateResult(self):
        result = self._evaluateExpression(expression=self._view.displayText())
        self._view.setDisplayText(result)

    def _buildExpression(self, sub_exp):
        if self._view.displayText() == self._error_message:
            self._view.clearDisplay()

        expression = self._view.displayText() + sub_exp
        self._view.setDisplayText(expression)

    def _connectSignals(self):
        for btnText, btn in self._view.buttons.items():
            if btnText not in {"=" , "c"}:
                btn.clicked.connect(partial(self._buildExpression, btnText))
        
        self._view.buttons["c"].clicked.connect(self._view.clearDisplay)
        self._view.buttons["="].clicked.connect(self._calculateResult)
        self._view.display.returnPressed.connect(self._calculateResult)

def main():
    calculator = QApplication([])
    view = PyCalculator()
    view.show()

    PyCalculatorBrain(view=view)
    sys.exit(calculator.exec())

if __name__ == "__main__":
    main()
