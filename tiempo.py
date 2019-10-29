import time
millis1 = int(round(time.time() * 1000))

time.sleep(0.2)

millis2 = int(round(time.time() * 1000))

print (millis2 - millis1)
