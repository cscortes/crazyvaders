from lib.StaticObject import StaticObject

class LineOfNumbers(StaticObject):
    def __init__(self, ix, iy, fontrequested, color):
        super().__init__()
        self.x = ix
        self.y = iy
        self.numbers = self.create_bag_numbers(fontrequested, color)
        
    def create_bag_numbers(self, font, color):
        bag = []
        for i in range(0,10):
            bag.append(font.render("%d" % i, 1, color))
        return bag 

    def draw(self, screen):
        for i in range(0, 20):
           screen.blit(self.numbers[i % 10],   (self.x  + i * 20, self.y))
