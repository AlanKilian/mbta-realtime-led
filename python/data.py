class MapColors:
    RED = 0xFF0000
    GREEN = 0x00FF00
    BLUE = 0x0000FF
    ORANGE = 0xFFA500


BRIGHTNESS_MULTIPLIERS = {
    MapColors.RED: 1,
    MapColors.ORANGE: 0.75,
    MapColors.BLUE: 0.5,
    MapColors.GREEN: 0.5
}

BRIGHTNESS = 0.3
FADE_SIZE = 1
FADE_GRANULARITY = 0.1

SLEEP_TIME = 0.015
PORTS = ['/dev/ttyACM0', '/dev/ttyACM1']

ON_HOUR = 8
OFF_HOUR = 24

API_ROUTE_NAMES = {
    'red_a': 'Red',
}

API_ROUTE_FILTERS = {
    'red_a': lambda t: 'Braintree' in t.name.lower(),
}

ROUTES = {
    'red_a': [
        'Alewife',
        'Davis',
        'Porter',
        'Harvard',
        'Central',
        'Kendall/MIT',
        'Charles/MGH',
        'Park Street',
        'Downtown Crossing',
        'South Station',
        'Broadway',
        'Andrew',
        'JFK/UMass',
        'Savin Hill',
        'Fields Corner',
        'Shawmut',
        'Ashmont',
        'North Quincy',
        'Wollaston',
        'Quincy Center',
        'Quincy Adams',
        'Braintree'
    ]
}

STATION_LOCATIONS = {
    'red_a': [
        ('Alewife', 0)
    ]
}

STRIPS = {
    'redLine': (4, 146)
}

ROUTE_COLORS = {
    'red_a': MapColors.RED,
}

ROUTE_SEGMENTS = {
    'red_a': [
        ('redLine', 97, 145, True),
        ('greenLineB', 60, 60, False),
        ('redLine', 93, 96, True),
        ('orangeLine', 41, 41, False),
        ('redLine', 66, 92, True),
        ('redLine', 0, 22, True)
    ]
}
