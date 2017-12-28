import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# the pins i want to use
SPI0_MOSI = 19
SPI0_MISO = 21
SPI0_SCLK = 23
SPI0_SC0  = 24


GPIO.setup(SPI0_MOSI , GPIO.OUT)
GPIO.setup(SPI0_MISO , GPIO.OUT)
GPIO.setup(SPI0_SCLK , GPIO.OUT)
GPIO.setup(SPI0_SC0 , GPIO.OUT)

GPIO.output(SPI0_MOSI, GPIO.LOW)
GPIO.output(SPI0_MISO, GPIO.LOW)
GPIO.output(SPI0_SCLK, GPIO.LOW)
GPIO.output(SPI0_SC0, GPIO.LOW)


while True:
  GPIO.output(SPI0_MOSI, GPIO.HIGH)
  GPIO.output(SPI0_MISO, GPIO.HIGH)
  GPIO.output(SPI0_SCLK, GPIO.HIGH)
  GPIO.output(SPI0_SC0, GPIO.HIGH)
  print("high")


  time.sleep(1)

  GPIO.output(SPI0_MOSI, GPIO.LOW)
  GPIO.output(SPI0_MISO, GPIO.LOW)
  GPIO.output(SPI0_SCLK, GPIO.LOW)
  GPIO.output(SPI0_SC0, GPIO.LOW)
  print("Low")

  time.sleep(.05) 
 

