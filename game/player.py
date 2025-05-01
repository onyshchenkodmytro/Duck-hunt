

class Player:
    def __init__(self):
        self.bullets = 3
        self.lives = 5
        self.score = 0

    def shoot(self):
        if self.bullets > 0:
            self.bullets -= 1
            return True
        return False

    def reload(self):
        self.bullets = 3

    def lose_life(self, count=1):
        self.lives -= count

    def is_alive(self):
        return self.lives > 0
