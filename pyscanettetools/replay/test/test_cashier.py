import unittest
from ..src.Cashier import Cashier
from ..src.Scanner import Scanner,ProductDBFailureException
from ..src.Item import Item
from mockito import spy,when,unstub
import mockito
class TestCashier(unittest.TestCase):

    def setUp(self):
        self.folderPath="C:/Users/QZTD9928/Documents/code/pyscannetteAgilkia/csv/"
        self.cashier=spy(Cashier(bycsv=True,path=self.folderPath+"produitsOK.csv"))
        self.scan=mockito.mock(spec=Scanner,strict=True)

    def initBasket(self):
        basket=[]
        basket.append(Item(5410188006711, 2.15, "Tropicana Tonic Breakfast"))
        basket.append(Item(8715700110622, 0.96, "Ketchup"))
        basket.append(Item(45496420598, 54.99, "Jeu switch Minecraft"))
        self.basket=set(basket)
        when(self.scan).getItems().thenReturn(self.basket)
        when(self.scan).quantity(5410188006711).thenReturn(3)
        when(self.scan).quantity(8715700110622).thenReturn(2)
        when(self.scan).quantity(45496420598).thenReturn(1)
        self.totalBasket=3*2.15+0.96*2+54.99

    def tearDown(self):
        unstub()
    def initUnknownRef(self):
        unknownref=[5410188006712]
        unknownref=set(unknownref)
        when(self.scan).getUnknownReferences().thenReturn(unknownref)


    def testFileDoesNotExist(self):
        self.assertRaises(ProductDBFailureException,Scanner,True,self.folderPath+"fichierInexistant.csv")

    def testFileWithErrors(self):
        self.assertRaises(ProductDBFailureException,Scanner,True,self.folderPath+"produitsKO.csv")

    def testProofreadingRequestFrequence(self):
        nbTrue=0
        nbFalse=0
        for i in range(100000):
            if(self.cashier.proofreadingRequest()):
                nbTrue+=1
            else:
                nbFalse+=1

        self.assertTrue(nbTrue>9500 and nbTrue<10500)

    def testConnection0_notProofread(self):
        when(self.scan).getItems().thenReturn(set([]))
        when(self.scan).getUnknownReferences().thenReturn(set([]))
        when(Cashier).proofreadingRequest().thenReturn(False)

        when(self.scan).proofreadingDone().thenReturn(False)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0)<0)
        self.assertEqual(-1,self.cashier.connection(self.scan))

    def testConnection0_Proofread(self):
        when(self.scan).getItems().thenReturn(set([]))
        when(self.scan).getUnknownReferences().thenReturn(set([]))
        when(Cashier).proofreadingRequest().thenReturn(False)

        when(self.scan).proofreadingDone().thenReturn(True)
        self.assertEqual(0, self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0) < 0)
        self.assertEqual(-1, self.cashier.connection(self.scan))

    def testConnection1_notProofread(self):
        when(self.scan).getItems().thenReturn(set([]))
        when(self.scan).getUnknownReferences().thenReturn(set([]))
        when(Cashier).proofreadingRequest().thenReturn(True)

        when(self.scan).proofreadingDone().thenReturn(False)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0)<0)
        self.assertEqual(-1,self.cashier.connection(self.scan))

    def testConnection1_Proofread(self):
        when(self.scan).getItems().thenReturn(set([]))
        when(self.scan).getUnknownReferences().thenReturn(set([]))
        when(Cashier).proofreadingRequest().thenReturn(True)

        when(self.scan).proofreadingDone().thenReturn(True)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0)<0)
        self.assertEqual(-1,self.cashier.connection(self.scan))

    def testConnection2_notProofread(self):
        when(self.scan).getItems().thenReturn(set([]))
        self.initUnknownRef()
        when(Cashier).proofreadingRequest().thenReturn(False)

        when(self.scan).proofreadingDone().thenReturn(False)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0)<0)
        self.assertEqual(-1,self.cashier.connection(self.scan))

    def testConnection2_Proofread(self):
        when(self.scan).getItems().thenReturn(set([]))
        self.initUnknownRef()
        when(Cashier).proofreadingRequest().thenReturn(False)
        when(self.scan).proofreadingDone().thenReturn(True)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0)<0)
        self.assertEqual(-1,self.cashier.connection(self.scan))


    def testConnection3_notProofread(self):
        when(self.scan).getItems().thenReturn(set([]))
        self.initUnknownRef()
        when(Cashier).proofreadingRequest().thenReturn(True)

        when(self.scan).proofreadingDone().thenReturn(False)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0)<0)
        self.assertEqual(-1,self.cashier.connection(self.scan))


    def testConnection3_Proofread(self):
        when(self.scan).getItems().thenReturn(set([]))
        self.initUnknownRef()
        when(Cashier).proofreadingRequest().thenReturn(True)

        when(self.scan).proofreadingDone().thenReturn(True)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0)<0)
        self.assertEqual(-1,self.cashier.connection(self.scan))

    def testConnection4_notProofread(self):
        self.initBasket()
        when(self.scan).getUnknownReferences().thenReturn(set([]))
        when(Cashier).proofreadingRequest().thenReturn(False)

        when(self.scan).proofreadingDone().thenReturn(False)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertEqual(-1,self.cashier.connection(self.scan))
        self.assertAlmostEqual(first=0, second=self.cashier.pay(self.totalBasket),delta=0.001)

    def testConnection4_Proofread(self):
        self.initBasket()
        when(self.scan).getUnknownReferences().thenReturn(set([]))
        when(Cashier).proofreadingRequest().thenReturn(False)

        when(self.scan).proofreadingDone().thenReturn(True)
        self.assertEqual(0, self.cashier.connection(self.scan))
        self.assertEqual(-1, self.cashier.connection(self.scan))
        self.assertAlmostEqual(first=0, second=self.cashier.pay(self.totalBasket), delta=0.001)

    def testConnection5_notProofread(self):
        self.initBasket()
        when(self.scan).getUnknownReferences().thenReturn(set([]))
        when(Cashier).proofreadingRequest().thenReturn(True)
        when(self.scan).proofreadingDone().thenReturn(False)

        self.assertEqual(1,self.cashier.connection(self.scan))
        self.assertEqual(1,self.cashier.connection(self.scan))

    def testConnection5_Proofread(self):
        self.initBasket()
        when(self.scan).getUnknownReferences().thenReturn(set([]))
        when(Cashier).proofreadingRequest().thenReturn(True)

        when(self.scan).proofreadingDone().thenReturn(True)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertEqual(-1,self.cashier.connection(self.scan))
        self.assertAlmostEqual(first=0, second=self.cashier.pay(self.totalBasket), delta=0.001)


    def testConnection6_notProofread(self):
        self.initBasket()
        self.initUnknownRef()
        when(Cashier).proofreadingRequest().thenReturn(False)

        when(self.scan).proofreadingDone().thenReturn(False)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertEqual(-1,self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0)<0)

    def testConnection6_Proofread(self):
        self.initBasket()
        self.initUnknownRef()
        when(Cashier).proofreadingRequest().thenReturn(False)

        when(self.scan).proofreadingDone().thenReturn(True)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertEqual(-1,self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0)<0)

    def testConnection7_notProofread(self):
        self.initBasket()
        self.initUnknownRef()
        when(Cashier).proofreadingRequest().thenReturn(True)
        when(self.scan).proofreadingDone().thenReturn(False)
        self.assertEqual(1,self.cashier.connection(self.scan))
        self.assertEqual(1,self.cashier.connection(self.scan))

    def testConnection7_Proofread(self):
        self.initBasket()
        self.initUnknownRef()
        when(Cashier).proofreadingRequest().thenReturn(True)

        when(self.scan).proofreadingDone().thenReturn(True)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertEqual(-1,self.cashier.connection(self.scan))
        self.assertTrue(self.cashier.pay(0)<0)

    def testPaythenWait(self):
        self.assertTrue(self.cashier.pay(0)<0)

    def testPayFromOpenSession(self):
        self.initBasket()
        self.initUnknownRef()
        when(Cashier).proofreadingRequest().thenReturn(True)

        when(self.scan).proofreadingDone().thenReturn(True)
        self.assertEqual(0,self.cashier.connection(self.scan))
        self.assertEqual(0,self.cashier.openSession())
        self.assertTrue(self.cashier.pay(0)<0)








if __name__ == '__main__':
    unittest.main()
