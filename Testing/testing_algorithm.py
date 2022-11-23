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

        return random_items, self.level.id

    def get_questions(self, next_level, level=None):
        print(level, 'start')
        if not level:
            level = self.level.id

        if next_level:
            level += 1
        print(level, 'after')

        items = list(Questions.objects.filter(
            competence__id=self.competence.id,
            level__id=level
        ))

        print(items)

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
            competence_id=self.competence
        )

        answers = Answers.objects.filter(
            id__in=answers_ids
        )
        print(answers.count())
        testing_result.all_questions = answers.count()
        print(testing_result.all_questions, 'ALL')
        for answer in answers:
            if not answer.is_correct:
                testing_result.wrong_questions += 1
        print(testing_result.wrong_questions, 'WRONG')

        self.correct_answers = testing_result.all_questions - testing_result.wrong_questions
        print(self.correct_answers, 'CORRECT')
        return self.correct_answers >= self.test_settings.next_level_score

    def get_statistics(self):
        return self.testing_result()

    def testing_result(self):
        user = User.objects.get(
            id=self.user.id
        )
        testing_result, _ = TestingResult.objects.get_or_create(
            user_id=user
        )
        return testing_result
