# First install spidev:
# Enable SPI (sudo raspi-config)
# $ sudo apt-get update 
# $ sudo apt-get upgrade
# $ sudo apt-get install python-dev
# $ sudo reboot
# $ wget https://github.com/doceme/py-spidev/archive/master.zip 
# $ unzip master.zip
# $ cd py-spidev-master
# $ sudo python setup.py install

from spidev import SpiDev

class MCP3008:
    def __init__(self, bus = 0, device = 0):
        self.bus, self.device = bus, device
        self.spi = SpiDev()
        self.open()
        self.spi.max_speed_hz = 1000000 # 1MHz

    def open(self):
        self.spi.open(self.bus, self.device)
        self.spi.max_speed_hz = 1000000 # 1MHz
    
    def read(self, channel = 0):
        cmd1 = 4 | 2 | (( channel & 4) >> 2)
        cmd2 = (channel & 3) << 6

        adc = self.spi.xfer2([cmd1, cmd2, 0])
        data = ((adc[1] & 15) << 8) + adc[2]
        return data
            
    def close(self):
        self.spi.close()
