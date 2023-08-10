import time
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711


# 1. Kalibrasi beban jika diperlukan


try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    # Create an object hx which represents your real hx711 chip
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    hx = HX711(dout_pin=18, pd_sck_pin=17)
    # measure tare and save the value as offset for current channel
    # and gain selected. That means channel A and gain 128
    err = hx.zero()
    # check if successful
    if err:
        raise ValueError('Tare is unsuccessful.')

    reading = hx.get_raw_data_mean()
    if reading:  # always check if you get correct value or only False
        # now the value is close to 0
        print('Data subtracted by offset but still not converted to units:',
              reading)
    else:
        print('invalid data', reading)

    # In order to calculate the conversion ratio to some units, in my case I want grams,
    # you must have known weight.
    input('Put known weight on the scale and then press Enter')
    reading = hx.get_data_mean()
    if reading:
        print('Mean value from HX711 subtracted by offset:', reading)
        known_weight_grams = input(
            'Write how many grams it was and press Enter: ')
        try:
            value = float(known_weight_grams)
            print(value, 'grams')
        except ValueError:
            print('Expected integer or float and I have got:',
                  known_weight_grams)

        # set scale ratio for particular channel and gain which is
        # used to calculate the conversion to units. Required argument is only
        # scale ratio. Without arguments 'channel' and 'gain_A' it sets
        # the ratio for current channel and gain.
        ratio = reading / value  # calculate the ratio for channel A and gain 128
        hx.set_scale_ratio(ratio)  # set ratio for current channel
        print('Ratio is set.')
    else:
        raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)

    # Read data several times and return mean value
    # subtracted by offset and converted by scale ratio to
    # desired units. In my case in grams.
    print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
    input('Press Enter to begin reading')
    weight = 2000 # 2. Atur beban awal
    print('Current weight on the scale in grams is: ')
    while True:
        while True: 
             current_weight = 2000 # hasil disini dibaca menggunakan fungsi dari membaca beban  
             delta_weight = current_weight - weight # 4. Cek apakah beban saat ini selisih 200 gram dari beban sebelumnya
             print(hx.get_weight_mean(20), 'g')
             if delta_weight < 200: # jika selisih air kurang dari 200 maka beri notifikasi untuk minum
                print("Saatnya minum 200 ml air!") # jika selisih air sudah melebihi atau sama dengan 200 ml maka beri notifikasi yg bagus
             else:
                print("Bagus!! Anda sudah minum 200 ml dalam 2 jam ini, Lanjutkan!!")
                # 5. Update beban ke beban terakhir untuk dibandingkan 2 jam berikutnya
                weight = current_weight
                # 6. Jeda 2 jam menggunakan sleep dalam second
                time.sleep(60)
 
except (KeyboardInterrupt, SystemExit):
    print('Selesai')


finally:
    GPIO.cleanup()

