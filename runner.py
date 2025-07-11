import logging
import random
import time

from config import DELAY_RANGE, MIN_LEN, MAX_LEN
from fetcher import fetch_and_extract
from progress import init_progress
from progress import load_progress, save_progress
from utils import brute_code_at, total_combinations, load_dictionary

logger = logging.getLogger(__name__)


def process_codes(codes, stage, length=0, start_index=0):
    retry = []
    for idx, code in enumerate(codes, start=start_index):
        success, failed_code = fetch_and_extract(code)

        progress = load_progress()
        progress['stage'] = stage
        if stage == 'dict':
            progress['dict_index'] = idx
        else:
            progress['brute_len'] = length
            progress['brute_index'] = idx
        save_progress(progress)

        if failed_code:
            retry.append(failed_code)

        time.sleep(random.uniform(*DELAY_RANGE))

    return retry


def run():
    init_progress()
    progress = load_progress()

    if progress['stage'] == 'dict':
        dict_codes = load_dictionary()
        retry = process_codes(dict_codes[progress['dict_index']:], 'dict', start_index=progress['dict_index'])
        while retry:
            retry = process_codes(retry, 'dict')
        progress.update({'stage': 'brute', 'brute_len': MIN_LEN, 'brute_index': 0})
        save_progress(progress)

    for length in range(progress['brute_len'], MAX_LEN + 1):
        total = total_combinations(length)
        start = progress['brute_index'] if length == progress['brute_len'] else 0
        codes = (brute_code_at(i, length) for i in range(start, total))
        retry = process_codes(codes, 'brute', length, start)

        while retry:
            retry = process_codes(retry, 'brute', length)

        progress = load_progress()
        progress.update({'brute_len': length + 1, 'brute_index': 0})
        save_progress(progress)

    logger.info('All done.')
