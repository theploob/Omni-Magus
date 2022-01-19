from mageengine import MageEngine
from threading import Thread
from time import sleep


def mage_engine_processor():
	me = MageEngine()
	print('starting mage engine')
	try:
		while True:
			sleep(0.1)
			me.tick_update()
			time_passed = round(me.time_passed, 1)
			print(time_passed)
	finally:
		print('ended engine')



thread1 = Thread(target=mage_engine_processor)

thread1.start()
sleep(10)
thread1.raise_exception()
