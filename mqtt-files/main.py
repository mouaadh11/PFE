# main.py
import time
import sensor as sn
import connection
from utime import ticks_diff, ticks_us
from machine import sleep, SoftI2C, Pin, Timer
import broker

mqttc = broker.setUp()
broker.connect(mqttc)

led = Pin(12, Pin.OUT)

MAX_HISTORY = 32
history = []
beats_history = []
beat = False
beats = 0
t_start_beat = ticks_us()  # Starting time of the acquisition   

def display_bpm(t):
    global beats        
    print('BPM: ', beats)

#timer = Timer(1)
#timer.init(period=2000, mode=Timer.PERIODIC, callback=display_bpm)
def hr(red_reading):
    global beats, history, beats_history, beat, t_start_beat
    value = red_reading
    history.append(value)
    
    # Get the tail, up to MAX_HISTORY length
    history = history[-MAX_HISTORY:]
    minima = 0
    maxima = 0
    threshold_on = 0
    threshold_off = 0

    minima, maxima = min(history), max(history)

    threshold_on = (minima + maxima * 3) // 4   # 3/4
    threshold_off = (minima + maxima) // 2      # 1/2
    
    if value > 1000:
        if not beat and value > threshold_on:
            beat = True                    
            led.on()
            t_us = ticks_diff(ticks_us(), t_start_beat)
            t_s = t_us/1000000
            f = 1/t_s
            bpm = f * 60
            if bpm < 500:
                t_start_beat = ticks_us()
                beats_history.append(bpm)                    
                beats_history = beats_history[-MAX_HISTORY:] 
                beats = round(sum(beats_history)/len(beats_history) ,2)                    
        if beat and value< threshold_off:
            beat = False
            led.off()
        
    else:
        led.off()
        print('No finger')
    return beats

def main():
    sensor, default_value = sn.setUp()

    # Select whether to compute the acquisition frequency or not
    compute_frequency = True
    samples_n = 0  # Number of samples that have been collected
    t_start = ticks_us()  # Starting time of the acquisition
    while True:
            ir_reading, red_reading = sn.get_data(sensor, default_value)
            hr(red_reading)
            current_time = str(time.localtime()[3] +1) + ":" + str(time.localtime()[4]) + ":" + str(time.localtime()[5])
            try:
                broker.send_data(mqttc ,ir_reading, red_reading, beats, current_time)
            except OSError:
                 print("Error while sending data to server")
            #print (f"{ir_reading},{red_reading},{beats},{current_time})")

            # Compute the real frequency at which we receive data
            if compute_frequency:
                if ticks_diff(ticks_us(), t_start) >= 999999:
                    f_HZ = samples_n
                    samples_n = 0
                    print("acquisition frequency = ", f_HZ)
                    t_start = ticks_us()
                else:
                    samples_n = samples_n + 1

if __name__ == '__main__':
    main()