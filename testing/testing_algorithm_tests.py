import pytest

from .models import Answers


@pytest.mark.parametrize('answers, expected', [

])
@pytest.mark.django_db
def test_should_calculate_correct_answers(
    answers: list[Answers],
    expected: dict[str, int],
) -> None:
    ...
