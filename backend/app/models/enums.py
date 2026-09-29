import enum

from sqlalchemy import Enum as SAEnum


class CatSection(str, enum.Enum):
    VARC = "VARC"
    DILR = "DILR"
    QA = "QA"


class CatQuestionType(str, enum.Enum):
    MCQ = "MCQ"
    TITA = "TITA"


class CatQuestionSource(str, enum.Enum):
    PYQ = "pyq"
    AI_GENERATED = "ai_generated"


class CatTestType(str, enum.Enum):
    FULL_MOCK = "full_mock"
    SECTIONAL = "sectional"
    TOPIC_DRILL = "topic_drill"


class CatMockTestStatus(str, enum.Enum):
    GENERATING = "generating"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    SUBMITTED = "submitted"


class CatWeakConceptStatus(str, enum.Enum):
    FLAGGED = "flagged"
    DRILLING = "drilling"
    RESOLVED = "resolved"


class CatPIStatus(str, enum.Enum):
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"


def sa_enum(enum_cls, name: str) -> SAEnum:
    """Build a SQLAlchemy Enum column type that stores each member's `.value`
    (e.g. "generating") rather than its `.name` (e.g. "GENERATING")."""
    return SAEnum(enum_cls, name=name, values_callable=lambda obj: [member.value for member in obj])
