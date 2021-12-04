#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path
from random import choice
from re import split
from string import punctuation

FILE = Path(__file__).resolve().parent / 'text.txt'


class AutoText():
    def __init__(self, file: Path, n: int, split_reg=r'\b'):
        self.chain = defaultdict(set)
        self.buf = []
        self.n = n

        with file.open() as f:
            for line in f:
                if line.strip() == '':
                    continue

                line = line.replace('\n', ' ')

                words = split(split_reg, line)

                # remove empty "words"
                words = list(filter(len, words))
                self.consume(words)

    def consume(self, words):
        self.buf.extend(words)
        buf_len = len(self.buf)

        if buf_len >= self.n:
            for i in range(buf_len - self.n):
                *cond, state = self.buf[i:i + self.n + 1]
                self.chain[tuple(cond)].add(state)

            # leave last n - 1 "words" for next iteration
            self.buf = self.buf[-self.n + 1:]

    def generate(self, max_count):
        self.last_state = self.random_state()
        start = list(self.last_state)
        autotext = list(self.gen(max_count))

        return ''.join(start + autotext)

    def gen(self, max_count):
        for _ in range(max_count):
            state = list(self.chain[self.last_state])
            if state:
                word = choice(state)
                yield word
                self.last_state = self.last_state[1:] + (word, )

    def random_state(self):
        conditions = self.chain.keys()
        return choice(list(filter(self.is_upper_word, conditions)))

    @staticmethod
    def is_upper_word(s):
        w = s[0].strip()
        return w and w[0] not in punctuation and w[0] == w[0].upper()


def main():
    gen = AutoText(FILE, 4)
    print(gen.generate(250))


if __name__ == '__main__':
    main()
