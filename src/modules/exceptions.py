class RhygenException(Exception):
    pass


class InvalidBeatException(RhygenException):
    pass


class EmptyScoreException(RhygenException):
    pass


class NoteNotSupportedError(RhygenException):
    pass


class InvalidPhraseSetError(RhygenException):
    pass
