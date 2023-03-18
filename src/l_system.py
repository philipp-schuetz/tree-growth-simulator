import random
from modules.config import config
import turtle

# rules = {
#     'A': 'B-A-B',
#     'B': 'A+B+A'
# }
# base = 'A'
# angle = 60

# turtle.color('blue')
# turtle.speed(0)

# for i in range(0,6): 
#     # apply rules to string
#     new = ''
#     for letter in base:
#         if letter in rules:
#             new += rules[letter]
#         else:
#             new += letter
#     base = new
    
#     for letter in base:
#         if letter == 'A':
#             turtle.forward(4)
#         elif letter == 'B':
#             turtle.forward(4)
#         elif letter == '+':
#             turtle.left(angle)
#         elif letter == '-':
#             turtle.right(angle)
# turtle.done()

# random.choice('list')

def apply_rules(sentence):
    # get rules from config, only once at the top of the file, to reduce file reads

    x ={
        'F': 'FRF',
        'R': 'RFR'
    }
    config.create_file()

    # get and sort rules
    rules = config.get_rules()
    rules_dict = {}
    for rule in rules:
        if rule['letter'] not in rules_dict:
            rules_dict['letter'] = []
        rules_dict[rule['letter']].append(rule['new_letters'])
    
    print(rules_dict)

    new = ''
    for letter in sentence:
        if letter in rules:
            new += rules[letter]
        else:
            new += letter
    base = new

apply_rules('F')

def getindex(coords: tuple[int, int, int], array) -> tuple[int, int, int]:
    """conversion from x(plain),y(height),z(room) coordinates starting, at 0,0,0, to array indexes of 3d array"""
    for i in coords:
        if i >= len(array):
            raise IndexError('coordinates out of bounds')
    return (coords[2], len(array)-(coords[1]+1), coords[0])