#!/usr/bin/env python3
from collections import defaultdict
from pathlib import Path
from random import choice
from re import split

FILE = Path(__file__).resolve().parent / 'text.txt'


class AutoText():
    def __init__(self, file: Path, n: int, split_reg=r'\b'):
        self.chain = defaultdict(set)

        with file.open() as f:
            for line in f:
                if not line.strip():
                    continue
                line = line.replace('\n', ' ')
                parts = split(split_reg, line)[1:-1]
                for i in range(len(parts) - n):
                    *cond, state = parts[i:i + n + 1]
                    self.chain[tuple(cond)].add(state)

    def generate(self, max_count):
        self.last_state = self.random_state()

        text = list(self.last_state)

        for word in self.gen(max_count):
            text.append(word)

        return ''.join(text)

    def gen(self, max_count):
        for _ in range(max_count):
            state = list(self.chain[self.last_state])
            if state:
                word = choice(state)
                yield word
                self.last_state = self.last_state[1:] + (word, )

    def random_state(self):
        return choice(list(self.chain.keys()))


def main():
    gen = AutoText(FILE, 4)
    print(gen.generate(250))


if __name__ == '__main__':
    main()
