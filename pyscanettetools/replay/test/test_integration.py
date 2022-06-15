import unittest
from mockito import unstub
from ..src.Cashier import Cashier
from ..src.Scanner import Scanner

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.folderPath="C:/Users/QZTD9928/Documents/code/pyscannetteAgilkia/csv/"
        self.myCashier=Cashier(bycsv=True,path=self.folderPath+'produitsOK.csv')
        self.myScanner=Scanner(bycsv=True,path=self.folderPath+'produitsOK.csv')
    def tearDown(self):
        unstub()
    def initBasket(self):
        self.myScanner.unlock()
        self.myScanner.scan(5410188006711)
        self.myScanner.scan(5410188006711)
        self.myScanner.scan(5410188006711)
        self.myScanner.scan(8715700110622)
        self.myScanner.scan(8715700110622)
        self.myScanner.scan(45496420598)

        self.totalBasket=3*2.15+0.96*2+52.24

    def initEmptyBasket(self):
        self.myScanner.unlock()

    def transferAndProofreading(self):
        code=self.myScanner.transmission(self.myCashier)
        if (code==1):
            self.assertEqual(0, self.myScanner.scan(5410188006711))
            self.assertEqual(0, self.myScanner.scan(5410188006711))
            self.assertEqual(0, self.myScanner.scan(5410188006711))
            self.assertEqual(0, self.myScanner.scan(8715700110622))
            self.assertEqual(0, self.myScanner.scan(8715700110622))
            self.assertEqual(0, self.myScanner.scan(45496420598))
            code=self.myScanner.transmission(self.myCashier)
        self.assertEqual(0,code)

    def initUnknownRefs(self):
        self.myScanner.scan(1)

    def testConnection0_notProofread(self):
        self.initEmptyBasket()
        self.transferAndProofreading()
        self.assertTrue(self.myCashier.pay(0)<0)
        self.assertEqual(-1,self.myCashier.connection(self.myScanner))


    def testDeletionNonExistentProduct(self):
        self.initBasket()
        self.initUnknownRefs()
        self.transferAndProofreading()
        self.assertEqual(0,self.myCashier.openSession())
        self.assertEqual(-2,self.myCashier.scan(5410188006712))
        self.assertEqual(0,self.myCashier.closeSession())
        self.assertAlmostEqual(first=2.15, second=self.myCashier.pay(self.totalBasket+2.15), delta=0.001)

    def testAbandonFromWaiting(self):
        self.initBasket()
        self.myCashier.abandon()
        self.transferAndProofreading()

    def testAbandonFromPayment(self):
        #todo
        pass

    def testAbandonFromWaitingCashier(self):
        self.initBasket()
        self.initUnknownRefs()
        self.transferAndProofreading()
        self.myCashier.abandon()
        self.initBasket()
        self.transferAndProofreading()

    def testAbandonFromAuthentifiedCashier(self):
        self.initBasket()
        self.initUnknownRefs()
        self.transferAndProofreading()
        self.assertEqual(0,self.myCashier.openSession())
        self.myCashier.abandon()
        self.initBasket()
        self.transferAndProofreading()



    def testComplicatedScenario(self):
        #empty basket
        self.initEmptyBasket()
        #unknown references
        self.initUnknownRefs()
        self.transferAndProofreading()
        self.assertEqual(0,self.myCashier.openSession())
        self.assertEqual(0, self.myCashier.scan(5410188006711))
        self.assertEqual(0, self.myCashier.scan(45496420598))
        #cashier is deleting three products

        self.assertEqual(0, self.myCashier.delete(5410188006711))
        self.assertEqual(0, self.myCashier.delete(45496420598))
        self.assertEqual(-2, self.myCashier.delete(8715700110622))
        #
        # #closing the session
        self.assertEqual(0, self.myCashier.closeSession())
        #
        #-->must be pending
        self.initEmptyBasket()
        self.transferAndProofreading()
    def testConnectionThenAbandonThenConnection(self):
        self.initBasket()
        self.transferAndProofreading()
        self.myCashier.abandon()
        self.myScanner.unlock()
        self.myScanner.scan(3017620402678)
        i=self.myScanner.transmission(self.myCashier)
        if i == 1:
            self.myScanner.scan(3017620402678)
            i = self.myScanner.transmission(self.myCashier)
        self.assertEqual(0, i)
        self.assertAlmostEqual(first=0, second=self.myCashier.pay(1.67), delta=0.01)
    def testTwoPayments(self):
        self.initBasket()
        self.transferAndProofreading()
        self.assertAlmostEqual(first=0, second=self.myCashier.pay(self.totalBasket), delta=0.01)
        self.myScanner.unlock()
        self.myScanner.scan(3017620402678)
        i=self.myScanner.transmission(self.myCashier)
        if i==1:
            self.myScanner.scan(3017620402678)
            i=self.myScanner.transmission(self.myCashier)
        self.assertEqual(0,i)
        self.assertAlmostEqual(first=0, second=self.myCashier.pay(1.67), delta=0.01)



if __name__ == '__main__':
    unittest.main()
