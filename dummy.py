axis_y = tuple(range(1, 9))
axis_x = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')

def encode_x(index):
    return axis_x[index]


def decode_x( letter):
    return axis_x.index(letter)


def encode_y(index):
    return axis_y[-index - 1]


def decode_y(number):
    return abs(int(number) - 8)


# from coord to word
def letter_notation( coord):
    return str(encode_x(coord[0])) + str(encode_y(coord[1]))


# from word to array indexes
def number_notation( coord):
    return decode_x(coord[0]), decode_y(coord[1])


print(letter_notation((0, 0)))
print(number_notation("A1"))