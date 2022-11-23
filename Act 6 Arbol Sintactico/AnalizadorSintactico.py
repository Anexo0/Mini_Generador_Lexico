import sys

import networkx as nx
import matplotlib.pyplot as plt

from LexicoGramatica import AnalizadorLexico
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from csv import reader
from os import listdir, remove

class NoTerminal():
    def __init__(self, elemento, elementos, estado, token):
        self.Elemento = elemento
        self.Elementos = elementos
        self.Estado = estado
        self.Token = token

    def __str__(self):
        string = f"{self.Elemento}({self.Token})\n"
        for a in self.Elementos:
            string += f"{str(a)}\t"
        return string

    def GetNodes(self):
        Nodes = [str(self.Elemento)]
        Sons = []
        for Elem in self.Elementos:
            if isinstance(Elem, NoTerminal):
                Sons += [Elem.GetNodes()]
            else:
                Sons += [str(Elem.Elemento)]
        if not self.Elementos:
            Nodes += [self.Elementos]
        if Sons:
            Nodes += Sons
        return Nodes

class Terminal():
    def __init__(self, elemento, estado, token):
        self.Elemento = elemento
        self.Estado = estado
        self.Token = token

    def __str__(self):
        return f"{self.Elemento} ({self.Token})"

class AnlaizadorSintactico():

    def __init__(self):
        self.Tokens = list()
        self.Pila = list()
        self.Entrada = list()
        self.Header = int()
        self.Gram = self.ResolveGram()
        self.Rules = self.ResolveRules()

    def Analize(self, Tokens) -> list:
        self.Pila.clear()
        self.Entrada.clear()
        Res = []
        for a in Tokens:
            self.Entrada.insert(0, a[0])
        self.Entrada.insert(0, "$")
        Tokens.append(["$", "$"])
        self.Pila.append(Terminal("$", "e0", "$"))
        PText = "".join([f"{a.Elemento}{a.Estado}" for a in self.Pila])
        Res.append([PText, ''.join(reversed(self.Entrada)), "0"])
        self.Header = 0
        Header = 0
        while True:
            if Tokens[self.Header][1] in self.Gram[0]:
                Step = self.Gram[Header + 1][self.Gram[0].index(Tokens[self.Header][1])]
                if Step:
                    if 'd' in Step:
                        self.Pila.append(Terminal(Tokens[self.Header][0], Step, Tokens[self.Header][1]))
                        Step = int(Step[1:])
                        Header = Step
                        self.Header += 1
                        self.Entrada.pop()
                        PText = "".join([f"{a.Elemento}{a.Estado[1:]}" for a in self.Pila])
                        Res.append([PText, "".join(reversed(self.Entrada)), f"d{Step}"])
                    elif 'r' in Step:
                        Rule = self.Rules[int(Step[1:])]
                        if Step == "r0":
                            PText = "".join([f"{a.Elemento}{a.Estado[1:]}" for a in self.Pila])
                            Res.append([PText, ''.join(reversed(self.Entrada)), "r0 accepted"])
                            Res.append(self.Pila.pop())
                            break
                        if Rule[0] == [a.Token for a in self.Pila[-Rule[1]:]] or not Rule[1]:
                            Elements = []
                            for a in range(Rule[1]):
                                Elements.insert(0, self.Pila.pop())
                            Header = int(self.Pila[-1].Estado[1:])
                            Step2 = self.Gram[Header + 1][self.Gram[0].index(Rule[2])]
                            if Step2:
                                self.Pila.append(NoTerminal(Rule[2], Elements, f"s{Step2}", Rule[2]))
                                Tokens.insert(self.Header, [Rule[2], Rule[2]])
                            PText = "".join([f"{a.Elemento}{a.Estado[1:]}" for a in self.Pila])
                            Res.append([PText, "".join(reversed(self.Entrada)), Step])
                        else:
                            Pila = list(map(self.ToString, self.Pila))
                            Res.append([''.join(Pila), ''.join(reversed(self.Entrada)), "Error"])
                            Res.append("Error")
                            break
                    else:
                        Header = int(Step)
                        Last = Header
                        self.Header += 1
                        PText = "".join([f"{a.Elemento}{a.Estado[1:]}" for a in self.Pila])
                        Res.append([PText, "".join(reversed(self.Entrada)), Step])

                else:
                    Pila = list(map(self.ToString, self.Pila))
                    Res.append([''.join(Pila), ''.join(reversed(self.Entrada)), "Error"])
                    Res.append("Error")
                    break
            else:
                Pila = list(map(self.ToString, self.Pila))
                Res.append([''.join(Pila), ''.join(reversed(self.Entrada)), "Error"])
                Res.append("Error")
                break
        return Res

    def ToString(self, Item:Terminal):
        return f"{Item.Elemento}{Item.Estado[1:]}"
    def ToGram(slef, Token):
        if not Token:
            return 0
        return Token
    def ResolveGram(self):
        Gram = []
        with open("Gramatica/Gramatica.csv") as GrFile:
            GrCsv = reader(GrFile)
            for Row in GrCsv:
                Gr = list(map(self.ToGram, Row))
                Gram.append(Gr)
        return Gram
    def ResolveRules(self):
        Rules = []
        with open("Gramatica/Rules.csv") as RlFile:
            RlCsv = reader(RlFile, delimiter="|")
            for i, Row in enumerate(RlCsv, 1):
                Rule = [Row[1].split(" "), int(Row[2]), Row[0]]
                Rules.append(Rule)
        return Rules

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sintactico Objetos")
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
                  "}" \
                  "QTabWidget::pane {" \
                  "    border-top: 2px solid #C2C7CB;" \
                  "}" \
                  "QTabWidget::tab-bar {" \
                  "    left: 5px;" \
                  "}" \
                  "QTabBar::tab {" \
                  "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1," \
                  "                                stop: 0 #E1E1E1, stop: 0.4 #DDDDDD," \
                  "                                stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);" \
                  "    border: 2px solid #C4C4C3;" \
                  "    border-bottom-color: #C2C7CB;" \
                  "    border-top-left-radius: 4px;" \
                  "    border-top-right-radius: 4px;" \
                  "    min-width: 8ex;" \
                  "    padding: 2px;" \
                  "}" \
                  "QTabBar::tab:selected, QTabBar::tab:hover {" \
                  "    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1," \
                  "                                stop: 0 #fafafa, stop: 0.4 #f4f4f4," \
                  "                                stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);" \
                  "}" \
                  "QTabBar::tab:selected {" \
                  "    border-color: #9B9B9B;" \
                  "    border-bottom-color: #C2C7CB;" \
                  "}" \
                  "QTabBar::tab:!selected {" \
                  "    margin-top: 2px;" \
                  "}"
        self.setStyleSheet(Main_SS)
        self.Screen = App.primaryScreen().size()
        self.UiComponents()
        self.showMaximized()
        ##################
        #self.Pressed()
        #quit(0)
        ##################

    @Slot()
    def Pressed(self):
        with open(self.CbbxInput.itemText(self.CbbxInput.currentIndex())) as File:
            plt.close()
            Text = File.read().replace("\n", "")
            Tokens = AnLex.Analize(Text)
            Res = AnSin.Analize(Tokens)
            Arbol = Res.pop()
            Nodes = Arbol.GetNodes()
            Graph = nx.Graph()
            Nodes, Edges, Labels, i = self.GraphNodes(Graph, Nodes)
            Labels = {a: b for a, b in zip(Nodes, Labels)}
            Graph.add_nodes_from(Nodes)
            Graph.add_edges_from(Edges)
            Pos = nx.nx_pydot.graphviz_layout(Graph, prog="dot")
            plt.figure(0, figsize=(225, 75), dpi=10)
            nx.draw(Graph, Pos,with_labels=False, node_size=25000, width=20, node_color="#CFCFCF",
                    edge_color="lightblue", arrows=True, arrowstyle="-|>", arrowsize=150)
            nx.draw_networkx_labels(Graph, Pos, Labels, 100, font_weight="bold")
            plt.savefig("Graph.png")
            self.LblArbol.setPixmap(QPixmap("Graph.png"))
            self.TblRes.setRowCount(len(Res))
            for x, a in enumerate(Res):
                for y, b in enumerate(a):
                    item = QTableWidgetItem()
                    item.setText(b)
                    item.setToolTip(b)
                    item.setFont(QFont("Verdana", 14))
                    item.setTextAlignment(Qt.AlignCenter)
                    item.setFlags(~Qt.ItemFlag.ItemIsEnabled)
                    self.TblRes.setItem(x, y, item)
    @Slot()
    def Changed(self, Index):
        self.TblRes.close()
        self.LblArbol.close()
        if Index == 0:
            self.TblRes.show()
        elif Index == 1:
            self.LblArbol.show()
        elif Index == 2:
            pass
        elif Index == 3:
            pass

    def GraphNodes(self, Graph:nx.Graph, Nodes, Index=0, Last=0):
        _Nodes = []
        _Labels = []
        _Edges = []
        if Nodes:
            _Last = Index
        else:
            return _Nodes, _Edges, _Labels, Index
        for Node in Nodes:
            if isinstance(Node, list):
                n, e, l, Index = self.GraphNodes(Graph, Node, Index, _Last)
                _Nodes += n
                _Edges += e
                _Labels += l
            else:
                _Nodes.append(Index)
                _Labels.append(Node)
                if Index == _Last and Index != 0:
                    _Edges.append((Last, Index))
                elif Index != 0:
                    _Edges.append((_Last, Index))
                Index += 1
        return _Nodes, _Edges, _Labels, Index

    def UiComponents(self):
        BtnFont = QFont("Verdana", 15)
        self.CbbxInput = QComboBox(self)
        self.CbbxInput.setGeometry(self.Screen.width() / 16, self.Screen.height() / 8,
                                   self.Screen.width() / 4, 50)
        self.CbbxInput.setFont(BtnFont)
        for File in listdir():
            if File[File.find("."):] == ".txt":
                self.CbbxInput.addItem(File)
        self.CbbxInput.setCurrentIndex(0)

        self.BtnAnalize = QPushButton("Analize", self)
        self.BtnAnalize.setGeometry(self.Screen.width() / 16 * 5, self.Screen.height() / 8,
                                    150, 50)
        self.BtnAnalize.setFont(BtnFont)
        self.BtnAnalize.pressed.connect(self.Pressed)

        self.TblRes = QTableWidget(self)
        self.TblRes.setGeometry(self.Screen.width() / 16, self.Screen.height() / 4,
                                self.Screen.width() / 16 * 14, self.Screen.height() / 8 * 5)
        self.TblRes.setColumnCount(3)
        for a in range(3):
            self.TblRes.setColumnWidth(a, (self.TblRes.width() - 20) / 3)
        self.TblRes.setHorizontalHeaderLabels(["Pila", "Entrada", "Salida"])
        self.TblRes.horizontalScrollBar().close()

        self.TblRes.verticalHeader().close()

        self.LblArbol = QLabel(self)
        self.LblArbol.setGeometry(self.Screen.width() / 16, self.Screen.height() / 4,
                                  self.Screen.width() / 16 * 14, self.Screen.height() / 8 * 5)
        self.LblArbol.setScaledContents(True)
        self.LblArbol.close()
        print(self.LblArbol.size())


        self.TBar = QTabBar(self)
        self.TBar.setGeometry(self.Screen.width() / 16, self.Screen.height() / 4 - 20,
                              self.Screen.width() / 16 * 14, 25)
        self.TBar.addTab("Pila Y Entrada")
        self.TBar.addTab("Arbol")
        self.TBar.addTab("WIP")
        self.TBar.addTab("WIP")
        self.TBar.currentChanged.connect(self.Changed)

if __name__ == "__main__":
    AnSin = AnlaizadorSintactico()
    AnLex = AnalizadorLexico()

    App = QApplication(sys.argv)
    main_Window = MainWindow()
    App.exec()
