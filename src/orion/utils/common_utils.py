import random


def random_mobile():
    head = ['186', '135', '136', '182']
    mobile = random.choice(head) + str(random.randint(10000000, 100000000))
    return mobile
