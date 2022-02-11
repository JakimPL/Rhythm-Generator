class LilyException(Exception):
    pass


class InvalidBeatException(LilyException):
    pass


class EmptyScoreException(LilyException):
    pass


class NoteNotSupportedError(LilyException):
    pass


class InvalidPhraseSetError(LilyException):
    pass
