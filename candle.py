class Candle:
    #represents a candle

    minute: int     # opening minute
    open:   float   # open price
    close:  float   # closing price
    low:    float   # low of the minute
    high:   float   # high of the minute
    volume: float   # total volume traded in the minute
    opened: bool    # if the candle is currently trading
    useable: float  # if the candle is useable

    """
    Initializes a candle

    Inputs:
    -- minute: The opening minute of the candle
    -- price: The price of the trade
    -- volume: The volume of the trade
    Outputs:
    -- None
    """
    def __init__(self, minute, price, volume):
        self.minute = minute
        self.open = price
        self.high = price
        self.low = price
        self.close = -1
        self.volume = volume
        self.opened = True
        self.useable = True


    """
    Updates the values of the candle

    Inputs:
    -- price: The price of the trade
    -- volume: The volume of the trade
    Outputs:
    -- None

    Prints an error if the candle is not currently being traded (this should not happen ever)
    If it does occur, the candle is no longer usable. 
    """
    def updateCandle(self, price, volume):
        if (not self.opened):
            print("ERROR, tried to access a closed or nonexistent candle.")
            self.useable = False

        self.high = max(self.low, price)
        self.low = min(self.low, price)
        self.volume += volume


    """
    Updates the candle's values and closes the candle.

    Inputs:
    -- price: The price of the last trade
    -- volume: The volume of the last trade
    Outputs:
    -- None

    Prints an error if the candle is not currently being traded (this should not happen ever)
    If it does occur, the candle is no longer usable. 
    """
    def closeCandle(self, price, volume):
        if (not self.opened):
            print("ERROR, tried to access a closed or nonexistent candle.")
            self.useable = False

        self.high = max(self.low, price)
        self.low = min(self.low, price)
        self.close = price
        self.volume += volume
        self.opened = False

    
    """
    Sets a candle as unusable.
    """
    def setUnusable(self):
        self.useable = False


    """
    Exports the candle info as a list

    Inputs:
    -- None
    Outputs:
    -- List of candle values as: [minute, open, high, low, close, volume, usability]
    """
    def exportCandleInfo(self):
        return [self.minute, self.open, self.high, self.low, self.close, self.volume, self.useable]
        

    def __repr__(self):
        return self.__str__()


    def __str__(self):
        return f"Candle(min={self.minute}, O={self.open}, H={self.high}, L={self.low}, C={self.close}, V={self.volume}, usable = {self.useable})"