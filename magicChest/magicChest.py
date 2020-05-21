import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import redis
import time

try:
    from .config import config
except ImportError as e:
    from config import config


if __name__ == '__main__':

    bdd = redis.Redis(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_PWD)

    # create the spi bus
    spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)

    # create the cs (chip select)
    cs = digitalio.DigitalInOut(board.D5)

    # create the mcp object
    mcp = MCP.MCP3008(spi, cs)

    # create analogs inputs channels
    spotsPins = {
        MCP.P0: AnalogIn(mcp, MCP.P0),
        MCP.P1: AnalogIn(mcp, MCP.P1),
        MCP.P2: AnalogIn(mcp, MCP.P2),
        MCP.P3: AnalogIn(mcp, MCP.P3),
        MCP.P4: AnalogIn(mcp, MCP.P4),
        MCP.P5: AnalogIn(mcp, MCP.P5),
        MCP.P6: AnalogIn(mcp, MCP.P6)
    }

    # Value 1 => Close / Linked
    # Value 0 => Open / Unlinked
    chestPin = digitalio.DigitalInOut(config.CHEST_PIN)
    chestPin.direction = digitalio.Direction.INPUT

    pokePin = digitalio.DigitalInOut(config.FIXED_TOYS_PIN['POKEBALL'])
    pokePin.direction = digitalio.Direction.INPUT
    pokePin.pull = digitalio.Pull.UP

    lightPin = digitalio.DigitalInOut(config.FIXED_TOYS_PIN['LIGHT'])
    lightPin.direction = digitalio.Direction.INPUT

    oldChest = chestPin.value


    while True:
        # If the chest is newly closed
        #if chestPin.value != oldChest and chestPin.value == 1:
            # Update Redis values
        #    print('UPDATE redis')
        #oldChest = chestPin.value
        for k,v in spotsPins.items():
            print(str(k) + ' : ' + str(v.value))
        print('Chest : ' + str(chestPin.value))
        print('Pokeball : ' + str(pokePin.value))
        print('Light : ' + str(lightPin.value))
        print('--------------------')
        time.sleep(1)