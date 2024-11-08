import logging

from db.queries import CREATE_TABLE_EVENTS, INSERT_EVENT
from db.utils import DatabaseSession


logger = logging.getLogger(__name__)


def create_tables(session: DatabaseSession):
    with session.connect() as cursor:
        cursor.execute(CREATE_TABLE_EVENTS)
    logger.info("Created tables")


def add_event(session: DatabaseSession, name: str, link: str):
    with session.connect() as cursor:
        cursor.execute(
            INSERT_EVENT,
            (name, link)
        )
    logger.debug("Added event %s with link %s", name, link)


def get_events(session: DatabaseSession):
    with session.connect() as cursor:
        cursor.execute("SELECT * FROM events")
        return cursor.fetchall()


def delete_event(session: DatabaseSession, event_id: int):
    with session.connect() as cursor:
        cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    logger.debug("Deleted event with id %i", event_id)
