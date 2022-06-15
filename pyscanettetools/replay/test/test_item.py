import unittest
from ..src.Item import Item

class TestItem(unittest.TestCase):

    def setUp(self):
        self.item = Item(3474377910731, 1.1, "Marker pour tableau blanc Maxiflo")

    def testItem0(self):
        self.assertEqual(3474377910731, self.item.codeEAN13)
        self.assertTrue(self.item.unitaryPrice,1.1)
        self.assertEqual("Marker pour tableau blanc Maxiflo", self.item.name);

    def testItem1(self):
        self.assertTrue(self.item.isValidEAN13())

    def testItem2(self):
        i=Item(123, 0, "Item with code ok (key > 0)")
        self.assertTrue(i.isValidEAN13())

    def testItem3(self):
        i=Item(1232, 0, "Item with wrong code")
        self.assertFalse(i.isValidEAN13())

    def testItem4(self):
        i=Item(130, 0, "item with code ok (key = 0)")
        self.assertTrue(i.isValidEAN13())

    def testItem5(self):
        i=Item(1232, 0, "Article avec code erroné")
        self.assertFalse(i.__eq__(self.item))

    def testItem6(self):
        i = Item(3474377910731, 0, "Marker Maxiflo")
        self.assertTrue(i.__eq__(self.item))

    def testItem7(self):
        i=Item(-3474377910731, 0, "Article avec code erroné")
        self.assertFalse(i.isValidEAN13())

    def testItem8(self):
        i=Item(45496420598, 0, "Minecraft Switch")
        self.assertTrue(i.isValidEAN13())

    def testItem9(self):
        i=Item(45496420598, 0, None)
        self.assertTrue(i.name=="")

    def testItem10(self):
        self.assertFalse(self.item.__eq__(None))

    def testItem11(self):
        self.assertTrue(self.item.__eq__(self.item))

    def testItem12(self):
        i=Item(13474377910731, 1.1, "Marker")
        self.assertFalse(i.isValidEAN13())

    def testItem13(self):
        i=Item(34743779107310, 1.1, "Marker")
        self.assertFalse(i.isValidEAN13())

    def testItem14(self):
        i1=Item(1,0,"")
        i2=Item(1,0,"")
        i3=Item(2,0,"")

        s=set([i1,i2,i3])
        self.assertTrue(len(s)==2)
        self.assertTrue(i1 in s)
        self.assertTrue(i2 in s)
        self.assertTrue(i3 in s)
        self.assertTrue(Item(2,1,"toto") in s)



if __name__ == '__main__':
    unittest.main()
