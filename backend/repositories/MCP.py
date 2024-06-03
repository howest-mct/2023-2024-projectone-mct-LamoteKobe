import spidev

class MCP:

    def __init__(self, bus=0, device=0) -> None:
        self.__spi = spidev.SpiDev()
        self.__spi.open(bus, device) # Bus SPI0, slave op CE 0 
        self.__spi.max_speed_hz = 10 ** 5 # 100 kHz
    
    def read_channel(self, channel):
        adc = self.__spi.xfer2([1, (8+channel)<<4,0])
        data = ((adc[1]&3)<<8) | adc[2]
        return data

    def closepi(self):
        self.__spi.close()