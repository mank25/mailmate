# Import model modules here so Alembic's autogenerate can see them via Base.metadata.
from app.models.user import User  # noqa: F401
from app.models.mailbox import Mailbox  # noqa: F401
from app.models.email import Email  # noqa: F401
