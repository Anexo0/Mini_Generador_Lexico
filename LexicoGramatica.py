import csv
import re


class AnalizadorLexico:
    def __init__(self):
        self.Text = str
        self.Header = int
        self.Tokens = list
        self.RePatts = None
        self.RsWords = None
        self.TLen = None
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
                L = [Line[0], Line[1][1:-1].replace("'", "").split(",")]
                Rw.append(L)
        self.RePatts = Re
        self.RsWords = Rw

    def Analize(self, text):
        self.Text = text
        self.Header = 0
        self.Tokens = []
        self.TLen = len(self.Text)
        while self.Header < self.TLen:
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
            Simbol = Simbol.replace(" ", "")
        return [Simbol, Token]
