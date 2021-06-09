class NotIntValueError(Exception):
    """Exception thrown when value on spinbox is not inteeger"""
    def __init__(self,info):
        super().__init__(info)


class NegativeNumberValueError(Exception):
    """Exception thrown when value on spinbox is negative"""
    def __init__(self,info):
        super().__init__(info)
