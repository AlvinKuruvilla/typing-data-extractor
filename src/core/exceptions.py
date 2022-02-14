class NotCSVFileError(Exception):
    """Exception raised if provided path is not a csv file.

    Attributes:
        path -- input path which caused the error
        message -- explanation of the error
    """

    def __init__(self, path, message):
        self.path = path
        self.message = message
        super().__init__(self.message)


class Invalid_Verifier(Exception):
    """Exception raised if provided verifier is not valid.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
