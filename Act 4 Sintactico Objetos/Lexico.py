import sys
import re
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class analizador_Lexico:
    text = str
    header = int
    tokens = list
    rs_Words = ["Tipo", ["int", "float", "void"],
                "if", ["if"],
                "while", ["while"],
                "else", ["else"],
                "return", ["return"]
               ]

    def analize(self, text) -> list:
        self.text = text
        self.header = 0
        self.tokens = []
        self.t_Len = len(self.text)
        while self.header < self.t_Len:
            self.getToken()
        return self.tokens

    def getToken(self):
        pre = self.preanalisis()
        if pre:
            token = self.coincidir(pre)
            self.tokens.append(token)

    def preanalisis(self) -> str:
        pre = re.match(r" *[^ ]+", self.text[self.header:])
        if pre:
            if "\"" in pre[0]:
                if re.match(r" *\".*\"", self.text[self.header:]):
                    pre = re.match(r" *\".*\"", self.text[self.header:])
            return pre[0]
        else:
            pre = re.match(r" *", self.text[self.header:])
            self.header += len(pre[0])
            return ""

    def coincidir(self, pre) -> list:
        rsw_Tok = ""
        token = ""
        simbol = ""
        if re.match(r" *[^a-zA-Z\d+\-*/|!{}()=<>&^;,\" ]", pre):
            simbol = re.match(r" *[^a-zA-Z\d+\-*/|!{}()=<>&^;,\" ]+", pre)[0]
            token = "Error"
            self.header += len(simbol)
            return [simbol, token]
        for words in self.rs_Words:
            if isinstance(words, str):
                rsw_Tok = words
                continue
            else:
                for word in words:
                    if re.fullmatch(r" *" + word, pre):
                        token = rsw_Tok
                        simbol = re.fullmatch(r" *" + word, pre)[0]
                        self.header += len(simbol)
                        return [simbol, token]
        if re.match(r" *[a-zA-Z][a-zA-Z\d]*", pre):
            simbol = re.match(r" *[a-zA-Z][a-zA-Z\d]*", pre)[0]
            self.header += len(simbol)
            token = "Id"
        elif re.match(r" *\d+\.\d+", pre):
            simbol = re.match(r" *\d+\.\d+", pre)[0]
            if simbol.count(".") > 1:
                token = "Error"
                self.header += len(pre)
            elif len(simbol) == pre.rfind(".") + 1:
                token = "Error"
            else:
                self.header += len(simbol)
                token = "Real"
        elif re.match(r" *\d+", pre):
            simbol = re.match(r" *\d+", pre)[0]
            self.header += len(simbol)
            token = "Entero"
        elif re.match(r" *\".*\"", pre):
            simbol = re.match(r" *\".*\"", pre)[0]
            self.header += len(simbol)
            token = "Cadena"
        elif re.match(r" *[+\-]", pre):
            simbol = re.match(r" *[+\-]", pre)[0]
            self.header += len(simbol)
            token = "OpSuma"
        elif re.match(r" *[*/]", pre):
            simbol = re.match(r" *[*/]", pre)[0]
            self.header += len(simbol)
            token = "OpMul"
        elif re.match(r" *(>|<|>=|<=)", pre):
            simbol = re.match(r" *(>|<|>=|<=)?", pre)[0]
            self.header += len(simbol)
            token = "OpRelac"
        elif re.match(r" *(!=|==)", pre):
            simbol = re.match(r" *(!=|==)", pre)[0]
            self.header += len(simbol)
            token = "OpIgualdad"
        elif re.match(r" *=", pre):
            simbol = re.match(r" *=", pre)[0]
            self.header += len(simbol)
            token = "OpAsignacion"
        elif re.match(r" *&&", pre):
            simbol = re.match(r" *&&", pre)[0]
            self.header += len(simbol)
            token = "OpAnd"
        elif re.match(r" *\|\|", pre):
            simbol = re.match(r" *\|\|", pre)[0]
            self.header += len(simbol)
            token = "OpOr"
        elif re.match(r" *!", pre):
            simbol = re.match(r" *!", pre)[0]
            self.header += len(simbol)
            token = "OpNot"
        elif re.match(r" *[()]", pre):
            simbol = re.match(r" *[()]", pre)[0]
            self.header += len(simbol)
            token = "Parentesis"
        elif re.match(r" *[{}]", pre):
            simbol = re.match(r" *[{}]", pre)[0]
            self.header += len(simbol)
            token = "Llaves"
        elif re.match(r" *;", pre):
            simbol = re.match(r" *;", pre)[0]
            self.header += len(simbol)
            token = "Punto y Coma"
        elif re.match(r" *,", pre):
            simbol = re.match(r" *,", pre)[0]
            self.header += len(simbol)
            token = "Coma"
        elif re.match(r" *=", pre):
            simbol = re.match(r" *=", pre)[0]
            self.header += len(simbol)
            token = "Igual"
        if not token:
            token = "Error"
            simbol = pre
            self.header += len(pre)
        if token != "Cadena":
            simbol = simbol.replace(" ","")
        return [simbol, token]

class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lexico")
        self.setStyleSheet(main_SS)
        self.Screen = app.primaryScreen().size()
        self.setGeometry(self.Screen.width()/16*4, self.Screen.height()/8,
                         self.Screen.width()/16*8, self.Screen.height()/8*6)
        self.uiComponents()
        self.show()

    @Slot()
    def entered(self):
        if self.sender() is self.lnEd_In:
            An_L.analize(self.lnEd_In.text())
            x = 0
            self.tbl_Res.setRowCount(len(An_L.tokens))
            for a in An_L.tokens:
                item = QTableWidgetItem()
                item.setText(a[0])
                item.setToolTip(a[0])
                item.setFont(QFont("Verdana", 16))
                item.setTextAlignment(Qt.AlignCenter)
                self.tbl_Res.setItem(x, 0, item)

                item = QTableWidgetItem()
                item.setText(a[1])
                item.setToolTip(a[1])
                item.setFont(QFont("Verdana", 16))
                item.setTextAlignment(Qt.AlignCenter)
                self.tbl_Res.setItem(x, 1, item)
                x += 1

    def uiComponents(self):
        self.lnEd_In = QLineEdit(self)
        self.lnEd_In.setGeometry(self.size().width() / 8, self.size().height() / 8,
                                 self.size().width() / 8 * 6, 30)
        self.lnEd_In.returnPressed.connect(self.entered)

        self.tbl_Res = QTableWidget(self)
        self.tbl_Res.setGeometry(self.size().width() / 8, self.size().height() / 8 * 2,
                                 self.size().width() / 8 * 6, self.size().height() / 8 * 5)
        self.tbl_Res.setColumnCount(2)
        for a in range(2):
            self.tbl_Res.setColumnWidth(a, self.tbl_Res.width() / 2 - 10)
        self.tbl_Res.setHorizontalHeaderLabels(["Campo", "Tipo"])
        self.tbl_Res.horizontalScrollBar().close()
        self.tbl_Res.verticalHeader().close()
        self.tbl_Res.setEditTriggers(QAbstractItemView.NoEditTriggers)

if __name__ == "__main__":
    An_L = analizador_Lexico()

    main_SS = "QMainWindow {" \
              "color: #fff;" \
              "font: bold; " \
              "border: 2px solid #555; " \
              "border-radius: 3px; " \
              "border-style: outset; " \
              "background: qradialgradient(" \
              "cx: 0.5, cy: 0.0, fx: 0.5, fy: 0.5, radius: 1, stop: 0 #76A5AF, stop: 0.5 #45818E);" \
              "padding: 1px;" \
              "}" \
              "QPushButton {" \
              "color: #fff;" \
              "font: bold; " \
              "border: 2px solid #555; " \
              "border-radius: 3px; " \
              "border-style: outset; " \
              "background: qradialgradient(" \
              "cx: 0.5, cy: -0.5, fx: 0.5, fy: -0.4, radius: 1.50, stop: 0 #fff, stop: 1 #000);" \
              "padding: 1px;" \
              "}" \
              "QLineEdit {" \
              "color: #000;" \
              "font: bold; " \
              "border: 2px solid #555; " \
              "border-radius: 10px; " \
              "border-style: outset; " \
              "background: #FFF;" \
              "padding: 1px;" \
              "}" \
              "QTableWidget {" \
              "color: #fff;" \
              "background-color: #76A5AF;" \
              "padding: 1px;" \
              "}" \
              "QLabel {" \
              "color: #fff;" \
              "font: 15pt verdana bold; " \
              "}" \
              "QCheckBox {" \
              "color: #fff;" \
              "font: bold;" \
              "}" \
              "QMessageBox {" \
              "background-color: #76A5AF;" \
              "}"

    app = QApplication(sys.argv)
    main_Window = mainWindow()
    app.exec()