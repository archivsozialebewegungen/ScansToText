'''
Created on 23.01.2021

@author: michael
'''
import unittest
from injector import Injector
from ImageToTextService import ImageToTextService,\
    ProcessorsModule, LineBreakPostProcessor
import difflib
from ImageTools import load
import re

class Test(unittest.TestCase):


    def setUp(self):
        
        injector = Injector([ProcessorsModule()])
        self.img_to_text_service = injector.get(ImageToTextService)  


    def testExtradienstSeite4(self):
        
        img = load("testdata/ExtradienstSeite4.tif")
        ocr_text = self.img_to_text_service.get_text(img)
        self.assertDiffs("testdata/ExtradienstSeite4.txt", ocr_text, 6)
    
    def assertDiffs(self, gold_standard, ocr_text, max_allowed):
        
        file = open("/tmp/out.txt", "w")
        file.write(ocr_text)
        file.close()
        file = open(gold_standard, "r")
        text = file.read()
        file.close()
        diff = ''.join(list(difflib.unified_diff(text, ocr_text)))
        matches = re.findall('@@[0-9,\-\+\s]+@@', diff)
        
        self.assertTrue(len(matches) <= max_allowed, "More than %d differences: %d." % (max_allowed, len(matches)))
        
        return len(matches)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testExtradienstSeite4']
    unittest.main()