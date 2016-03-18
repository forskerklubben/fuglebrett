import RPi.GPIO as GPIO
 
GPIO.setmode(GPIO.BCM)
DEBUG = 1
 
# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
  if ((adcnum > 7) or (adcnum < 0)):
    return -1
  GPIO.output(cspin, True)
 
  GPIO.output(clockpin, False)  # start clock low
  GPIO.output(cspin, False)     # bring CS low
 
  commandout = adcnum
  commandout |= 0x18  # start bit + single-ended bit
  commandout <<= 3    # we only need to send 5 bits here
  for i in range(5):
    if (commandout & 0x80):
      GPIO.output(mosipin, True)
    else:
      GPIO.output(mosipin, False)
    commandout <<= 1
    GPIO.output(clockpin, True)
    GPIO.output(clockpin, False)

  adcout = 0
  # read in one empty bit, one null bit and 10 ADC bits
  for i in range(12):
    GPIO.output(clockpin, True)
    GPIO.output(clockpin, False)
    adcout <<= 1
    if (GPIO.input(misopin)):
      adcout |= 0x1

  GPIO.output(cspin, True)

  adcout >>= 1       # first bit is 'null' so drop it
  return adcout
 
# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
 
# set up the SPI interface pins
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)
 
sensor1_adc = 0;
sensor2_adc = 1;
sensor3_adc = 2;
sensor4_adc = 3;
sensor5_adc = 4;
sensor6_adc = 5;
sensor7_adc = 6;
sensor8_adc = 7;

while True:
  # read the analog pin
  sensor1 = readadc(sensor1_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  sensor2 = readadc(sensor2_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  sensor3 = readadc(sensor3_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  sensor4 = readadc(sensor4_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  sensor5 = readadc(sensor5_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  sensor6 = readadc(sensor6_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  sensor7 = readadc(sensor7_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)
  sensor8 = readadc(sensor8_adc, SPICLK, SPIMOSI, SPIMISO, SPICS)

  if DEBUG:
    print("sensor1: ", sensor1)
    print("sensor2: ", sensor2)
    print("sensor3: ", sensor3)
    print("sensor4: ", sensor4)
    print("sensor5: ", sensor5)
    print("sensor6: ", sensor6)
    print("sensor7: ", sensor7)
    print("sensor8: ", sensor8)

  # hang out and do nothing for a half second
  time.sleep(0.5)
