from starlette_admin.contrib.sqla import ModelView


class UserView(ModelView):
    fields = ["id", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser"]


class GameView(ModelView):
    fields = ["id", "title", "description", "start_time", "end_time", "topic_id", "score"]


class QuestionView(ModelView):
    fields = ["id", "title", "description", "topic_id"]


class ParticipationView(ModelView):
    fields = ["id", "user_id", "game_id", "start_time", "end_time", "gained_score"]


class SubmissionView(ModelView):
    fields = ["id", "user_id", "game_id", "question_id", "option_id", "is_correct"]


class OptionView(ModelView):
    fields = ["id", "question_id", "title", "is_correct"]


class TopicView(ModelView):
    fields = ["id", "name"]