from starlette_admin.contrib.sqla import ModelView

from app.models import User
from app.admin.settings import admin


class UserView(ModelView):
    fields = ["id", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser"]