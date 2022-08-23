import sys
import re
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class AnalizadorLexico:
    text = str
    header = int
    tokens = list

    def analize(self, text):
        self.text = text
        self.header = 0
        self.tokens = []
        self.t_Len = len(self.text)
        while self.header < self.t_Len:
            self.id()

    def id(self) -> None:
        pre = self.preanalisis()
        if re.match(r" *\d", pre):
            self.real()
            return
        if pre:
            pre = self.coincidir("Id", pre)

    def real(self) -> None:
        pre = self.preanalisis()
        pre = self.coincidir("Real", pre)

    def preanalisis(self) -> str:
        pre = re.match(r" *[^ ]+", self.text[self.header:])
        if pre:
            return pre[0]
        else:
            pre = re.match(r" *", self.text[self.header:])
            self.header += len(pre[0])
            return ""

    def coincidir(self, type, pre) -> str:
        self.header += len(pre)
        if type == "Id":
            tok = "Id"
            if re.findall(r"[^a-zA-Z\d ]", pre):
                tok = "Error"
            self.tokens.append([str(pre).replace(" ", ""), tok])
        elif type == "Real":
            tok = "Real"
            if pre.count(".") > 1:
                tok = "Error"
            elif re.findall(r"[^\d. ]", pre):
                tok = "Error"
            self.tokens.append([str(pre).replace(" ", ""), tok])
        return pre

class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Lexico")
        self.setStyleSheet(Main_SS)
        self.Screen = app.primaryScreen().size()
        self.setGeometry(self.Screen.width()/8*3, self.Screen.height()/4,
                         self.Screen.width()/4, self.Screen.height()/4*2)
        self.uiComponents()
        self.show()

    @Slot()
    def Entered(self):
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
        self.lnEd_In.returnPressed.connect(self.Entered)

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

    Main_SS = "QMainWindow {" \
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


