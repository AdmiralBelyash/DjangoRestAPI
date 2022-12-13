import datetime
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

    def get_questions(self, next_level, time, level=None):
        if datetime.datetime.strptime(time, '%H:%M:%S').time() >= self.test_settings.time:
            return self.get_statistics()

        if self.testing_result.question_summary >= (
            Levels.objects.all().count() * self.test_settings.questions_count
        ):
            return self.get_statistics()

        if not level:
            level = self.level.id

        if level == 7:
            self.get_statistics()

        if next_level:
            if level == 6:
                level += 1
            else:
                level += 2
        else:
            if level == 1:
                result = self.get_statistics()
                result.update(level=Levels(0))
                return result
            else:
                level -= 1

        items = list(Questions.objects.filter(
            competence__id=self.competence.id,
            level__id=level
        ))

        random_items = random.sample(items, self.questions_count)

        return random_items, level

    def calculate_statistic(
        self,
        answers_ids: list[int],
        time_spent,
        level,
    ):
        user = User.objects.get(
            id=self.user.id
        )
        testing_result, _ = TestingResult.objects.get_or_create(
            user_id=user,
            test_id=self.test_settings,
            competence_id=self.competence.id,
            time_summary=self.test_settings.time
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

        testing_result.question_summary += answers_count
        testing_result.wrong_questions += wrong_answers
        testing_result.time_spent = time_spent
        testing_result.level = Levels(level)
        testing_result.save()

        return self.correct_answers >= self.test_settings.next_level_score

    def get_statistics(self):
        user = User.objects.get(
            id=self.user.id
        )
        return TestingResult.objects.filter(
            user_id=user,
            competence_id=self.competence.id,
            test_id=self.test_settings
        )

    @property
    def testing_result(self):
        user = User.objects.get(
            id=self.user.id
        )
        testing_result, _ = TestingResult.objects.get_or_create(
            user_id=user,
            competence_id=self.competence.id,
            test_id=self.test_settings,
            time_summary=self.test_settings.time
        )
        return testing_result

    def clear_testing_result(self):
        self.testing_result.delete()
