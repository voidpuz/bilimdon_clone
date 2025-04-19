from starlette_admin.contrib.sqla import ModelView

from app.models import User, Game


class UserView(ModelView):
    fields = ["id", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser", "joined_at"]
    exclude_fields_from_list = ["joined_at"]
    exclude_fields_from_create = ["joined_at"]
    exclude_fields_from_edit = ["joined_at"]
    export_fields = ["id", "email", "first_name", "last_name", "is_active", "joined_at"]
    export_types = ["csv", "excel", "pdf", "print"]


class GameView(ModelView):
    fields = ["id", "title", "description", "start_time", "end_time", "topic", "score"]


class QuestionView(ModelView):
    fields = ["id", "title", "description", "topic"]


class ParticipationView(ModelView):
    fields = ["id", "user", "game", "start_time", "end_time", "gained_score"]
    exclude_fields_from_list = ["start_time", "end_time"]


class SubmissionView(ModelView):
    fields = ["id", "owner", "game", "question", "option", "is_correct"]


class OptionView(ModelView):
    fields = ["id", "question", "title", "is_correct"]


class TopicView(ModelView):
    fields = ["id", "name"]