import logging

from app import logging as app_logging
from app.settings import Settings

settings = Settings()  # type: ignore[reportCallIssue]
app_logging.configure_logging(settings.log_level)

logger = logging.getLogger(__name__)


logger.info("App is starting")

if settings.framework == "flask":
    logger.info("Using Flask framework")
    from app.presentation.flask.app_factory import app_factory
else:
    logger.info("Using FastAPI framework")
    from app.presentation.fastapi.app_factory import app_factory

app = app_factory()
