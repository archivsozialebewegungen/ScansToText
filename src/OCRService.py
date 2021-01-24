'''
Created on 23.01.2021

@author: michael
'''
import pytesseract
from PIL import Image
from injector import singleton, inject
import layoutparser
from ImageTools import pil_to_numpy, numpy_to_pil
from layoutparser.elements import TextBlock, Rectangle

class SortableBlock:
    
    def __init__(self, block):
        
        self.block = block

    def _x_equals(self, other):
        
        return abs(self.upper_left_x - other.upper_left_x) < 10

    def _y_equals(self, other):
        
        return abs(self.upper_left_y - other.upper_left_y) < 10

    def __lt__(self, other):
        '''
        Smaller means:
        '''
                
        if not self._x_equals(other):
            return self.upper_left_x < other.upper_left_y
        
        if not self._y_equals(other):
            return self.upper_left_y < other.upper_left_y
        
        return False

    def __eq__(self, other):
        
        return not self < other and not other < self

    def __ne__(self, other):
    
        return self < other or other < self
    
    def __gt__(self, other):
    
        return other < self
    
    def __ge__(self, other):
    
        return not self < other
    
    def __le__(self, other):
    
        return not other < self
    
    def __str__(self):
        
        return "%d|%d:%d|%d" % (self.upper_left_x, self.upper_left_y,
                                self.lower_right_x, self.lower_right_y)
              
    upper_left_x = property(lambda self: int(self.block.block.y_1))
    upper_left_y = property(lambda self: int(self.block.block.x_1))
    lower_right_x = property(lambda self: int(self.block.block.y_2))
    lower_right_y = property(lambda self: int(self.block.block.x_2))
    
class BlockDetector:
    
    def __init__(self, model_uri='lp://PrimaLayout/mask_rcnn_R_50_FPN_3x/config'):
        
        self.model = layoutparser.Detectron2LayoutModel(model_uri)

    def get_image_blocks(self, img):
        
        blocks = self.split_image(img)
        blocks.sort()
        return self.blocks_to_images(blocks, img)
        
    def blocks_to_images(self, blocks, img):

        ndarray = pil_to_numpy(img)
        print(ndarray.shape)
        images = []
        for block in blocks:
            print(block)
            block_img = Image.fromarray(ndarray[
                                                block.upper_left_y:block.lower_right_y,
                                                block.upper_left_x:block.lower_right_x,
                                                ], img.mode)
            images.append(block_img)
            block_img.show()
            input("Wait...")
        return images
    
    def split_image(self, img):
        '''
        Receives an image, performs layout analysis and returns
        an array of images in the correct order for running ocr
        '''
        layout = self.model.detect(img)
        blocks = []
        for text_block in layout:
            if type(text_block) != TextBlock:
                raise Exception("Unexpected layout element %s" % type(text_block))
            if type(text_block.block) != Rectangle:
                raise Exception("Unexpected block type %s" % type(text_block.block))
            if text_block.score < 0.9:
                continue
            blocks.append(SortableBlock(text_block))
        return blocks

@singleton
class OCRService(object):
    '''
    classdocs
    '''
    
    @inject
    def __init__(self, block_detector: BlockDetector):
        
        self.lang = "deu"
        self.block_detector = block_detector
    
    def get_text(self, img: Image):
    
        img_blocks = self.block_detector.get_image_blocks(img)
        text = ""
        for block in img_blocks:
            text += "\n" + pytesseract.image_to_string(block, lang=self.lang) 
        return text