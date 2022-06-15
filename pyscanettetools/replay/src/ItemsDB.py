
ITEMSDB={5410188006711: {"ean": 5410188006711, "price": 2.15, "name": "Tropicana Tonic Breakfast", "idShelf": 13},
3560070048786: {"ean": 3560070048786, "price": 0.87, "name": "Cookies choco", "idShelf": 3},
3017800238592: {"ean": 3017800238592, "price": 2.20,
                "name": "Daucy Curry vert de légumes riz graines de courge et tournesol", "idShelf": 2},
3560070976478: {"ean": 3560070976478, "price": 1.94, "name": "Poulet satay et son riz", "idShelf": 2},
3046920010856: {"ean": 3046920010856, "price": 2.01, "name": "Lindt Excellence Citron à la pointe de Gingembre", "idShelf": 12},
8715700110622: {"ean": 8715700110622, "price": 0.96, "name": "Ketchup", "idShelf": 10},
3520115810259: {"ean": 3520115810259, "price": 8.49, "name": "Mont d'or moyen Napiot", "idShelf": 6},
3270190022534: {"ean": 3270190022534, "price": 0.58, "name": "Pâte feuilletée", "idShelf": 11},
8718309259938: {"ean": 8718309259938, "price": 4.65, "name": "Soda stream saveur agrumes", "idShelf": 14},
3560071097424: {"ean": 3560071097424, "price": 2.40, "name": "Tartelettes carrées fraise", "idShelf": 3},
3017620402678: {"ean": 3017620402678, "price": 1.86, "name": "Nutella 220g", "idShelf": 1},
3245412567216: {"ean": 3245412567216, "price": 1.47, "name": "Pain de mie", "idShelf": 1},
45496420598: {"ean": 45496420598, "price": 54.99, "name": "Jeu switch Minecraft", "idShelf": 7},
3560070139675: {"ean": 3560070139675, "price": 1.94, "name": "Boîte de 110 mouchoirs en papier", "idShelf": 5},
3020120029030: {"ean": 3020120029030, "price": 1.70, "name": "Cahier Oxford 90 pages petits carreaux", "idShelf": 0},
3474377910724: {"ean": 3474377910724, "price": 8.60, "name": "Sortez couverts !", "idShelf": 5} }
import csv
from math import floor
from .Item import Item

class ItemsDB:

    def __init__(self,bycsv=False,path=None):
        self.items = {}
        if not(bycsv) and path is None:
           self.readDict()
        elif bycsv and path is not None:
            self.readFile(path)
        else:
            raise Exception("Arg not correct")


    def readDict(self):

        for key in ITEMSDB.keys():
            i = Item(_ean13=key, _pu=ITEMSDB[key]["price"], _name=ITEMSDB[key]["name"])
            self.items[key] = i

    def readFile(self,path):
        if path is None or path[-4:]!='.csv':
            raise IOError("path is not correct")
        temp={}

        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if(len(row)!=3 and len(row)!=4):
                    raise FileFormatException(path)
                try:
                    ean13=int(row[0])
                    pu=float(row[1])
                    name=row[2].strip()
                    reduc=0
                    if(len(row)==4):
                        row[3]=row[3].strip()
                        if(row[3][-1] !='%'):
                            raise FileFormatException(path)
                        row[3]=row[3][:-1]
                        reduc=int(row[3])
                        pu=floor((pu-(pu*reduc/100.0))*100)/100

                    if pu>=0:
                        i=Item(ean13,pu,name)
                        if(not(i.isValidEAN13())):
                            raise FileFormatException(path)
                        temp[ean13]=i
                    else:
                        raise FileFormatException(path)
                except ValueError:
                    raise FileFormatException(path)
            self.items=temp



    def addItemsRecognizableByTheCashier(self):

        self.items[7640164630021] = {"ean": 7640164630021, "price": 229.90, "name": "Robot éducatif Thymio", "idShelf": 7};
        self.items[3570590109324] = {"ean": 3570590109324, "price": 7.48, "name": "Vin blanc Arbois Vieilles Vignes",
                                   "idShelf": 6};

    def getArticle(self,_ean13):
        if _ean13 not in self.items.keys():
            raise ArticleNotFoundException(_ean13)
        return self.items[_ean13]

    def getSizeDB(self):
        return len(self.items.keys())




class ArticleNotFoundException(Exception):

    def __init__(self,_ean13):
        super(ArticleNotFoundException,self).__init__("Item "+str(_ean13)+" cannot be found in the database")

class FileFormatException(Exception):
    def __init(self,filename):
        super().__init__("the file "+filename+" has not a correct format")

if __name__=="__main__":
    # db=ItemsDB(bycsv=True,path="./csv/validFile.csv")
    db=ItemsDB()
    db.initdb()
    print(db.items)

