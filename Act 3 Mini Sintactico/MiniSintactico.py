import sys
import re
from Lexico import analizador_Lexico
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

class analizador_Sintactico():

    def __init__(self):
        self.tokens = list()
        self.pila = list()
        self.entrada = list()
        self.header = int()
        self.gramatica1 =    [
                        ["Id", "OpSuma", "$", "E"],
                        ["d2", 0, 0, "1"],
                        [0, 0, "r0", 0],
                        [0, "d3", 0, 0],
                        ["d4", 0, 0, 0],
                        [0, 0, "r1", 0]
                        ]
        self.rules =    [
                        "End",
                        [["Id", "OpSuma", "Id"], 3, "E"]
                        ]

    def analize(self, tokens) -> list:
        self.pila.clear()
        self.entrada.clear()
        pila_Tok = []
        res = []
        for a in tokens:
            self.entrada.insert(0, a[0])
        self.entrada.insert(0, "$")
        tokens.append(["$", "$"])
        self.pila.append("$0")
        res.append([''.join(self.pila), ''.join(reversed(self.entrada)), "0"])
        self.header = 0
        header = 0
        while self.pila:
            if tokens[self.header][1] in self.gramatica1[0]:
                step = self.gramatica1[header+1][self.gramatica1[0].index(tokens[self.header][1])]
                if step:
                    if 'd' in step:
                        step = int(step[1:])
                        self.pila.append(f"{tokens[self.header][0]}{step}")
                        pila_Tok.append(tokens[self.header][1])
                        header = step
                        self.header += 1
                        self.entrada.pop()
                        res.append([''.join(self.pila), ''.join(reversed(self.entrada)), f"d{step}"])
                    elif 'r' in step:
                        rule = self.rules[int(step[1:])]
                        if rule == "End":
                            self.pila.pop()
                            res.append([''.join(self.pila), ''.join(reversed(self.entrada)), "r1 accepted"])
                            break
                        if rule[0] == pila_Tok[-3:]:
                            for a in range(rule[1]):
                                pila_Tok.pop()
                                self.pila.pop()
                            header = int(self.pila[-1][1:])
                            if self.gramatica1[header + 1][self.gramatica1[0].index(rule[2])]:
                                self.pila.append(f"E{self.gramatica1[header + 1][self.gramatica1[0].index(rule[2])]}")
                                tokens.insert(self.header, ["E", "E"])
                            res.append([''.join(self.pila), ''.join(reversed(self.entrada)), step])
                        else:
                            res.append([''.join(self.pila), ''.join(reversed(self.entrada)), "Error"])
                            break
                    else:
                        header = int(step)
                        self.header += 1

                else:
                    res.append([''.join(self.pila), ''.join(reversed(self.entrada)), "Error"])
                    break
            else:
                res.append([''.join(self.pila), ''.join(reversed(self.entrada)), "Error"])
                break
        print(pila_Tok)
        return res


class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Sintactico")
        self.setStyleSheet(Main_SS)
        self.Screen = app.primaryScreen().size()
        self.setGeometry(self.Screen.width()/16, self.Screen.height()/8,
                         self.Screen.width()/16*14, self.Screen.height()/8*6)
        self.uiComponents()
        self.show()

    @Slot()
    def entered(self):
        if self.lnEd_In.text():
            tokens = a_Lex.analize(self.lnEd_In.text())
            res = a_Sint.analize(tokens)
            self.tbl_Res.setRowCount(len(res))
            for x, a in enumerate(res):
                for y, b in enumerate(a):
                    item = QTableWidgetItem()
                    item.setText(b)
                    item.setToolTip(b)
                    item.setFont(QFont("Verdana", 16))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tbl_Res.setItem(x, y, item)
        else:
            self.tbl_Res.clearContents()
            self.tbl_Res.setRowCount(0)



    def uiComponents(self):
        self.lnEd_In = QLineEdit("Hola + Mundo", self)
        self.lnEd_In.setGeometry(self.size().width() / 8, self.size().height() / 8,
                                 self.size().width() / 8 * 6, 30)
        self.lnEd_In.returnPressed.connect(self.entered)

        self.tbl_Res = QTableWidget(self)
        self.tbl_Res.setGeometry(self.size().width() / 8, self.size().height() / 8 * 2,
                                 self.size().width() / 8 * 6, self.size().height() / 8 * 5)
        self.tbl_Res.setColumnCount(3)
        for a in range(3):
            self.tbl_Res.setColumnWidth(a, (self.tbl_Res.width() - 20) / 3 )
        self.tbl_Res.setHorizontalHeaderLabels(["Pila", "Entrada", "Salida"])
        self.tbl_Res.horizontalScrollBar().close()
        self.tbl_Res.verticalHeader().close()
        self.tbl_Res.setEditTriggers(QAbstractItemView.NoEditTriggers)

if __name__ == "__main__":
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
    test1 =  [
                ["Hola", "Id"],
                ["+", "OpSuma"],
                ["Mundo", "Id"]
            ]

    a_Sint = analizador_Sintactico()
    a_Lex = analizador_Lexico()

    app = QApplication(sys.argv)
    main_Window = mainWindow()
    app.exec()