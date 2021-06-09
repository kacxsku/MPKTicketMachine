class NotIntValueError(Exception):
    """Exception thrown when value on spinbox is not inteeger"""
    def __init__(self):
        super().__init__()


class NegativeNumberValueError(Exception):
    """Exception thrown when value on spinbox is negative"""
    def __init__(self):
        super().__init__()
