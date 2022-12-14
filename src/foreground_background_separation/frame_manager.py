import cv2

class FrameManager(object):
    num_of_frames = 0
    ret = False
    frame = None
    width = 0
    height = 0
    out = None
    #Set up videocapture for source video
    def __init__(self, path):
        print(' ** using source: "{}"'.format(path))
        self.path = path
        self.cap = cv2.VideoCapture(self.path)
        self.frame_width = 640
        self.frame_height = 480
        self.count_frames()


    #Use to reset video capture
    def reset(self):
        self.cap = cv2.VideoCapture(self.path)

    #To determine the number of frames in video file
    def count_frames(self):
        while True:
            ret, f = self.cap.read()
            if ret is False:
                break
            self.num_of_frames += 1
        self.reset()
        print(' ** total {} frames captured from source'.format(self.num_of_frames))

    #To iterates to next frame (if frame exists)
    def get_next_frame(self):
        self.ret, f = self.cap.read()
        if self.ret is True:     
            self.frame = cv2.resize(f, (self.frame_width, self.frame_height)) #all frames are resized to 640 x 480 here to reduce training time
            return True     #returns true if next frame exists, false if it does not
        return False

    #Creating a window and display the current frame
    def show_frame(self, wait=25):
        cv2.imshow('Capture Display', self.frame)
        if cv2.waitKey(wait) == ord('q'):
            self.close_window()

    #Closeing cv2 window and release resources
    def close_window(self):
        self.cap.release()
        cv2.destroyAllWindows()

    #Initialize resources required for creating avi file
    def output_init(self, filename):
        self.out = cv2.VideoWriter(
            filename+'.avi',
            cv2.VideoWriter_fourcc(*'DIVX'), 10.0, #DIVX prefered for common size video
            (self.frame_width, self.frame_height)
        )

    #Write current frame to output file
    def output_write_frame(self):
        self.out.write(self.frame)

    #Release cv2 video writer resources
    def output_release(self):
        self.out.release()

    #Release all cv2 related resources
    def __del__(self):
        if self.out is not None:
            self.out.release()
        self.cap.release()
        cv2.destroyAllWindows()
