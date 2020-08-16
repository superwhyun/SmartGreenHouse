import RPi.GPIO as GPIO 

import time #sleep함수를쓰기위해 



GPIO.setmode(GPIO.BCM)

GPIO.setup(18,GPIO.OUT) #gpio18번 셋업 ->릴레이모듈

GPIO.setup(21,GPIO.OUT) #gpio21번 셋업 ->LED

print("setup") 

time.sleep(2) #2초 쉬기

for i in range(1,100):

	GPIO.output(18,True)

	print("true")

	time.sleep(2)



	GPIO.output(18,False)

	print("false")

	time.sleep(2)



GPIO.cleanup() 

print("cleanup")

time.sleep(2)


