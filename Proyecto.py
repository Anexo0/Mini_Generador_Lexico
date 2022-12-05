import LexicoGramatica as Alx
import AnalizadorSemantico as Asm
import AnalizadorSintactico as Asn

import sys
import networkx as nx
from os import listdir
from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *
import matplotlib.pyplot as plt


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

    @Slot()
    def Pressed(self):
        with open(self.CbbxInput.itemText(self.CbbxInput.currentIndex())) as File:
            plt.close()
            Text = File.read().replace("\n", "")
            Tokens = AnLex.Analize(Text)
            Res = AnSin.Analize(Tokens)
            Arbol = Res.pop()
            Nodes = Arbol.GetNodes()
            Simbols = AnSim.Analize(Arbol, Asn.NoTerminal)
            Graph = nx.Graph()
            Nodes, Edges, Labels, i = self.GraphNodes(Graph, Nodes)
            Labels = {a: b for a, b in zip(Nodes, Labels)}
            Graph.add_nodes_from(Nodes)
            Graph.add_edges_from(Edges)
            Pos = nx.nx_pydot.graphviz_layout(Graph, prog="dot")
            plt.figure(0, figsize=(225, 75), dpi=10)
            nx.draw(Graph, Pos, with_labels=False, node_size=25000, width=20, node_color="#CFCFCF",
                    edge_color="lightblue", arrows=True, arrowstyle="-|>", arrowsize=150)
            nx.draw_networkx_labels(Graph, Pos, Labels, 100, font_weight="bold")
            plt.savefig("Graph.png")
            self.LblArbol.setPixmap(QPixmap("Graph.png"))
            self.TblRes.setRowCount(len(Res))
            for x, a in enumerate(Res):
                for y, b in enumerate(a):
                    Item = QTableWidgetItem()
                    Item.setText(b)
                    Item.setToolTip(b)
                    Item.setFont(QFont("Verdana", 14))
                    Item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    Item.setFlags(~Qt.ItemFlag.ItemIsEnabled)
                    self.TblRes.setItem(x, y, Item)
            self.TblVar.setRowCount(len(Simbols))
            for x, a in enumerate(Simbols):
                for y, b in enumerate(a):
                    Item = QTableWidgetItem()
                    Item.setText(b if b else "")
                    Item.setToolTip(b if b else "")
                    Item.setFont(QFont("Verdana", 14))
                    Item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    Item.setFlags(~Qt.ItemFlag.ItemIsEnabled)
                    self.TblVar.setItem(x, y, Item)

    @Slot()
    def TabChanged(self, Index):
        self.TblRes.close()
        self.LblArbol.close()
        self.TblVar.close()
        self.TxFile.close()
        if Index == 0:
            self.TblRes.show()
        elif Index == 1:
            self.LblArbol.show()
        elif Index == 2:
            self.TblVar.show()
        elif Index == 3:
            self.TxFile.show()

    @Slot()
    def IndexChanged(self, Index):
        Path = self.CbbxInput.itemText(Index)
        with open(Path, "r") as File:
            self.TxFile.setText(f"{Path}\n\n{File.read()}")

    def GraphNodes(self, Graph: nx.Graph, Nodes, Index=0, Last=0):
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
        self.CbbxInput.currentIndexChanged.connect(self.IndexChanged)

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

        self.TblVar = QTableWidget(self)
        self.TblVar.setGeometry(self.Screen.width() / 16, self.Screen.height() / 4,
                                self.Screen.width() / 16 * 14, self.Screen.height() / 8 * 5)
        self.TblVar.setColumnCount(4)
        for a in range(4):
            self.TblVar.setColumnWidth(a, (self.TblVar.width() - 20) / 4)
        self.TblVar.setHorizontalHeaderLabels(["Objeto", "Tipo", "Identificador", "Scope"])
        self.TblVar.horizontalScrollBar().close()
        self.TblVar.verticalHeader().close()
        self.TblVar.close()

        self.TBar = QTabBar(self)
        self.TBar.setGeometry(self.Screen.width() / 16, self.Screen.height() / 4 - 20,
                              self.Screen.width() / 16 * 14, 25)
        self.TBar.addTab("Pila Y Entrada")
        self.TBar.addTab("Arbol Sintactico")
        self.TBar.addTab("Scope")
        self.TBar.addTab("Current File")
        self.TBar.currentChanged.connect(self.TabChanged)

        self.TxFile = QTextEdit(self)
        self.TxFile.setGeometry(self.Screen.width() / 16, self.Screen.height() / 4 + 3,
                                self.Screen.width() / 16 * 14, self.Screen.height() / 8 * 5)
        self.IndexChanged(0)
        self.TxFile.close()


if __name__ == "__main__":
    AnSin = Asn.AnalizadorSintactico()
    AnLex = Alx.AnalizadorLexico()
    AnSim = Asm.AnalizadorSemantico()
    App = QApplication(sys.argv)
    main_Window = MainWindow()
    App.exec()
