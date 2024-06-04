import smbus2
import time
from PIL import Image, ImageDraw

class OLED:
    def __init__(self, i2c_bus=1, i2c_address=0x3C):
        self.i2c_address = i2c_address
        self.bus = smbus2.SMBus(i2c_bus)
        self.width = 128
        self.height = 64
        self.pages = self.height // 8
        
        # Initialize display
        self.initialize_display()

    def write_command(self, cmd):
        control = 0x00  # Control byte
        self.bus.write_byte_data(self.i2c_address, control, cmd)

    def initialize_display(self):
        init_sequence = [
            0xAE,  # Display OFF
            0xD5, 0x80,  # Set display clock divide ratio/oscillator frequency
            0xA8, 0x3F,  # Set multiplex ratio
            0xD3, 0x00,  # Set display offset
            0x40,  # Set start line address
            0x8D, 0x14,  # Enable charge pump regulator
            0x20, 0x00,  # Set memory addressing mode to horizontal addressing mode
            0xA1,  # Set segment re-map (A0/A1)
            0xC8,  # Set COM output scan direction (C0/C8)
            0xDA, 0x12,  # Set COM pins hardware configuration
            0x81, 0xCF,  # Set contrast control
            0xD9, 0xF1,  # Set pre-charge period
            0xDB, 0x40,  # Set VCOMH deselect level
            0xA4,  # Entire display ON
            0xA6,  # Set normal display (A6/A7)
            0xAF  # Display ON
        ]
        
        for cmd in init_sequence:
            self.write_command(cmd)

    def clear_display(self):
        for page in range(self.pages):
            self.write_command(0xB0 + page)  # Set page address
            self.write_command(0x00)  # Set lower column start address
            self.write_command(0x10)  # Set higher column start address
            for i in range(self.width):
                self.bus.write_byte_data(self.i2c_address, 0x40, 0x00)

    def display_image(self, image):
        image = image.convert('1')
        imdata = list(image.getdata())
        
        for page in range(self.pages):
            self.write_command(0xB0 + page)
            self.write_command(0x00)
            self.write_command(0x10)
            for x in range(self.width):
                byte = 0
                for bit in range(8):
                    byte |= (imdata[x + (page * 8 + bit) * self.width] & 0x01) << bit
                self.bus.write_byte_data(self.i2c_address, 0x40, byte)

if __name__ == "__main__":
    oled = OLED()
    oled.clear_display()
    
    # Create a blank image for drawing
    image = Image.new('1', (oled.width, oled.height), 0)
    draw = ImageDraw.Draw(image)
    
    # Draw a simple text
    draw.text((0, 0), "P1", fill=1)
    
    # Display image on the OLED
    oled.display_image(image)
