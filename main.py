import logging

from db import engine
from db_model import Base
from runner import run

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] (%(name)s): %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    try:
        Base.metadata.create_all(engine)
        run()
    except KeyboardInterrupt:
        print('\nOperation interrupted by user')
    except Exception as e:
        print(f'\nAn error occurred: {e}')
