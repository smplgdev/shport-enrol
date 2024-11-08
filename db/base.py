import os

from db.utils import DatabaseSession


def get_session(db_path: str = None):
    session = DatabaseSession(db_path)

    return session
