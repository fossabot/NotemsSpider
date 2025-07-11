import logging

from db import engine
from db_model import Base
from runner import run

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    run()
