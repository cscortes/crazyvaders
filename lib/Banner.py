from lib.StaticObject import StaticObject
import numpy as np

class Banner(StaticObject):
    RENDERED : dict = {}

    def __init__(self, word, fontrequested, color, pos = (0,0), spacing=20):
        super().__init__()
        self.pos = pos
        self.word = word
        self.font = fontrequested
        self.color = color
        self.spacing = spacing
    
    def draw(self, screen):
        for idx, ch in enumerate(self.word):
            offset =  np.add(self.pos , (idx*self.spacing, 0))
            screen.blit(self.get_rendr(ch), offset)

    def get_rendr(self, ch):
        if not ch in Banner.RENDERED.keys():
            Banner.RENDERED[ch] = self.font.render(ch, 1, self.color)

        return Banner.RENDERED[ch]
