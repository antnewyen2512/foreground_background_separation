#Set up for a training model before separate step
class Model:
    def __init__(self, name, alpha, beta, height, width, data):
        self.name = name
        self.alpha = alpha
        self.beta = beta
        self.height = height
        self.width = width
        self.data = data