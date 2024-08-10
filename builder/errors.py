# encoding: utf-8
class BuilderError(Exception):
    """Base class for exceptions related to building processes.

    Attributes:
        message (str)   : Description of the error.
        info (str)      : Additional information about the error context.
    """

    def __init__(self, message, info=""):
        self.message = message
        self.info = info
        super().__init__(message)

    def __str__(self):
        if self.info:
            return f"{self.message} ({self.info})"
        return self.message


class BuilderConfigError(BuilderError):
    """ Exception raised for errors in the configuration of the builder."""

    def __init__(self, message="Invalid configuration", info=""):
        super().__init__(message, info)


class BuilderValidationError(BuilderError):
    """ Exception raised for errors in the validation of builder parameters."""
    def __init__(self, message="Validation failed", info=""):
        super().__init__(message, info)


def main():
    """Main function for testing the BuilderError class."""

    try:
        raise BuilderError("An error occurred")
    except BuilderError as e:
        print(str(e))


if __name__ == "__main__":
    main()
