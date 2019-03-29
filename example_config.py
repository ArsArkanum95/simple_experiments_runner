

def sample_function(a, b, c):
    return a + b * c

RUN_1 = {
    'function': sample_function,
    'default_values': {
        'a': 1, 'b': 2, 'c': 3
    },
    'values': {
        'a': [2, 3, 4],
        'b': [3, 4, 5],
        'c': [4, 5, 6]
    },
    'run': {
        'individual_search': {
            'args': ['a'],
            'grid_search': ['b', 'c']
        },
        'grid_search': ['a', 'b'],
        'individual_search': ['c']
    }
}