import re
from functools import lru_cache

from config import DICT_FILE, CHARS


def load_dictionary():
    pat = re.compile(r"^[A-Za-z0-9]+$")
    seen = set()
    codes = []

    with open(DICT_FILE, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if line and line not in seen and pat.match(line):
                seen.add(line)
                codes.append(line)

    return codes


@lru_cache(maxsize=1)
def load_dictionary_cached():
    return load_dictionary()


def total_combinations(length):
    return len(CHARS) ** length


def total_brute_combinations(min_len, max_len):
    return sum(total_combinations(length) for length in range(min_len, max_len + 1))


def brute_code_at(index, length):
    base = len(CHARS)
    chars = []
    for _ in range(length):
        chars.append(CHARS[index % base])
        index //= base
    return "".join(reversed(chars))


def get_code_index(code, dictionary, min_len):
    try:
        return "dict", 0, dictionary.index(code)
    except ValueError:
        length = len(code)
        if length < min_len:
            return None
        base = len(CHARS)
        char_map = {char: i for i, char in enumerate(CHARS)}
        index = 0
        for char in code:
            index = index * base + char_map[char]

        return "brute", length, index
