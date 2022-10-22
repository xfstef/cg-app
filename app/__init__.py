from os import getenv

from dotenv import load_dotenv

from app.core.config import Settings

load_dotenv(getenv("ENV_FILE"))

settings = Settings()

from app.users.models import User   # noqa
from app.posts.models import PublicPost # noqa
from app.subscriptions.models import Subscription   # noqa