from fastaoc import AdventOfCodePuzzle


SNAFU_ALPHABET = '=-012'


def snafu_to_decimal(number: str) -> int:
    result = 0

    decimal = 0
    for i in reversed(number):
        result += (SNAFU_ALPHABET.index(i)-2) * 5 ** decimal
        decimal += 1

    return result


def decimal_to_snafu(number: int) -> str:
    """Decimal to SNAFU converter

    Algorithm:
    1. Evaluate the first literal of the number (literal with highest decimal).
       It can be only literal 1 or 2.
    2. Evaluate tail of the number by simple number cast algorithm.

    """

    decimal = 0
    old_actual = 0
    while True:
        actual = old_actual + (5 ** decimal) * 2
        if actual >= number:
            if (actual - old_actual) // 2 >= number - old_actual:
                res = (1, decimal, (number - old_actual - 1) % 5 ** decimal)
            else:
                res = (2, decimal, (number - old_actual - 1) % 5 ** decimal)
            break
        decimal += 1
        old_actual = actual

    face, decimal, tail_number = res

    current = tail_number
    result = str()

    while current >= 5:
        current_loss = current % 5
        current //= 5
        result += SNAFU_ALPHABET[current_loss]
    else:
        result += SNAFU_ALPHABET[current]

    result += SNAFU_ALPHABET[0] * (decimal - len(result))
    result += str(face)
    return result[::-1]


class Solution(AdventOfCodePuzzle):
    def task_1(self, data):

        """Some task solution

        :input 1:
            1=-0-2
            12111
            2=0=
            21
            2=01
            111
            20012
            112
            1=-1=
            1-12
            12
            1=
            122
        :output 1:
            2=-1=0

        """

        result = 0

        for i in data.strip().split('\n'):
            result += snafu_to_decimal(i)

        return decimal_to_snafu(result)
