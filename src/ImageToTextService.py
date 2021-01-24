'''
Created on 23.01.2021

@author: michael
'''
from optparse import OptionParser
from PIL import Image
from OCRService import OCRService
from ImageTools import load
from injector import inject, singleton, Injector, Module, BoundKey, provider
import re

PREPROCESSORS = BoundKey("key_preprocessors")
POSTPROCESSORS = BoundKey("key_postprocessors")

@singleton
class ImageToTextService:
    
    @inject
    def __init__(self, ocr_service: OCRService,
                 pre_processors: PREPROCESSORS,
                 post_processors: POSTPROCESSORS):
        
        self.ocr_service = ocr_service
        self.pre_processors = pre_processors
        self.post_processors = post_processors
    
    def get_text(self, img: Image):
        
        img = self.preprocess_image(img)
        text = self.ocr_service.get_text(img)
        return self.postprocess_text(text)

    def preprocess_image(self, img):
        
        for preprocessor in self.pre_processors:
            img = preprocessor.process_img(img)
        return img
    
    def postprocess_text(self, text):
        
        for postprocessor in self.post_processors:
            text = postprocessor.process_text(text)
            
        return text

class PostProcessor:
    
    def process_text(self, text):
        
        raise Exception("Implement in child class")

class LineBreakPostProcessor(PostProcessor):
    
    def process_text(self, text):

        text = text.replace("Mai-\nko", "Maiko")        
        # There seems to be no possibility to define a unicode lower case
        # pattern
        text = re.sub(r"-\s*(\n\s*)+(?=[a-zäöüß])", "", text)
        text = re.sub("\s*\n(\s*\n\s*)+", "@@@PARAGRAPH@@@", text)
        text = re.sub("-\s*\n\s*", "-", text)
        text = re.sub("\s*\n\s*", " ", text)
        text = text.replace("@@@PARAGRAPH@@@", "\n")
        return text

class QuotesPostProcessor(PostProcessor):
    
    def process_text(self, text):
        
        text = text.replace("’’", "”")
        text = text.replace("‚‚", "„")
        return text
    
class ProcessorsModule(Module):

    @provider
    @singleton
    @inject
    def create_preprocessors(self) -> PREPROCESSORS:
        
        return list()

    @provider
    @singleton
    @inject
    def create_postprocessors(self) -> POSTPROCESSORS:
        
        return (LineBreakPostProcessor(), QuotesPostProcessor())

def main():
    input_file, lang = get_opts()
    image = load(input_file)
    injector = Injector()
    image_to_text_service = injector.get(ImageToTextService)
    image_to_text_service.lang = lang
    print(image_to_text_service.get_text(image))

def get_opts():
    parser = OptionParser(usage="Usage: %prog <input-file>")
    parser.add_option("-l", "--lang",
                      dest="lang",
                      action="store",
                      default="deu",
                      help="Set language")
    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("Incorrect number of arguments")

    return args[0], options.lang;

if __name__ == '__main__':
    main()