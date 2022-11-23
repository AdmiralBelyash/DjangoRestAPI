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
        self.wrong_answers = 0

    def get_start_questions(
        self,
    ):
        self.clear_testing_result()

        items = list(Questions.objects.filter(
            competence__id=self.competence.id,
            level__id=self.level.id
        ))

        random_items = random.sample(items, self.questions_count)

        return random_items, self.level.id

    def get_questions(self, next_level, level=None):
        if not level:
            level = self.level.id

        if level == 7 or level == 1:
            return self.get_statistics()

        if self.testing_result.all_questions >= (
            Levels.objects.all().count() * self.test_settings.questions_count
        ):
            return self.get_statistics()

        if next_level:
            level += 1

        if not next_level:
            level -= 1

        items = list(Questions.objects.filter(
            competence__id=self.competence.id,
            level__id=level
        ))

        random_items = random.sample(items, self.questions_count)

        return random_items, level

    def calculate_statistic(
        self,
        answers_ids: list[int]
    ):
        user = User.objects.get(
            id=self.user.id
        )
        testing_result, _ = TestingResult.objects.get_or_create(
            user_id=user,
            test_id=self.test_settings.id,
            competence_id=self.competence.id
        )

        answers = Answers.objects.filter(
            id__in=answers_ids
        )
        wrong_answers = 0
        answers_count = answers.count()
        for answer in answers:
            if not answer.is_correct:
                wrong_answers += 1

        self.correct_answers = answers_count - wrong_answers

        testing_result.all_questions += answers_count
        testing_result.wrong_questions = wrong_answers

        return self.correct_answers >= self.test_settings.next_level_score

    def get_statistics(self):
        return self.testing_result

    @property
    def testing_result(self):
        user = User.objects.get(
            id=self.user.id
        )
        testing_result, _ = TestingResult.objects.get_or_create(
            user_id=user,
            competence_id=self.competence.id,
            test_id=self.test_settings.id
        )
        return testing_result

    def clear_testing_result(self):
        self.testing_result.delete()
