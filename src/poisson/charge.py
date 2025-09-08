class Charge:
    def __init__(self, x, y, sign):
        self.x = x
        self.y = y
        self.sign = sign

    def __str__(self) -> str:
        return f"This is a charge with sign {self.sign} at position (x,y) = ({self.x},{self.y})"
