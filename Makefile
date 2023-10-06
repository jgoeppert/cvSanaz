num=1

bew: 
	dos2unix serial_wrapper.py
	./serial_wrapper.py -s ${num}

5: 
	dos2unix serial_wrapper.py
	./serial_wrapper.py -s 5

10: 
	dos2unix serial_wrapper.py
	./serial_wrapper.py -s 10

20:	
	dos2unix serial_wrapper.py
	./serial_wrapper.py -s 20
