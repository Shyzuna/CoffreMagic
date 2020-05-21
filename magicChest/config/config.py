import adafruit_mcp3xxx.mcp3008 as MCP
import board

# Redis
REDIS_HOST = '127.0.0.1'
REDIS_PORT = '6379'
REDIS_PWD = ''

# Toys
MOVING_TOYS_VALUES = {
    'pompier': (53000, 57000),
    'patate': (38000, 42000)
}

MOVING_TOYS_MAPPING = {
    'pompier': 0,
    'patate': 1
}

FIXED_TOYS_PIN = {
    'pokeball': board.D13,
    'light': board.D19
}

CHEST_PIN = board.D26

# Spots

SPOTS_MAPPING = {
    MCP.P0: 0,
    MCP.P1: 1,
    MCP.P2: 2,
    MCP.P3: 3,
    MCP.P4: 4,
    MCP.P5: 5,
    MCP.P6: 6
}

# MISC

# Smth better ?
ADC_THRESHOLD = 15000
