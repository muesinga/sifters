# config.py

TITLE = 'sixty'
OUTPUT_DIR = f'sifters/{TITLE}/mid/'

# MIDI constants
TICKS_PER_QUARTER_NOTE = 480

# Default velocity profile
DEFAULT_VELOCITY_PROFILE = {
    'gap': 64,
    'primary': 127,
    'secondary': 64,
    'overlap': 1
}

# Note duration multipliers
DURATION_MULTIPLIER_KEY = {
    'Whole Note': 4,
    'Half Note': 2,
    'Quarter Note': 1,
    'Eighth Note': 0.5,
    'Sixteenth Note': 0.25
}

# Mapping from duration names to MIDI time signature denominators
DURATION_TO_DENOMINATOR = {
    'Whole Note': 1,
    'Half Note': 2,
    'Quarter Note': 4,
    'Eighth Note': 8,
    'Sixteenth Note': 16
}

# List of instrument config dictionaries
INSTRUMENT_CONFIGS = [
    {
        'sieve': '(3@0|3@2)&(4@1|4@3)&(5@2|5@3)',
        'accent_dict': {
            'primary': '(5@2)',
            'secondary': '(5@3)',
        },
        'duration': 'Sixteenth Note',
        'note': 36,
    },
    {
        'sieve': '(10@0|12@0|15@0)',
        'accent_dict': {
            'primary': '(10@0)',
            'secondary': '(12@0)',
        },
        'duration': 'Sixteenth Note',
        'note': 37,
    },
    {
        'sieve': '(3@1|3@2)&(4@0|4@3)',
        'accent_dict': {
            'primary': '(3@2)',
            'secondary': '(4@3)',
        },
        'duration': 'Sixteenth Note',
        'note': 38,
    },
    {
        'sieve': '(4@2|4@3)&(5@1|5@4)&(6@0|6@5)',
        'accent_dict': {
            'primary': '(5@4)',
            'secondary': '(6@5)'
        },
        'duration': 'Eighth Note',
        'note': 39,
    },
    {
        'sieve': '(4@0|4@1)&(5@2|5@3)&(6@4|6@5)',
        'accent_dict': {
            'primary': '(5@4)',
            'secondary': '(6@5)'
        },
        'duration': 'Eighth Note',
        'note': 40,
    },
    {
        'sieve': '4@1&5@3&6|5',
        'accent_dict': {
            'primary': '(5@4)',
            'secondary': '(6@5)'
        },
        'duration': 'Eighth Note',
        'note': 41,
    },
    {
        'sieve': '4@1&5@3&6@5',
        'accent_dict': {
            'primary': '(5@4)',
            'secondary': '(6@5)'
        },
        'duration': 'Eighth Note',
        'note': 42,
    },
]