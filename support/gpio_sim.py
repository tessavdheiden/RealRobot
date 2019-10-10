class Motor:
    def __init__(self, pin1, pin2):
        self.pin1 = pin1
        self.pin2 = pin2

    def forward(self, val):
        print(val)
    def backward(self, val):
        print(val)
    def stop(self):
        pass