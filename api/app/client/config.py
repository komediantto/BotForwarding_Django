from loguru import logger
from botForward_api.models import Session


def get_or_create_session_string():
    session = Session.objects.first()
    if session is not None:
        logger.warning(session)
        return session
