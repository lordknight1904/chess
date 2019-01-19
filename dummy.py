from functools import reduce
product = reduce((lambda x, y: x + y if y % 3 == 0 or y % 5 == 0 else x), range(1000))
# product = reduce((lambda x, y: print(x, y)), range(10))

# product = reduce((lambda x, y: print(x*y, y)), [1, 2, 3, 4])

print(product)
