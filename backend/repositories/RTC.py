import smbus
import time
from datetime import datetime, timedelta
import socket
import subprocess

class RTC:
    def __init__(self):
        self.bus = smbus.SMBus(1)
        self.RTC_ADDRESS = 0x68
    
    def bcd_to_dec(self, bcd):
        """Convert BCD to decimal"""
        return (bcd & 0x0F) + ((bcd >> 4) * 10)

    def dec_to_bcd(self, dec):
        """Convert decimal to BCD"""
        return (dec // 10 << 4) + (dec % 10)

    def set_time(self, now):
        """Set the time on the RTC module"""
        self.bus.write_i2c_block_data(self.RTC_ADDRESS, 0, [
            self.dec_to_bcd(now.second),
            self.dec_to_bcd(now.minute),
            self.dec_to_bcd(now.hour),
            self.dec_to_bcd(now.isoweekday()),
            self.dec_to_bcd(now.day),
            self.dec_to_bcd(now.month),
            self.dec_to_bcd(now.year - 2000)
        ])

    def read_time(self):
        """Read the time from the RTC module"""
        data = self.bus.read_i2c_block_data(self.RTC_ADDRESS, 0, 7)
        seconds = self.bcd_to_dec(data[0])
        minutes = self.bcd_to_dec(data[1])
        hours = self.bcd_to_dec(data[2])
        day = self.bcd_to_dec(data[3])
        date = self.bcd_to_dec(data[4])
        month = self.bcd_to_dec(data[5])
        year = self.bcd_to_dec(data[6]) + 2000
        return seconds, minutes, hours, day, date, month, year
    
    def update(self):
        """Update RTC time from internet if connection available, else sync Pi time"""
        try:
            # Check internet connectivity by attempting to resolve a well-known domain
            socket.create_connection(("www.google.com", 80))
            # If successful, update RTC time from internet time
            current_time = subprocess.check_output(["date", "+%Y-%m-%d %H:%M:%S"]).decode("utf-8")
            current_datetime = datetime.strptime(current_time.strip(), "%Y-%m-%d %H:%M:%S")
            self.set_time(current_datetime)
        except OSError:
            # If no internet connection, sync Pi time with RTC time
            rtc_time = self.read_time()
            system_time = datetime(rtc_time[6], rtc_time[5], rtc_time[4], rtc_time[2], rtc_time[1], rtc_time[0])
            # Set system time using subprocess to call 'date' command
            subprocess.run(["sudo", "date", "--set", system_time.strftime("%Y-%m-%d %H:%M:%S")])
            