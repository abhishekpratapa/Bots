import bot
from enum import Enum

# Enum type Stocks
class StockType(Enum):
    All = 1
    NASDAQ = 2
    NYSE = 3
    DAX = 4


#Stocks App
class Stock:
    def __init__(self, market=StockType.All):
        pass
