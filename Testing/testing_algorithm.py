import random

from .models import (
    Competence,
    Levels,
    Questions,
    Answers,
    TestingResult,
    TestSettings,
    User
)


class TestAlgorithm:
    def __init__(
        self,
        test_settings: TestSettings,
        user: User
    ):
        self.competence = test_settings.competence_id
        self.questions_count = test_settings.questions_count
        self.test_settings = test_settings
        self.level = test_settings.level_id
        self.user = user
        self.correct_answers = 0

    def get_start_questions(
        self,
    ):
        items = list(Questions.objects.filter(
            competence__id=self.competence.id,
            level__id=self.level.id
        ))

        random_items = random.sample(items, self.questions_count)

        self.testing_result.set_answered_questions(random_items)

        return random_items, self.level.id

    def get_questions(self, next_level, level):
        if next_level:
            level += 1

        items = list(Questions.objects.filter(
            competence__id=self.competence.id,
            level__id=level
        ))

        random_items = random.sample(items, self.questions_count)

        self.testing_result.set_answered_questions(random_items)

        return random_items, level

    def calculate_statistic(
        self,
        answers_ids: list[int]
    ):
        answers = Answers.objects.filter(
            id__in=answers_ids
        )
        self.testing_result.all_questions = answers.count()
        for answer in answers:
            if not answer.is_correct:
                self.testing_result.wrong_questions += 1

        self.correct_answers = self.testing_result.all_questions - self.testing_result.wrong_questions

    def is_next_level(self):
        return self.correct_answers >= self.test_settings.next_level_score

    def get_statistics(self):
        return self.testing_result

    @property
    def testing_result(self):
        user = User.objects.get(
            id=self.user.id
        )
        testing_result, _ = TestingResult.objects.get_or_create(
            user_id=user
        )
        return testing_result
