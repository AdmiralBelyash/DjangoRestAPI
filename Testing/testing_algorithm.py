import random

from .models import (
    Competence,
    Levels, 
    Questions, 
    Answers, 
    TestingResult, 
    TestSettings
)

class TestAlgorithm:
    def __init__(
        self,
        test_settings: TestSettings,
    ):
        self.competence = test_settings.competence
        self.questions_count = test_settings.questions_count
        self.user_id = test_settings.user.id
        self.test_settings = test_settings
        self.correct_answers = 0

    def get_questions(
        self,
        level: Levels,
    ):
        items = list(Questions.objects.filter(
            competence=self.competence,
            level=level
        ))

        random_items = random.sample(items, self.questions_count)

        self.testing_result.set_answered_questions(random_items)

        return random_items


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
        return self.correct_answers >= self.test_settings.answers_pass_value

    def get_statistics(self):
        return self.testing_result

    @property
    def testing_result(self):
        return TestingResult.objects.get(
            user_id__id=self.user_id
        )
