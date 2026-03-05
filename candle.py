class Candle:
    "represents a candle"
    minute: int
    open:   float
    close:  float
    low:    float
    high:   float
    volume: float
    opened: bool
    useable: float

    def __init__(self, minute, price, volume):
        self.minute = minute
        self.open = price
        self.high = price
        self.low = price
        self.close = -1
        self.volume = volume
        self.opened = True
        self.useable = True

    def updateCandle(self, price, volume):
        if (not self.opened):
            print("ERROR, tried to access a closed or nonexistent candle.")
            self.useable = False

        self.high = max(self.low, price)
        self.low = min(self.low, price)
        self.volume += volume

    def closeCandle(self, price, volume):
        if (not self.opened):
            print("ERROR, tried to access a closed or nonexistent candle.")
            self.useable = False

        self.high = max(self.low, price)
        self.low = min(self.low, price)
        self.close = price
        self.volume += volume
        self.opened = False

    def setUnusable(self):
        self.useable = False

    def exportCandleInfo(self):
        return [self.minute, self.open, self.high, self.low, self.close, self.volume, self.useable]
        
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"Candle(min={self.minute}, O={self.open}, H={self.high}, L={self.low}, C={self.close}, V={self.volume}, usable = {self.useable})"