from .codeword import Codeword
import math

class Codebook(object):
    #Set up alpha and beta
    def __init__(self, alpha, beta):
        self.codewords = []
        self.alpha = alpha
        self.beta = beta
 
    #A process of pixel to either add or create a new codeword
    def process_pixel(self, pixel, t): #pixel is defined as rgb values as list, t is defined as current frame number)
        for cw in self.codewords:
            if self.is_match(cw, pixel):
                self.add_pixel_to_cw(cw, pixel, t)
                return                  #if pixel matches codeword, then adds pixel to codeword
        self.codewords.append(self.new_codeword(pixel, t)) #else, create a new codeword and append it to the N.codewords
  
    #Matching codeword
    def is_match(self, cw, pixel): #cw is defined as codeword and new pixel rgb values being checked
        r = pow(int(pixel[0]), 2) 
        g = pow(int(pixel[1]), 2)
        b = pow(int(pixel[2]), 2)
        brightness = math.sqrt(r + g + b)
        mini = int(cw.min_brightness() * self.alpha)
        maxi = int(cw.max_brightness() * self.beta)
        if mini <= brightness <= maxi:
            return True     #if pixel matches the codeword
        else:
            return False

    #Adding pixel to codeword
    def add_pixel_to_cw(self, cw, pixel, t):
        r = int(pixel[0])
        g = int(pixel[1])
        b = int(pixel[2])
        brightness = math.sqrt(pow(r, 2) + pow(g, 2) + pow(b, 2))
        cw.red(self.calc_new_color(curr=cw.red(), new=r, frequency=cw.frequency()))
        cw.green(self.calc_new_color(curr=cw.green(), new=g, frequency=cw.frequency()))
        cw.blue(self.calc_new_color(curr=cw.blue(), new=b, frequency=cw.frequency()))
        cw.min_brightness(min(brightness, cw.min_brightness()))
        cw.max_brightness(max(brightness, cw.max_brightness()))
        cw.frequency(cw.frequency() + 1)
        cw.lam(max(cw.lam(), t - cw.last_access()))
        cw.last_access(t)

    #Calculate new color
    def calc_new_color(self, curr, new, frequency): #current color, new color, and frequency of the relevant codeword
        num = (frequency * curr) + new
        den = frequency + 1
        return num / den        #the new adjusted color value (0-255)


    #Create new codeword
    def new_codeword(self, pixel, t):
        r = int(pixel[0])
        g = int(pixel[1])
        b = int(pixel[2])
        brightness = math.sqrt(pow(r, 2) + pow(g, 2) + pow(b, 2))
        cw = Codeword()
        cw.red(r)
        cw.green(g)
        cw.blue(b)
        cw.max_brightness(brightness)
        cw.min_brightness(brightness)
        cw.frequency(1)
        cw.lam(t-1)
        cw.first_access(t)
        cw.last_access(t)
        return cw           

    #To check if pixel matches an existing codeword
    def bgd(self, pixel):
        for cw in self.codewords:
            if self.is_match(cw, pixel):
                return True
        return False

    #A list of the string representations of all codewords contained in N.data
    def get_cw_as_list(self):
        li = [x.__repr__() for x in self.codewords]
        return li
