from enum import Enum
from .ItemsDB import ItemsDB
from .ItemsDB import ArticleNotFoundException
from random import uniform

class CashierState(Enum):
    PENDING = 0
    WAITINGFORTHECASHIER = 1
    PAYMENT = 2
    AUTHENTIFIED = 3

class Cashier:

    def __init__(self,bycsv=False,path=None):

        self.items=ItemsDB(bycsv=bycsv,path=path)
        self.basket={}
        self.state=CashierState.PENDING
        self.toPay=0
        self.threshold=0.1

    def connection(self,s):
        if (s is None):
            return -1
        if (self.state is not(CashierState.PENDING)):
            return -1


        if (not(s.proofreadingDone()) and len(s.getItems())>0 and self.proofreadingRequest()):
            return 1

        self.basket.clear()

        for item in s.getItems():
            self.basket[item]=s.quantity(item.codeEAN13)


        if(len(s.getUnknownReferences())>0 or len(s.getItems()) ==0):
            self.state=CashierState.WAITINGFORTHECASHIER
        else:
            self.state=CashierState.PAYMENT

        return 0

    def proofreadingRequest(self):
        return uniform(0,1)<self.threshold
        # return True

    def pay(self,amount):
        if (self.state != CashierState.PAYMENT):
            return -42

        self.toPay=0
        for key in self.basket.keys():
            self.toPay+=key.unitaryPrice*self.basket[key]

        if (self.toPay-amount<0.01):
            self.basket.clear()
            self.state=CashierState.PENDING

        return amount-self.toPay

    def abandon(self):
        self.basket.clear()
        self.state=CashierState.PENDING

    def openSession(self):
        if (self.state==CashierState.PAYMENT or self.state == CashierState.WAITINGFORTHECASHIER):
            self.state=CashierState.AUTHENTIFIED
            return 0
        return -1

    def closeSession(self):
        if (self.state==CashierState.AUTHENTIFIED):
            self.state = CashierState.PENDING if not(self.basket) else CashierState.PAYMENT
            return 0
        return -1

    def scan(self,ean13):
        if(self.state!=CashierState.AUTHENTIFIED):
            return -1

        try:
            item=self.items.getArticle(ean13)
            if (item in self.basket.keys()):
                self.basket[item]+=1
            else:
                self.basket[item]=1
        except ArticleNotFoundException:
            return -2

        return 0

    def delete(self,ean13):
        if(self.state != CashierState.AUTHENTIFIED):
            return -1

        for item in self.basket:
            if(item.codeEAN13==ean13):
                nb=self.basket[item]
                if(nb>1):
                    self.basket[item]=nb-1
                else:
                    self.basket.pop(item)

                return 0
        return -2

    def returnFalse(self):
        return False

    def returnReturnFalse(self):
        return self.returnFalse()




