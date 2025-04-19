from starlette_admin.contrib.sqla import Admin

from app.database import engine
from app.models import User
from app.admin.views import UserView


admin = Admin(
    engine,
    title="Bilimdon Admin"
)


admin.add_view(UserView(User, icon="fa fa-user"))