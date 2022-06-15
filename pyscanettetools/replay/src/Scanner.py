from enum import Enum
from .ItemsDB import ItemsDB
from .ItemsDB import ArticleNotFoundException
from .ItemsDB import FileFormatException
class ScannerState(Enum):
    LOCKED=0
    DOINGSHOPPING=1
    PROOFREADING=2
    PROOFREADINGOK=3
    PROOFREADINGKO=4


TOBERESCANNEDMAX=12

class Scanner:

    def __init__(self,bycsv=False,path=None):
        try:
            self.state=ScannerState.LOCKED
            self.itemsDB=ItemsDB(bycsv=bycsv,path=path)
            self.basket={}
            self.unknownReferences=[]
            self.verified={}
            self.toBeRescanned=0
        except FileFormatException:
            raise ProductDBFailureException()
        except IOError:
            raise ProductDBFailureException()


    def unlock(self):
        if (self.state==ScannerState.LOCKED):
            self.state=ScannerState.DOINGSHOPPING
            return 0
        return -1

    def scan(self,ean13):
        if (self.state==ScannerState.DOINGSHOPPING):
            try:
                item=self.itemsDB.getArticle(ean13)
                quantity=self.quantity(ean13)
                quantity+=1
                self.basket[ean13]=quantity
                return 0
            except ArticleNotFoundException:
                self.unknownReferences.append(ean13)
                return -2

        if (self.state==ScannerState.PROOFREADING):
            quantity=self.verified[ean13] if ean13 in self.verified.keys() else 0
            self.verified[ean13]=quantity+1

            if(not(ean13 in self.basket.keys()) or self.verified[ean13]>self.basket[ean13]):
                self.state=ScannerState.PROOFREADINGKO
                return -3
            else:
                self.toBeRescanned-=1
                if(self.toBeRescanned==0):
                    self.state=ScannerState.PROOFREADINGOK

                return 0

        return -1


    def delete(self,ean13):
        if(self.state!=ScannerState.DOINGSHOPPING):
            return -1

        quantity=self.quantity(ean13)
        if(quantity<1):
            return -2

        if(quantity==1):
            self.basket.pop(ean13)
            return 0
        self.basket[ean13]=quantity-1
        return 0

    def quantity(self,ean13):
        return self.basket[ean13] if ean13 in self.basket.keys() else 0

    def abandon(self):
        self.state=ScannerState.LOCKED
        self.basket.clear()
        self.unknownReferences.clear()

    def getItems(self):
        itemset=[]
        try:
            for key in self.basket.keys():
                itemset.append(self.itemsDB.getArticle(key))
        except ArticleNotFoundException:
            pass
        itemset=set(itemset)
        return itemset

    def transmission(self,cashier):

        if (cashier is None):
            return -1
        if(self.state != ScannerState.PROOFREADINGOK and self.state != ScannerState.DOINGSHOPPING):
            return -1

        cashierReturnCode=cashier.connection(self)

        if(cashierReturnCode==0):
            self.state=ScannerState.LOCKED

            self.basket.clear()

            self.unknownReferences.clear()
            return 0
        elif (self.state ==ScannerState.DOINGSHOPPING and cashierReturnCode==1):
            self.state=ScannerState.PROOFREADING

            self.verified.clear()

            nb=self.getNbItems()

            self.toBeRescanned=TOBERESCANNEDMAX if nb> TOBERESCANNEDMAX else nb
            if (self.toBeRescanned==0):
                self.state=ScannerState.PROOFREADINGOK
            return 1

        return -1

    def proofreadingDone(self):
        return self.state==ScannerState.PROOFREADINGOK

    def getNbItems(self):
        nb=0
        for key in self.basket.keys():
            nb+=self.basket[key]
        return nb
    def getUnknownReferences(self):
        return set(self.unknownReferences)


class ProductDBFailureException(Exception):
    pass



