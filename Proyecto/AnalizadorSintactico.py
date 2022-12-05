from csv import reader


class NoTerminal:
    def __init__(self, element, sons, state, token):
        self.Element = element
        self.Sons = sons
        self.State = state
        self.Token = token
        self.Simbols = None
        self.Scope = None

    def __str__(self):
        string = f"{self.Element}({self.Token})\n"
        for a in self.Sons:
            string += f"{str(a)}\t"
        return string

    def GetNodes(self):
        Nodes = [str(self.Element)]
        Sons = []
        for Elem in self.Sons:
            if isinstance(Elem, NoTerminal):
                n = Elem.GetNodes()
                Sons += [n]
            else:
                Sons += [str(Elem.Element)]
        if not self.Sons:
            Nodes += [self.Sons]
        if Sons:
            Nodes += Sons
        return Nodes


class Terminal:
    def __init__(self, element, state, token):
        self.Element = element
        self.State = state
        self.Token = token
        self.Simbols = None
        self.Scope = None

    def __str__(self):
        return f"{self.Element} ({self.Token})"


class AnalizadorSintactico:

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
        PText = "".join([f"{a.Element}{a.State}" for a in self.Pila])
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
                        PText = "".join([f"{a.Element}{a.State[1:]}" for a in self.Pila])
                        Res.append([PText, "".join(reversed(self.Entrada)), f"d{Step}"])
                    elif 'r' in Step:
                        Rule = self.Rules[int(Step[1:])]
                        if Step == "r0":
                            PText = "".join([f"{a.Element}{a.State[1:]}" for a in self.Pila])
                            Res.append([PText, ''.join(reversed(self.Entrada)), "r0 accepted"])
                            Res.append(self.Pila.pop())
                            break
                        if Rule[0] == [a.Token for a in self.Pila[-Rule[1]:]] or not Rule[1]:
                            Elements = []
                            for a in range(Rule[1]):
                                Elements.insert(0, self.Pila.pop())
                            Header = int(self.Pila[-1].State[1:])
                            Step2 = self.Gram[Header + 1][self.Gram[0].index(Rule[2])]
                            if Step2:
                                self.Pila.append(NoTerminal(Rule[2], Elements, f"s{Step2}", Rule[2]))
                                Tokens.insert(self.Header, [Rule[2], Rule[2]])
                            PText = "".join([f"{a.Element}{a.State[1:]}" for a in self.Pila])
                            Res.append([PText, "".join(reversed(self.Entrada)), Step])
                        else:
                            Pila = list(map(self.ToString, self.Pila))
                            Res.append([''.join(Pila), ''.join(reversed(self.Entrada)), "Error"])
                            Res.append("Error")
                            break
                    else:
                        Header = int(Step)
                        self.Header += 1
                        PText = "".join([f"{a.Element}{a.State[1:]}" for a in self.Pila])
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

    def ToString(self, Item: Terminal):
        return f"{Item.Element}{Item.State[1:]}"

    def ToGram(self, Token):
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
