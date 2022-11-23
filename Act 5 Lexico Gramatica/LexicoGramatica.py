import csv
import sys
import re
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class AnalizadorLexico:
    def __init__(self):
        self.Text = str
        self.Header = int
        self.Tokens = list
        self.ResolveTokens()

    def ResolveTokens(self):
        Re = []
        with open("Gramatica/Tokens.csv", "r") as TFile:
            CsvT = csv.reader(TFile)
            for Line in CsvT:
                Re.append(Line)
        Rw = []
        with open("Gramatica/RsWords.csv", "r") as RFile:
            CsvR = csv.reader(RFile)
            for Line in CsvR:
                L = [Line[0], Line[1][1:-1].replace("'","").split(",")]
                Rw.append(L)
        self.RePatts = Re
        self.RsWords = Rw



    def Analize(self, text):
        self.Text = text
        self.Header = 0
        self.Tokens = []
        self.t_Len = len(self.Text)
        while self.Header < self.t_Len:
            self.GetToken()
        return self.Tokens

    def GetToken(self):
        Pre = self.Preanalisis()
        if Pre:
            Token = self.Coincidir(Pre)
            self.Tokens.append(Token)

    def Preanalisis(self) -> str:
        Pre = re.match(r" *[^ ]+", self.Text[self.Header:])
        if Pre:
            if "\"" in Pre[0]:
                if re.match(r" *\".*\"", self.Text[self.Header:]):
                    Pre = re.match(r" *\".*\"", self.Text[self.Header:])
            return Pre[0]
        else:
            Pre = re.match(r" *", self.Text[self.Header:])
            self.Header += len(Pre[0])
            return ""

    def Coincidir(self, pre) -> list:
        Token = ""
        Simbol = ""
        if re.match(r" *[^a-zA-Z\d+\-*/|!{}()=<>&^;,\" ]", pre):
            Simbol = re.match(r" *[^a-zA-Z\d+\-*/|!{}()=<>&^;,\" ]+", pre)[0]
            Token = "Error"
            self.Header += len(Simbol)
        if not Token:
            for Word in self.RsWords:
                for ReWords in Word[1]:
                    if re.fullmatch(r" *" + ReWords, pre):
                        Token = Word[0]
                        Simbol = re.fullmatch(r" *" + ReWords, pre)[0]
                        self.Header += len(Simbol)
                        break
        if not Token:
            for Word in self.RePatts:
                if re.match(r" *" + Word[1], pre):
                    Token = Word[0]
                    Simbol = re.match(r" *" + Word[1], pre)[0]
                    self.Header += len(Simbol)
                    break
        if not Token:
            Token = "Error"
            Simbol = pre
            self.Header += len(pre)
        if Token != "Cadena":
            Simbol = Simbol.replace(" ","")
        return [Simbol, Token]

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lexico")
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
        self.setStyleSheet(main_SS)
        self.Screen = App.primaryScreen().size()
        self.setGeometry(self.Screen.width()/16*4, self.Screen.height()/8,
                         self.Screen.width()/16*8, self.Screen.height()/8*6)
        self.uiComponents()
        self.show()

    @Slot()
    def entered(self):
        if self.sender() is self.lnEd_In:
            An_L.Analize(self.lnEd_In.text())
            x = 0
            self.tbl_Res.setRowCount(len(An_L.Tokens))
            for a in An_L.Tokens:
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
    An_L = AnalizadorLexico()
    App = QApplication(sys.argv)
    main_Window = MainWindow()
    App.exec()