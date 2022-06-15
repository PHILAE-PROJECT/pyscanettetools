class Item:

    def __init__(self,_ean13, _pu, _name):
        self.codeEAN13=_ean13
        self.unitaryPrice=_pu
        if _name is None:
            self.name=""
        else:
            self.name=_name

    def __eq__(self, i):
        if not(hasattr(i,'codeEAN13')):
            return False
        return i is not None and isinstance(i,Item) and i.codeEAN13 == self.codeEAN13

    def __hash__(self):
        return int(self.codeEAN13).__hash__()

    def isValidEAN13(self):
        if (self.codeEAN13<0):
            return False
        tab=str(self.codeEAN13)
        if(len(tab)>13):
            return False

        while(len(tab)<13):
            tab='0'+tab

        sum=0

        for i in range(0,12):
            digit=int(tab[i])
            sum+= digit*3 if (i%2==1) else digit

        reste=sum%10
        key=0 if (reste==0) else 10-reste

        return key==int(tab[12])










