import unittest
from ..src.ItemsDB import ItemsDB


class TestItemsDB(unittest.TestCase):

    def setUp(self):
        self.folderPath="../csv/"

    def testItemsDB0bis(self):
        self.assertRaises(IOError,ItemsDB,bycsv=True,path=self.folderPath+"produits.txt")

    def testItemsDB1(self):
        db=ItemsDB(bycsv=True,path=self.folderPath+'emptyFile.csv')
        self.assertEqual(0,db.getSizeDB())


    def testItemsDB2(self):
        db=ItemsDB(bycsv=True,path=self.folderPath+'validFileWithDuplicates.csv')
        self.assertEqual(1,db.getSizeDB())
        i=db.getArticle(3474377910731)
        self.assertTrue(i.isValidEAN13())
        self.assertTrue(i.unitaryPrice>0)
        self.assertNotEqual(None,i.name)
        self.assertNotEqual(0,len(i.name))


if __name__ == '__main__':
    unittest.main()
