from collections import namedtuple
import enum


ThemeQuestion = namedtuple(
    "ThemeQuestion",
    ("theme_id", "id", "value", "answer_variants", "answer_type", "correct_answer")
)


@enum.unique
class AnswerTypes(str, enum.Enum):
    ONLY_ONE = "only_one"
    MULTI = "multi"
