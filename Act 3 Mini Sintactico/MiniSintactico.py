import sys
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
        self.gramatica1 = [
            ["Id", "OpSuma", "$", "E"],
            ["d2", 0, 0, "1"],
            [0, 0, "r0", 0],
            [0, "d3", 0, 0],
            ["d4", 0, 0, 0],
            [0, 0, "r1", 0]
        ]
        self.rules1 = [
            ["End", 0, ""],
            [["Id", "OpSuma", "Id"], 3, "E"]
        ]
        self.gramatica2 = [
            ["Id", "OpSuma", "$", "E"],
            ["d2", 0, 0, "1"],
            [0, 0, "r0", 0],
            [0, "d3", "r2", 0],
            ["d2", 0, 0, "4"],
            [0, 0, "r1", 0]
        ]
        self.rules2 = [
            ["End", 0, ""],
            [["Id", "OpSuma", "E"], 3, "E"],
            [["Id"], 1, "E"]
        ]

    def analize(self, tokens, gramatica, rules) -> list:
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
            if tokens[self.header][1] in gramatica[0]:
                step = gramatica[header + 1][gramatica[0].index(tokens[self.header][1])]
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
                        rule = rules[int(step[1:])]
                        if rule == "End":
                            self.pila.pop()
                            res.append([''.join(self.pila), ''.join(reversed(self.entrada)), "r0 accepted"])
                            break
                        if rule[0] == pila_Tok[-rule[1]:]:
                            for a in range(rule[1]):
                                pila_Tok.pop()
                                self.pila.pop()
                            header = int(self.pila[-1][1:])
                            if gramatica[header + 1][gramatica[0].index(rule[2])]:
                                self.pila.append(f"E{gramatica[header + 1][gramatica[0].index(rule[2])]}")
                                pila_Tok.append("E")
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
        return res

class mainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Sintactico")
        self.setStyleSheet(Main_SS)
        self.Screen = app.primaryScreen().size()
        self.setGeometry(self.Screen.width() / 16, self.Screen.height() / 8,
                         self.Screen.width() / 16 * 14, self.Screen.height() / 8 * 6)
        self.uiComponents()
        self.show()

    @Slot()
    def entered(self):
        gram = self.lst_Gram.item(self.lst_Gram.selectedIndexes()[0].row()).text()
        if self.lnEd_In.text() and gram:
            tokens = a_Lex.analize(self.lnEd_In.text())
            res = []
            if gram == "Gramatica 1":
                res = a_Sint.analize(tokens, a_Sint.gramatica1, a_Sint.rules1)
            elif gram == "Gramatica 2":
                res = a_Sint.analize(tokens, a_Sint.gramatica2, a_Sint.rules2)
            self.tbl_Res.setRowCount(len(res))
            for x, a in enumerate(res):
                for y, b in enumerate(a):
                    item = QTableWidgetItem()
                    item.setText(b)
                    item.setToolTip(b)
                    item.setFont(QFont("Verdana", 14))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tbl_Res.setItem(x, y, item)
        else:
            self.tbl_Res.clearContents()
            self.tbl_Res.setRowCount(0)

    @Slot()
    def moved(self, action):
        row = self.lst_Gram.selectedIndexes()[0].row()
        if action == 1:
            if row < 2:
                row += 1
        elif action == 2:
            if row > 0:
                row -= 1
        self.lst_Gram.item(row).setSelected(True)
        self.tbl_Gram.show()
        gram = []
        rule = []
        if self.lst_Gram.item(row).text() == "Gramatica 1":
            gram = a_Sint.gramatica1
            rule = a_Sint.rules1
        elif self.lst_Gram.item(row).text() == "Gramatica 2":
            gram = a_Sint.gramatica2
            rule = a_Sint.rules2
        else:
            self.tbl_Gram.clear()
            self.tbl_Gram.close()
            self.tbl_Rul.clear()
            self.tbl_Rul.close()
        if gram:
            self.tbl_Gram.setColumnCount(len(gram[0]))
            self.tbl_Gram.setRowCount(len(gram) - 1)
            self.tbl_Gram.setHorizontalHeaderLabels(gram[0])
            self.tbl_Gram.adjustSize()
            for x, a in enumerate(gram):
                if x == 0:
                    continue
                for y, b in enumerate(a):
                    item = QTableWidgetItem(str(b))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tbl_Gram.setItem(x - 1, y, item)

        for a in range(self.tbl_Gram.columnCount()):
            self.tbl_Gram.setColumnWidth(a, (self.tbl_Gram.width() - 20) / self.tbl_Gram.columnCount())
        self.tbl_Gram.setVerticalHeaderLabels([str(a) for a in range(self.tbl_Gram.rowCount())])

        if rule:
            self.tbl_Rul.setRowCount(len(rule))
            for x, a in enumerate(rule):
                for y, b in enumerate(a):
                    item = QTableWidgetItem(str(b))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.tbl_Rul.setItem(x, y, item)


        geo = self.tbl_Gram.geometry()
        geo.setY(geo.y() + geo.height() + 20)
        geo.setHeight( 50 + len(rule) * 30)
        geo.setWidth(self.size().width() / 8 * 2 - 20)
        self.tbl_Rul.setVerticalHeaderLabels([str(a) for a in range(len(rule))])
        self.tbl_Rul.setGeometry(geo)
        self.tbl_Rul.show()


    def uiComponents(self):
        self.lnEd_In = QLineEdit("a+b+c+d+e+f", self)
        self.lnEd_In.setGeometry(self.size().width() / 16, self.size().height() / 32 * 4,
                                 self.size().width() / 16 * 10, 30)
        self.lnEd_In.returnPressed.connect(self.entered)

        self.lst_Gram = QListWidget(self)
        self.lst_Gram.setGeometry(self.size().width() / 16, self.size().height() / 32 * 6,
                                  self.size().width() / 16 * 2, 30)
        self.lst_Gram.addItem(QListWidgetItem(""))
        self.lst_Gram.addItem(QListWidgetItem("Gramatica 1"))
        self.lst_Gram.addItem(QListWidgetItem("Gramatica 2"))
        for a in range(self.lst_Gram.count()):
            self.lst_Gram.item(a).setFont(QFont("verdana", 16))
        self.lst_Gram.item(0).setSelected(True)
        self.lst_Gram.verticalScrollBar().actionTriggered.connect(self.moved)

        self.tbl_Res = QTableWidget(self)
        self.tbl_Res.setGeometry(self.size().width() / 16, self.size().height() / 32 * 8,
                                 self.size().width() / 16 * 10, self.size().height() / 8 * 5)
        self.tbl_Res.setColumnCount(3)
        for a in range(3):
            self.tbl_Res.setColumnWidth(a, (self.tbl_Res.width() - 20) / 3)
        self.tbl_Res.setHorizontalHeaderLabels(["Pila", "Entrada", "Salida"])
        self.tbl_Res.horizontalScrollBar().close()
        self.tbl_Res.verticalHeader().close()
        self.tbl_Res.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tbl_Gram = QTableWidget(self)
        self.tbl_Gram.setGeometry(self.size().width() / 32 * 23, self.size().height() / 32 * 8, 0, 0)
        self.tbl_Gram.close()

        self.tbl_Rul = QTableWidget(self)
        self.tbl_Rul.setColumnCount(3)
        self.tbl_Rul.setHorizontalHeaderLabels(["Regla", "Pop´s", "Resultado"])
        self.tbl_Rul.verticalScrollBar().close()
        self.tbl_Rul.close()

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

    a_Sint = analizador_Sintactico()
    a_Lex = analizador_Lexico()

    app = QApplication(sys.argv)
    main_Window = mainWindow()
    app.exec()
