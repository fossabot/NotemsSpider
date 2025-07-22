from db import get_read_session, get_write_session
from db_model import RetryQueue


def init_retry():
    with get_write_session() as session:
        if session.query(RetryQueue).count() == 0:
            # Placeholder for any initialization if needed
            pass


def load_retry():
    with get_read_session() as session:
        return session.query(RetryQueue).all()


def save_retry(code, retries=0):
    with get_write_session() as session:
        if not session.query(RetryQueue).filter_by(code=code).first():
            session.add(RetryQueue(code=code, retries=retries))


def increment_retry(code):
    with get_write_session() as session:
        retry_item = session.query(RetryQueue).filter_by(code=code).first()
        if retry_item:
            retry_item.retries += 1
            return retry_item.retries
        else:
            session.add(RetryQueue(code=code, retries=1))
            return 1


def delete_retry(code):
    with get_write_session() as session:
        retry = session.query(RetryQueue).filter_by(code=code).first()
        if retry:
            session.delete(retry)
