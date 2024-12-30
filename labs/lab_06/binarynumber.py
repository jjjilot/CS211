""" Lab 06 BinaryNumbers
    Josh Jilot
"""


class BinaryNumber:

    def __init__(self, bits:list[int]):
        self.bits = bits

    def __str__(self):
        return f'{self.bits}'

    def __or__(self, other):
        new_bits = [0]*len(self.bits)
        for i in range(len(self.bits)):
            if self.bits[i] == 1 or other.bits[i] == 1:
                new_bits[i] = 1
        return new_bits

    def __and__(self, other):
        new_bits = [0]*len(self.bits)
        for i in range(len(self.bits)):
            if self.bits[i] == 1 and other.bits[i] == 1:
                new_bits[i] = 1
        return new_bits

    def left_shift(self):
        self.bits.pop(0)
        self.bits.append(0)

    def right_shift(self):
        self.bits.pop()
        self.bits.insert(0,0)

    def extract(self, start: int, end: int):
        new_bits = BinaryNumber(self.bits)
        for i in range(len(self.bits) -  1 - end):
            new_bits.left_shift()
        for i in range(len(self.bits) - 1 - end + start):
            new_bits.right_shift()
        return new_bits


if __name__ == "__main__":
    # execute and verify

    bn = BinaryNumber([1, 0, 1, 0, 1])
    bn2 = BinaryNumber([1, 1, 1, 0, 0])
    print("1st binary number =", bn)

    print("2nd binary number =", bn2)

    print("AND", bn & bn2)
    print("OR", bn | bn2)

    bn.right_shift()
    print("1st number right-shifted =", bn)

    bn.left_shift()
    print("1st number left-shifted =", bn)

    bn = BinaryNumber([1, 0, 0, 1, 0, 1, 1, 1])
    extracted = bn.extract(2, 4)
    print(extracted)
