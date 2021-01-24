'''
Created on 23.01.2021

@author: michael
'''
import unittest
from ImageToTextService import LineBreakPostProcessor, QuotesPostProcessor


class Test(unittest.TestCase):


    def setUp(self):
        
        self.postprocessors = (LineBreakPostProcessor(), QuotesPostProcessor())

    def run_processors(self, pre, post):
        
        text = pre
        for p in self.postprocessors:
            text = p.process_text(text)
        self.assertEqual(post, text)

    def testName(self):
        
        self.maxDiff = None
        self.run_processors("Aus-\n tritt\n\naus\ndem Mai- \n\nkomi- \n tee", "Austritt\naus dem Maikomitee")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()