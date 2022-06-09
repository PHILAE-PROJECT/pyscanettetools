import unittest
from src.Scanner import Scanner,ScannerState
from src.Cashier import Cashier
import sys
import csv
import json
path='C:/Users/QZTD9928/Documents/code/pyscannetteAgilkia/'

# SCANNER_PRODUCTS = "../csv/produitsScanette.csv"
# CASHIER_PRODUCTS = '../csv/produitsCaisse.csv'
# TRACES_PATH_CSV="../csv/out.csv"
# TRACES_PATH_JSON="../csv/100043-steps.json"

SCANNER_PRODUCTS = path+"/csv/produitsScanette.csv"
CASHIER_PRODUCTS = path+'/csv/produitsCaisse.csv'
TRACES_PATH_CSV=path+"/csv/out.csv"
TRACES_PATH_JSON=path+"/csv/100043-steps.json"


class OneTraceExecutor(unittest.TestCase):

    def setUp(self):
        self.scanners = dict()
        self.cashiers = dict()
        self.sessions=dict()
        self.SEQ=None

    def process(self, line, obj, op, params, res):
        if op == 'debloquer':
            self._execUnlock(obj,res)
            return
        if op=='scanner':
            self._execScan(obj,params,res)
            return
        if op=='transmission':
            self._execTransmission(obj,params,res)
            return
        if op=='ouvrirSession':
            self._execOpenSession(obj,res)
            return
        if op=='fermerSession':
            self._execCloseSession(obj,res)
            return
        if op=='ajouter':
            self._execAdd(obj,params,res)
            return
        if op=='payer':
            self._execPay(obj,params,res)
            return
        if op=='abandon':
            self._execAbandon(obj)
            return
        if op=='supprimer':
            self._execDelete(obj,params,res)
            return
        print("Unknown operation:"+str(op)+" (line "+line+")")
        sys.exit(-1)

    def _execUnlock(self, sc, res):
        sc = sc.strip()
        if (sc not in self.scanners):
            self.scanners[sc] = Scanner(bycsv=True, path=SCANNER_PRODUCTS)

        r = self.scanners[sc].unlock()
        self.assertEqual(int(res),r)

    def _execScan(self,sc,params,res):
        sc=sc.strip()
        if (sc not in self.scanners):
            self.scanners[sc] = Scanner(bycsv=True, path=SCANNER_PRODUCTS)

        r=self.scanners[sc].scan(int(params[0]))
        self.assertEqual(int(res),r)

    def _execTransmission(self,sc,params,res):
        sc = sc.strip()
        if (sc not in self.scanners):
            self.scanners[sc] = Scanner(bycsv=True, path=SCANNER_PRODUCTS)
        params[0]=params[0].strip()
        if (params[0] not in self.cashiers):
            self.cashiers[params[0]] = Cashier(bycsv=True, path=CASHIER_PRODUCTS)
        resI=int(res)
        self.cashiers[params[0]].threshold=1 if (resI==1) else 0
        r=self.scanners[sc].transmission(self.cashiers[params[0]])
        self.assertEqual(resI,r)

    def _execOpenSession(self,c,res):
        c=c.strip()
        if c not in self.cashiers:
            self.cashiers[c] = Cashier(bycsv=True, path=CASHIER_PRODUCTS)
        r=self.cashiers[c].openSession()
        self.assertEqual(int(res),r)

    def _execCloseSession(self,c,res):
        c=c.strip()
        if c not in self.cashiers:
            self.cashiers[c] = Cashier(bycsv=True, path=CASHIER_PRODUCTS)
        r=self.cashiers[c].closeSession()
        self.assertEqual(int(res),r)

    def _execAdd(self,c,params,res):
        c=c.strip()
        if c not in self.cashiers:
            self.cashiers[c] = Cashier(bycsv=True, path=CASHIER_PRODUCTS)
        r=self.cashiers[c].scan(int(params[0]))
        self.assertEqual(int(res),r)

    def _execPay(self,c,params,res):
        c=c.strip()
        if c not in self.cashiers:
            self.cashiers[c] = Cashier(bycsv=True, path=CASHIER_PRODUCTS)
        r=self.cashiers[c].pay(float(params[0]))
        self.assertAlmostEqual(first=float(res),second=r,delta=0.01)

    def _execAbandon(self,c):
        c=c.strip()
        if c not in self.scanners and c[0]=='s':
            self.scanners[c] = Scanner(bycsv=True, path=SCANNER_PRODUCTS)
        if c in self.scanners:
            self.scanners[c].abandon()
            return
        if c not in self.cashiers and c[0]=='c':
            self.cashiers[c] = Cashier(bycsv=True, path=CASHIER_PRODUCTS)
        if c in self.cashiers:
            self.cashiers[c].abandon()
            return
        raise AssertionError(" c input hasn't the right value ")


    def _execDelete(self,c,params,res):
        c=c.strip()
        if c in  self.scanners:
            r=self.scanners[c].delete(int(params[0]))
            self.assertEqual(int(res),r)
            return
        if c in self.cashiers:
            r=self.cashiers[c].delete(int(params[0]))
            self.assertEqual(int(res),r)
            return
        raise AssertionError(" c input hasn't the right value ")


    def test_one_trace_as_test(self):

        for i_row,row in enumerate(self.SEQ):
            # i_row=0
            if len(row)!= 7:
                raise AssertionError('Error in csv file format ('+str(i_row)+')\nExpected: #LineID, #Timestamp, #SessionID, #Object, #Operation, #ArrayOfParameters, #ExpectedResult")')

            if row[2] not in self.sessions:
                # print('.')
                self.sessions[row[2]]=None
            obj=row[3].strip()
            op=row[4].strip()
            row[5]=row[5].strip()
            params=[row[5][1:-1]]
            res=row[6].strip()
            try:
                self.process(i_row,obj,op,params,res)
            except:
                print(str(row)+" (line "+str(i_row)+")")
                sys.exit(-1)




if __name__ == '__main__':
    # with open('../csv/100043-steps.json') as json_file:
    #     data = dict(json.load(json_file))
    unittest.main()
    # for k, v in data.items():
    #     print(v)
    #     o = OneTraceAsTestsAdaptor()
    #     o.setUp()
    #     o.SEQ = v
    #     o.test_one_trace_as_test()
    #     break

