class MGFFileNotFoundError(FileNotFoundError):
    """Exception raised when an MGF file cannot be found."""

    def __init__(self, filepath: str) -> None:
        message = f"No such file or directory: '{filepath}'"
        super().__init__(message)
        self.filepath = filepath
