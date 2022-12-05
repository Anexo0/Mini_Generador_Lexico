class AnalizadorSemantico:
    def __init__(self):
        self.Simbols = None
        self.Nodes = None

    def Analize(self, Node, cls, Simbols=None, Scope=None):
        if Simbols is None:
            Simbols = []
        for Elem in Node.Sons:
            if Elem.Token == "DefFunc":
                Scope = Elem.Sons[1].Element
                Simbols.append([f"Funcion", f"{Elem.Sons[0].Element}", Elem.Sons[1].Element, None])
            elif Elem.Token == "DefVar":
                if Scope:
                    Simbols.append([f"Variable", f"{Elem.Sons[0].Element}", Elem.Sons[1].Element, Scope])
                else:
                    Simbols.append([f"Variable", f"{Elem.Sons[0].Element}", Elem.Sons[1].Element, "Global"])
            elif Elem.Token == "Parametros":
                if Elem.Sons:
                    Simbols.append([f"Parameter", f"{Elem.Sons[0].Element}", Elem.Sons[1].Element, Scope])
            elif Elem.Token == "ListaParam":
                if Elem.Sons:
                    Simbols.append([f"Parameter", f"{Elem.Sons[1].Element}", Elem.Sons[2].Element, Scope])
            if isinstance(Elem, cls):
                s = self.Analize(Elem, cls, Simbols, Scope)
        return Simbols
