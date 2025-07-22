from contextlib import contextmanager

from readerwriterlock import rwlock
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from config import DB_FILE

rw_lock = rwlock.RWLockFair()

engine = create_engine(
    f"sqlite:///{DB_FILE}", connect_args={"check_same_thread": False}
)
Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def get_read_session():
    with rw_lock.gen_rlock():
        session = Session()
        try:
            yield session
        finally:
            session.close()


@contextmanager
def get_write_session():
    with rw_lock.gen_wlock():
        session = Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
