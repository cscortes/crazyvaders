from GameObject import GameObject


class MovingBox(GameObject):
    STEP = 10 
    def __init__(self, ix = 30, iy = 30, iwidth=60, iheight=60, iblue=True):
        super().__init__()
        self.is_blue = iblue
        self.x = ix
        self.y = iy
        self.width = iwidth
        self.height = iheight

    def process_events(self, evt):
        if evt.type == pygame.KEYDOWN and evt.key == pygame.K_SPACE:
            self.is_blue = not self.is_blue

        # render text
        if self.is_blue: self.color = COLOR_BLUE
        else: self.color = COLOR_ORANGE

    def process_keys(self, pressed):
        if pressed[pygame.K_UP]: 
            self.fire_missile()

        if pressed[pygame.K_LEFT]: self.x -= self.STEP
        if pressed[pygame.K_RIGHT]: self.x += self.STEP

    def fire_missile(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))
