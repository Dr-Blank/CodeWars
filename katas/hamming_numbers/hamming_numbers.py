"""calculating the nth hamming number"""

import math
from typing import List, Union

hamming_numbers: List[Union[int, float]] = [1]


def generate_hamming_numbers(n: int = 5_000, bases: List[int] = [2, 3, 5]):
    pointers = {base: 0 for base in bases}
    for _ in range(1, n):
        current_minimum = math.inf
        current_minimum_bases = []
        for base, pointer in pointers.items():
            next_number = hamming_numbers[pointer] * base
            if next_number < current_minimum:
                current_minimum = next_number
                current_minimum_bases = [base]
                continue
            if next_number == current_minimum:
                current_minimum_bases.append(base)

        hamming_numbers.append(current_minimum)
        for base in current_minimum_bases:
            pointers[base] += 1


generate_hamming_numbers()


def hamming(n: int):
    return hamming_numbers[n - 1]


def main():
    for i in range(10):
        print(hamming(i))


if __name__ == "__main__":
    main()
