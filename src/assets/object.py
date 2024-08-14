from src.asset import Asset


class Object(Asset):
    """
    A super class for all types of objects like blocks, borders, etc.
    """

    def __init__(self) -> None:
        """
        Creates an instance of this class.
        """
        super().__init__()
