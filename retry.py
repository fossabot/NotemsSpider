from db import get_session
from db_model import RetryQueue


def init_retry():
    with get_session() as session:
        if not session.query(RetryQueue).first():
            session.commit()


def load_retry():
    with get_session() as session:
        return session.query(RetryQueue).all()


def save_retry(code):
    with get_session() as session:
        if not session.query(RetryQueue).filter_by(code=code).first():
            session.add(RetryQueue(code=code))
            session.commit()


def delete_retry(code):
    with get_session() as session:
        session.query(RetryQueue).filter_by(code=code).delete()
        session.commit()
