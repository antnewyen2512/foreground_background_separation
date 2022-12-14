import cv2
import json
import datetime
from foreground_background_separation.frame_manager import FrameManager
from foreground_background_separation.codebook import Codebook
from foreground_background_separation.training_model import Model
from foreground_background_separation.codeword import Codeword
#Setting up cb_engine
class CodebookEngine:
    black = [0, 0, 0]
    white = [255, 255, 255]
    data = []
    cw_created = 0
    def __init__(self):
        pass

    #Initalizing frame by getting source video and alpha,beta valuable
    def init_frame_manager(self, source, alpha = 0.4, beta = 1.5):
        if source != '':
            self.fm = FrameManager(source)
        self.mnrl_threshold = self.fm.num_of_frames / 2
        self.alpha = alpha              #between 0.4 and 0.7 by reference
        self.beta = beta                #between 1.1 and 1.5 by reference

    #Initializing codebook with its size
    def init_codebooks(self):
        for y in range(0, self.fm.frame_height):
            temp = []
            for x in range(0, self.fm.frame_width):
                temp.append(Codebook(self.alpha, self.beta))
            self.data.append(temp)
        self.fm.reset()
        print(' ** codebooks initialized with {}, {} size successfully'.format(len(self.data[0]), len(self.data)))

    #Build codebook to process
    def build_codebooks(self):
        t = 1
        while self.fm.get_next_frame():
            for y in range(0, self.fm.frame_height-1):
                for x in range(0, self.fm.frame_width-1):
                    pixel = self.fm.frame[y][x]
                    cb = self.data[y][x]
                    cb.process_pixel(pixel, t)
            t += 1
        self.fm.reset()
        print(' ** codebooks built successfully')

    #Cleaning out lambdas - Section III
    def clean_lambdas(self):
        for y in range(0, self.fm.frame_height-1):
            for x in range(0, self.fm.frame_width-1):
                cb = self.data[y][x]
                for cw in cb.codewords:
                    cw.lam( max( cw.lam(), (self.fm.num_of_frames-cw.first_access()+cw.last_access()-1) ) )
        print(' ** lambdas being cleaned successfully')

    #Temporal filtering step
    def temporal_filtering(self):
        for y in range(0, self.fm.frame_height-1):
            for x in range(0, self.fm.frame_width-1):
                cw_list = self.data[y][x].codewords
                for cw in cw_list:
                    if cw.lam() <= self.mnrl_threshold:
                        cw_list.remove(cw)
        print(' ** temporal filtering completed successfully')

    #Created a train model
    def save_model(self, name):
        data = self.convert_data()
        model = Model(name=name,alpha=self.alpha, beta=self.beta, height=self.fm.frame_height, width=self.fm.frame_width, data=data)
        j_model = json.dumps(model.__dict__)
        with open( '{}.json'.format(name), 'w') as fd:
            fd.write(j_model)
        print(' ** model [{}.json] was created successfully'.format(name))

    #Converting data for matrix of codebooks represented as list of strings
    def convert_data(self):
        a = []
        for y in range(0, self.fm.frame_height-1):
            b = []
            for x in range(0, self.fm.frame_width-1):
                c = []
                cw_list = self.data[y][x].codewords
                for cw in cw_list:
                    c.append(cw.__repr__())
                b.append(c)
            a.append(b)
        return a

    #Loading selected model
    def load_model(self, source):
        with open(source, 'r') as json_file:
            i = json.load(json_file)
            self.alpha = i['alpha']
            self.beta = i['beta']
            self.data = []
            for y in range(0, int(i['height'])-1):
                temp = []
                for x in range(0, int(i['width'])-1):
                    cb = Codebook(alpha=self.alpha, beta=self.beta)
                    temp.append(cb)
                self.data.append(temp)
            for y in range(0, int(i['height'])-1):
                for x in range(0, int(i['width'])-1):
                    cb = self.data[y][x]
                    for v in i['data'][y][x]:
                        cb.codewords.append(Codeword(v))
        print(' ** model loaded: {}'.format(source))

    #Outputting the file           
    def build_output_file(self, source='', out=''):
        t = 1
        self.fm.output_init(out)
        while self.fm.get_next_frame():
            for y in range(0, self.fm.frame_height-1):
                for x in range(0, self.fm.frame_width-1):
                    pixel = self.fm.frame[y][x]
                    cb = self.data[y][x]
                    if cb.bgd(pixel):
                        self.fm.frame[y][x] = self.black
                    else:
                        self.fm.frame[y][x] = self.white
            self.fm.output_write_frame()
            t += 1
        self.fm.output_release()
        self.fm.cap.release()
        print(' ** output file built successfully')
