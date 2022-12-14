import uuid
from foreground_background_separation.cb_engine import CodebookEngine

#Set up python enviroment to run the code
class CbShell(object):
    path_to_source = 'source/'
    path_to_output = 'output/'
    path_to_models = 'models/' 
    _running = False
    def __init__(self):
        pass
    #Getting input from user
    def run(self):
        self._running = True
        while self._running:
            cmd = input('>> ')
            exe = self.parse(cmd)
            if exe != None:
                self.execute(exe)
    #Parsing input
    def parse(self, cmd):
        li = cmd.split(' ')
        if li[0] == '':
            return
        if li[0] == 'train':
            return self.build_training_exe(li)
        elif li[0] == 'separate':
            return self.build_separate_exe(li)
        elif li[0] == 'exit':
            print(' ** Exiting')
            self._running = False
        else:
            print(' ** Invalid command')
    #Executing input
    def execute(self, exe):
        if exe.cmd == 'train': #train a model from the source
            try:
                cbe = CodebookEngine()
                cbe.init_frame_manager(source=self.path_to_source+exe.source, alpha=exe.alpha, beta=exe.beta)
                cbe.init_codebooks()
                cbe.build_codebooks()
                cbe.clean_lambdas()
                cbe.temporal_filtering()
                cbe.save_model(name=self.path_to_models+exe.name)
            except:
                print("An error occurred. Please check that the arguments provided are correct.")

        elif exe.cmd == 'separate': #separate the source and model for output
            try:
                cbe = CodebookEngine()
                cbe.init_frame_manager(source=self.path_to_source+exe.source, alpha=exe.alpha, beta=exe.beta)
                cbe.load_model(source=self.path_to_models+exe.model)
                cbe.build_output_file(source=exe.source, out=self.path_to_output+exe.out)
            except:
                print("An error occurred. Please check that the arguments provided are correct.")
    #Building the train model function
    def build_training_exe(self, li):
        index = 1
        exe = RunConfig()
        exe.cmd = 'train'
        while index < len(li):
            if li[index] == '--source':
                if index+1 >= len(li):
                    print(' ** missing parameter value for [--source], please provide a value for this parameter')
                else:
                    exe.source = li[index+1]
            elif li[index] == '--name':
                if index+1 >= len(li):
                    print(' ** missing parameter value for [--name], please provide a value for this parameter')
                else:
                    exe.name = li[index+1]
            ##elif li[index] == '--alpha':
            #    if index+1 >= len(li):
            #        print(' ** missing parameter value for [--alpha], please provide a value for this parameter, or omit')
            #    else:
            #        exe.alpha = float(li[index+1])
            #elif li[index] == '--beta':
            #    if index+1 >= len(li):
            #        print(' ** missing parameter value for [--beta], please provide a value for this parameter, or omit')
            #    else:
            #        exe.beta = float(li[index+1])
            else:
                print(' ** invalid parameter: [{}]'.format(li[index]))
                break
            index+=2
        if exe.source == '':
            print(' ** missing required parameter [--source]')
            return
        if exe.name == '':
            print(' ** missing required parameter [--name]')
            return
        return exe
    #Building the separate function
    def build_separate_exe(self, li):
        index = 1
        exe = RunConfig()
        exe.cmd = 'separate'
        while index < len(li):
            if li[index] == '--source':
                if index+1 >= len(li):
                    print(' ** missing parameter value for [--source], please provide a value for this parameter')
                else:
                    exe.source = li[index+1]
            elif li[index] == '--model':
                if index+1 >= len(li):
                    print(' ** missing parameter value for [--model], please provide a value for this parameter')
                else:
                    exe.model = li[index+1]
            elif li[index] == '--out':
                if index+1 >= len(li):
                    print(' ** missing parameter value for [--out], please provide a value for this parameter')
                else:
                    exe.out = li[index+1]
            else:
                print(' ** invalid parameter: [{}]'.format(li[index]))
                break
            index+=2
        if exe.source == '':
            print(' ** missing required parameter [--source]')
            return
        if exe.out == '':
            print(' ** missing required parameter [--out]')
            return
        if exe.model == '':
            print(' ** missing required parameter [--model]')
            return
        return exe

# RunConfig object class:
class RunConfig(object):
    cmd = ''
    name = str(uuid.uuid1())
    source = ''
    model = ''
    alpha = 0.4
    beta = 1.5
    out = str(uuid.uuid1())
    def __init__(self):
        pass