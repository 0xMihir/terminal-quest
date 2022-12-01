pairs = {
    'r': 'red',
    'g': 'green',
    'G': 'light-green',
    'b': 'blue',
    'y': 'yellow',
    'o': 208,
    'w': 'white',
    'l': 147,
    'c': 'cyan',
    'p': 177,
    'P': 212,
    'B': 'light-blue',
}
COLOURS = {
    "black": 0,
    "red": 1,
    "green": 2,
    "yellow": 3,
    "blue": 4,
    "magenta": 5,
    "cyan": 6,
    "light-gray": 7,
    "dark-gray": 8,
    "light-red": 9,
    "light-green": 10,
    "light-yellow": 11,
    "light-blue": 12,
    "light-magenta": 13,
    "light-cyan": 14,
    "white": 15,
}

final = {}
for (key,val) in pairs.items():
    if (val in COLOURS.keys()):
        final[key] = COLOURS[val]
    else: 
        final[key] = val

print(final)