from neulog import Device

class CustomDevice(Device):
    def __init__(self, port = "COM5"):
        Device.__init__(self, port)

    def customClose(self):
        self.close()

    def setSampleRate(self, rate):
        self.sampleRate = rate