from neulog2 import Neulog


device = Neulog ("COM5", 9600)
# Determine which sensors are connected
# ( GSR , Heart rate , etc .)
# try catch

try:
    device.scan()
    while True:
        # acquires all sensor data currently available
        data = device.read()
        print(data)

# print the error 
except Exception as e:
    print(e)