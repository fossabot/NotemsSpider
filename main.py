import logging
import multiprocessing
import os
import signal
import sys

from alembic.config import Config

from alembic import command
from runner import run

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] (%(name)s): %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

interrupted = False


def handle_sigint(signum, frame):
    global interrupted
    if not interrupted:
        interrupted = True
        if worker and worker.is_alive():
            os.kill(worker.pid, signal.SIGINT)
        print("\nReceived interrupt, shutting down...")
    else:
        os._exit(1)


def worker_main():
    try:
        run()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

    signal.signal(signal.SIGINT, handle_sigint)

    worker = multiprocessing.Process(target=worker_main)
    worker.start()

    while worker.is_alive():
        worker.join(timeout=0.5)
