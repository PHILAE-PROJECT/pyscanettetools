import unittest
from ..src.Cashier import Cashier
from ..src.Scanner import Scanner
from ..src.Scanner import ProductDBFailureException
from ..src.Item import Item
import mockito
from mockito import when,unstub

class TestScanner(unittest.TestCase):

    def setUp(self):
        self.folderPath="C:/Users/QZTD9928/Documents/code/pyscannetteAgilkia/csv/"
        self.scan=Scanner(True,self.folderPath+"produitsOK.csv")
    def tearDown(self) -> None:
        unstub()
    def testInitializationKO_fileDoesNotExist(self):
        self.assertRaises(ProductDBFailureException,Scanner,True,self.folderPath)

    def testInitializationKO_fileKO(self):
        self.assertRaises(ProductDBFailureException,Scanner,True,self.folderPath+"produitsKO.csv")

    def testUnlockingOK(self):
        self.assertEqual(0,len(self.scan.getItems()))
        self.assertEqual(0,len(self.scan.unknownReferences))
        self.assertEqual(0,self.scan.unlock())
        self.assertEqual(-1,self.scan.unlock())
        self.assertEqual(0,len(self.scan.getItems()))
        self.assertEqual(0,len(self.scan.unknownReferences))

    def testUnlockingThenRelocking(self):
        self.assertEqual(0,self.scan.unlock())
        self.scan.abandon()
        self.assertEqual(0,len(self.scan.getItems()))
        self.assertEqual(0,len(self.scan.unknownReferences))
        self.assertEqual(0,self.scan.unlock())


    def testUnlockAfterAbandonAndBasketNotEmpty(self):
        #unlocking
        self.assertEqual(0,self.scan.unlock())
        #scanning one item
        self.scan.scan(5410188006711)
        #abandon
        self.scan.abandon()
        self.assertEqual(0, len(self.scan.getItems()))
        self.assertEqual(0, len(self.scan.unknownReferences))
        #unlocking again
        self.assertEqual(0, self.scan.unlock())
        self.assertEqual(0, len(self.scan.getItems()))
        self.assertEqual(0, len(self.scan.unknownReferences))

    def testAbandonFromLocked(self):
        self.scan.abandon()
        self.assertEqual(0, self.scan.unlock())

    def testAbandonThenProofReadingOK(self):
        mockCashier=mockito.mock(spec=Cashier)
        when(mockCashier).connection(self.scan).thenReturn(1)
        self.assertEqual(0,self.scan.unlock())
        self.assertEqual(0,self.scan.scan(5410188006711))
        self.assertEqual(-2, self.scan.scan(5410188006712))
        self.assertEqual(1, self.scan.transmission(mockCashier))
        self.scan.abandon()

        self.assertEqual(0, len(self.scan.getItems()))
        self.assertEqual(0, len(self.scan.unknownReferences))
        self.assertEqual(0, self.scan.unlock())

    def testAbandonThenProofReadingKO(self):
        mockCashier = mockito.mock(spec=Cashier)
        when(mockCashier).connection(self.scan).thenReturn(1)
        self.assertEqual(0, self.scan.unlock())
        self.assertEqual(-2, self.scan.scan(5410188006712))
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(1, self.scan.transmission(mockCashier))
        self.assertEqual(-3, self.scan.scan(8715700110622))
        self.scan.abandon()

        self.assertEqual(0, len(self.scan.getItems()))
        self.assertEqual(0, len(self.scan.unknownReferences))
        self.assertEqual(0, self.scan.unlock())

    def testScanThenLockedState(self):
        self.assertEqual(-1, self.scan.scan(5410188006711))
        self.assertEqual(0, len(self.scan.getItems()))
        self.assertEqual(0, len(self.scan.unknownReferences))

    def testScanFromProofreadingOK(self):
        mockCashier = mockito.mock(spec=Cashier)
        when(mockCashier).connection(self.scan).thenReturn(1)
        self.assertEqual(0, self.scan.unlock())
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(1, self.scan.transmission(mockCashier))
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(-1, self.scan.scan(5410188006711))
        self.assertEqual(-1, self.scan.scan(8715700110622))


    def testScanFromProofreadingKO(self):
        mockCashier = mockito.mock(spec=Cashier)
        when(mockCashier).connection(self.scan).thenReturn(1)
        self.assertEqual(0, self.scan.unlock())
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(1, self.scan.transmission(mockCashier))
        self.assertEqual(-3, self.scan.scan(8715700110622))
        self.assertEqual(-1, self.scan.scan(5410188006711))
        self.assertEqual(-1, self.scan.scan(8715700110622))


    def testScanASingleItem(self):
        self.assertEqual(0, self.scan.unlock())
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(1, self.scan.quantity(5410188006711))
        self.assertEqual(1, len(self.scan.getItems()))
        self.assertEqual(0, len(self.scan.unknownReferences))

    def testScanTwoDifferentItems(self):
        self.assertEqual(0, self.scan.unlock())
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(0, self.scan.scan(8715700110622))
        self.assertEqual(1, self.scan.quantity(5410188006711))
        self.assertEqual(1, self.scan.quantity(8715700110622))
        self.assertEqual(2, len(self.scan.getItems()))
        self.assertTrue(Item(5410188006711, 0, "") in self.scan.getItems())
        self.assertTrue(Item(8715700110622, 0, "") in self.scan.getItems())
        self.assertEqual(0, len(self.scan.unknownReferences))

    def testScanTwoSameItems(self):
        self.assertEqual(0, self.scan.unlock())
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(2, self.scan.quantity(5410188006711))
        self.assertEqual(0, self.scan.quantity(8715700110622))
        self.assertEqual(1, len(self.scan.getItems()))
        self.assertTrue(Item(5410188006711, 0, "") in self.scan.getItems())
        self.assertEqual(0, len(self.scan.unknownReferences))

    def testScanMultipleUnkwownReferences(self):
        self.assertEqual(0, self.scan.unlock())
        self.assertEqual(-2, self.scan.scan(5410188006710))
        self.assertEqual(-2, self.scan.scan(5410188006710))
        self.assertEqual(-2, self.scan.scan(5410188006712))
        self.assertEqual(0, len(self.scan.getItems()))
        self.assertTrue(5410188006710 in self.scan.unknownReferences)
        self.assertTrue(5410188006712 in self.scan.unknownReferences)

    def testScanMultipleItemsWithUnknownReferences(self):
        self.assertEqual(0, self.scan.unlock())
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(-2, self.scan.scan(5410188006712))
        self.assertEqual(0, self.scan.scan(8715700110622))
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(-2, self.scan.scan(5410188006710))
        self.assertEqual(2, self.scan.quantity(5410188006711))
        self.assertEqual(1, self.scan.quantity(8715700110622))
        self.assertEqual(2, len(self.scan.getItems()))
        self.assertTrue(Item(5410188006711, 0, "") in self.scan.getItems())
        self.assertTrue(Item(8715700110622, 0, "") in self.scan.getItems())
        self.assertEqual(2, len(self.scan.unknownReferences))
        self.assertTrue(5410188006710 in self.scan.unknownReferences)
        self.assertTrue(5410188006712 in self.scan.unknownReferences)

    def testScanProofreading1(self):
        mockCashier = mockito.mock(spec=Cashier)
        when(mockCashier).connection(self.scan).thenReturn(1)
        self.scan.unlock()
        self.scan.scan(5410188006711)
        self.scan.scan(5410188006711)
        self.scan.scan(5410188006711)
        self.scan.scan(8715700110622)
        self.scan.scan(8715700110622)
        self.assertEqual(1, self.scan.transmission(mockCashier))
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(-3, self.scan.scan(5410188006710))
        self.assertEqual(-1, self.scan.scan(8715700110622))

    def testScanProofreading2(self):
        mockCashier = mockito.mock(spec=Cashier)
        when(mockCashier).connection(self.scan).thenReturn(1)
        self.scan.unlock()
        self.scan.scan(5410188006711)
        self.scan.scan(5410188006711)
        self.scan.scan(5410188006711)
        self.scan.scan(8715700110622)
        self.scan.scan(8715700110622)
        self.assertEqual(1, self.scan.transmission(mockCashier))
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(0, self.scan.scan(5410188006711))
        self.assertEqual(0, self.scan.scan(8715700110622))
        self.assertEqual(0, self.scan.scan(8715700110622))
        self.assertEqual(-1, self.scan.scan(8715700110622))
        self.assertEqual(-1, self.scan.scan(8715700110621))
        self.assertEqual(3, self.scan.quantity(5410188006711))
        self.assertEqual(2, self.scan.quantity(8715700110622))
        self.assertEqual(2, len(self.scan.getItems()))

    def testScanProofreading3(self):
        mockCashier = mockito.mock(spec=Cashier)
        when(mockCashier).connection(self.scan).thenReturn(1)
        self.scan.unlock()
        for i in range(15):
            self.scan.scan(5410188006711)
        self.assertEqual(15, self.scan.quantity(5410188006711))
        self.assertEqual(1, len(self.scan.getItems()))
        self.assertEqual(0, len(self.scan.unknownReferences))
        self.assertEqual(1, self.scan.transmission(mockCashier))
        for i in range(12):
            self.assertEqual(0, self.scan.scan(5410188006711))

        self.assertEqual(-1, self.scan.scan(5410188006711))
        self.assertEqual(15, self.scan.quantity(5410188006711))
        self.assertEqual(1, len(self.scan.getItems()))
        self.assertEqual(0, len(self.scan.unknownReferences))

    def testScanProofreading4(self):
        scan=Scanner(bycsv=True,path=self.folderPath+'produits.csv')
        mockCashier = mockito.mock(spec=Cashier)
        when(mockCashier).connection(scan).thenReturn(1)
        scan.unlock()
        all17Items=[5410188006711, 3560070048786, 3017800238592, 3560070976478,
                3046920010856, 8715700110622, 3570590109324, 3520115810259, 3270190022534,
                8718309259938, 3560071097424, 3017620402678, 3245412567216, 45496420598,
                7640164630021, 3560070139675, 3020120029030]
        for ean13 in all17Items:
            self.assertEqual(0, scan.scan(ean13))
        self.assertEqual(1, scan.transmission(mockCashier))
        for i in range(12):
            self.assertEqual(0, scan.scan(all17Items[i]))

        self.assertEqual(-1,scan.scan(3560070139675))

    def testScanProofReading5(self):
        mockCashier = mockito.mock(spec=Cashier)
        when(mockCashier).connection(self.scan).thenReturn(1)
        self.scan.unlock()
        self.scan.scan(5410188006710)
        self.scan.scan(8715700110622)
        self.scan.transmission(mockCashier)
        self.assertEqual(-3, self.scan.scan(5410188006710))
        self.assertEqual(-1, self.scan.scan(8715700110622))



if __name__ == '__main__':
    unittest.main()
