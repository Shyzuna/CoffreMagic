import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import sounddevice as sd
import soundfile as sf
from pathlib import Path
import redis
import time

try:
    from .config import config
except ImportError as e:
    from config import config


"""
# Add some error handling (redis)
# Swap redis keys as config maybe
"""

def DisplayValues(spotsPins, chestPin, pokePin, lightPin, positionValue):
    print('--------------------')
    print('Status')
    for k, v in spotsPins.items():
        print(str(k) + ' : ' + str(v.value) + ' ( ' + str(positionValue[k]) + ' )')
    print('Chest : ' + str(chestPin.value))
    print('Pokeball : ' + str(pokePin.value))
    print('Light : ' + str(lightPin.value))
    print('--------------------')

def InitRedis(bdd, spotsPins):
    print('INIT REDIS :\nwidth: {}\nheight: 1\nelments: {}'.format(str(len(spotsPins)), str(config.MOVING_TOYS_MAPPING)))
    RedisHmset(bdd, 'coffreElements', config.MOVING_TOYS_MAPPING)
    RedisHmset(bdd, 'coffreConfig', {'width': len(spotsPins), 'height': 1})

def UpdateRedis(bdd, spotsPins, chestPin, pokePin, lightPin):
    print('UPDATE REDIS')
    i = 0
    positionValue = {}
    for spot, spotVal in spotsPins.items():
        value = 0
        if spotVal.value > config.ADC_THRESHOLD:
            for toy, val in config.MOVING_TOYS_VALUES.items():
                if val[0] <= spotVal.value <= val[1]:
                    value = config.MOVING_TOYS_MAPPING[toy]
                    break
        positionValue[spot] = value
        bdd.lset('coffrePosition', i, value)
        i += 1
    RedisHmset(bdd, 'coffre', {'chest': 1 if chestPin.value else 0, 'pokeball': 1 if pokePin.value else 0, 'light': 1 if lightPin.value else 0})
    return positionValue


def RedisHmset(bdd, key, d):
    for k, v in d.items():
        bdd.hset(key, k, v)


if __name__ == '__main__':

    musicData = sf.read(str(Path.cwd().joinpath('assets').joinpath('music').joinpath('music.wav')))
    currentMusic = None

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

    # Value 0 => Close / Linked
    # Value 1 => Open / Unlinked
    chestPin = digitalio.DigitalInOut(config.CHEST_PIN)
    chestPin.direction = digitalio.Direction.INPUT
    chestPin.pull = digitalio.Pull.UP

    pokePin = digitalio.DigitalInOut(config.FIXED_TOYS_PIN['pokeball'])
    pokePin.direction = digitalio.Direction.INPUT
    pokePin.pull = digitalio.Pull.UP

    lightPin = digitalio.DigitalInOut(config.FIXED_TOYS_PIN['light'])
    lightPin.direction = digitalio.Direction.INPUT
    lightPin.pull = digitalio.Pull.UP

    oldChest = chestPin

    # Send base data / config to redis
    InitRedis(bdd, spotsPins)
    positionValue = UpdateRedis(bdd, spotsPins, chestPin, pokePin, lightPin)
    DisplayValues(spotsPins, chestPin, pokePin, lightPin, positionValue)
    if chestPin.value == 0:
        # Start Music
        sd.play(musicData[0], musicData[1])
        currentMusic = sd.get_stream()

    while True:

        # chest status changed
        if chestPin.value != oldChest:
            # chest is now closed
            if not chestPin.value:
                print('CHEST CLOSED')
                # Update Redis values
                positionValue = UpdateRedis(bdd, spotsPins, chestPin, pokePin, lightPin)
                DisplayValues(spotsPins, chestPin, pokePin, lightPin, positionValue)

                # Start Music
                sd.play(musicData[0], musicData[1])
                currentMusic = sd.get_stream()
            # chest is now open
            else:
                print('CHEST OPENED')
                # Stop Music
                if currentMusic is not None:
                    currentMusic.stop()

        # Music Check loop
        if currentMusic is not None and not currentMusic.active:
            sd.play(musicData[0], musicData[1])
            currentMusic = sd.get_stream()

        oldChest = chestPin.value
        #time.sleep(1)