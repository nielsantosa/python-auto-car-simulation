class IOReadWrite:
    """
    Wrapper for read and write interface with User.
    """

    def write_string(self, text: str):
        print(text)

    def read_string(self) -> str:
        return input()
