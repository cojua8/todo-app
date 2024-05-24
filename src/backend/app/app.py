from app.settings import Settings

settings = Settings()  # type: ignore[reportCallIssue]
if settings.framework == "flask":
    from app.presentation.flask.app_factory import app_factory
else:
    from app.presentation.fastapi.app_factory import app_factory

app = app_factory()
