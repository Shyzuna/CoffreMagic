import adafruit_mcp3xxx.mcp3008 as MCP
import board

# Redis
REDIS_HOST = '192.168.1.15'
REDIS_PORT = '6379'
REDIS_PWD = ''

# Toys
MOVING_TOYS_VALUES = {
    'POMPIER': (18000, 22000),
    'PATATE': (38000, 42000)
}

MOVING_TOYS_MAPPING = {
    'POMPIER': 0,
    'PATATE': 1
}

FIXED_TOYS_PIN = {
    'POKEBALL': board.D13,
    'LIGHT': board.D19
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
