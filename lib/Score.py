from lib.LineOfNumbers import LineOfNumbers

class Score(LineOfNumbers):
    """This is 1 way to guarantee that we don't lose the score
    but it isn't flexible.  What if we have 2 players?"""
    
    score = 0
    
    def __init__(self, ix, iy, fontrequested, color, score=0):
        super().__init__(ix, iy, fontrequested, color)

    def draw(self, screen):
        tempscore = "%010d" % Score.score

        for i in range(0, 10):
            val = int(tempscore[i])
            screen.blit(self.numbers[val],   (self.x  + i * 20, self.y))

    def addscore(self, bonus:int) -> None:
        Score.score += bonus
        self.mis_steps = 0

    def getscore(self) -> int:
        return Score.score

