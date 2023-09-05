from RPi_GPIO_i2c_LCD import lcd
from w1thermsensor import W1ThermSensor


sensor = W1ThermSensor()
i2c_address = 0x27
lcdDsiplay = lcd.HD44780(i2c_address)

def read_temperature():
    try:
        temperature = sensor.get_temperature()
        return temperature
    except Exception as e:
        print("Error reading temperature:", e)
        return None

def lcdDisplay(line1, line2):
    lcdDsiplay.set(line1, 1)
    lcdDsiplay.set(line2, 2)

try:
    while True:
        temperature = read_temperature()
        if temperature is not None:
            line1 = "Temp: {:.2f} C".format(temperature)
            line2 = time.strftime("%Y-%m-%d %H:%M:%S")
            lcdDisplay(line1, line2)
        
        time.sleep(1)  
        
except KeyboardInterrupt:
    lcd.lcd_clear()
    GPIO.cleanup()
    print("Exiting...")
