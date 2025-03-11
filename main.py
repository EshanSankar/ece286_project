# TODO:
# -adding the actual tutorial gif and fixing the lag
# -adding the actual experiment images

import tkinter as tk
from PIL import Image, ImageTk
import cv2
import time

class App:
    def __init__(self, master):
        self.master = master
        self.master.attributes('-fullscreen', True)
        self.HEADER_FONT = "Arial 32 bold"
        self.BODY_FONT = "Arial 14"
        self.isDrawing = False
        self.isModifying = False
        self.fullRectangle = False
        self.edge_being_modified = None
        self.startX, self.startY, self.endX, self.endY = 0, 0, 0, 0
        self.temp_img = None
        self.beginTime = 0
        self.pracTime = 0
        self.home()
    
    def home(self): # Home page
        for i in self.master.winfo_children():
            i.destroy()
        self.frame_home = tk.Frame(self.master, width=1920, height=1080)
        self.frame_home.columnconfigure(0, weight=1)
        self.frame_home.rowconfigure([0, 1, 2, 3], minsize=300)
        self.frame_home.pack(expand=True, fill="both")
        self.text_home = tk.Label(self.frame_home, text="Welcome to the data annotator!", font=self.HEADER_FONT)
        self.text_home.grid(row=0,column=0)
        self.text_body = tk.Label(self.frame_home,
                                  text="Thank you for participating in our experiment! \n Here, you will perform bounding-box data annotation on images of stop signs. \n When you click 'Continue', you will be given a brief tutorial.",
                                  font=self.BODY_FONT)
        self.text_body.grid(row=1, column=0, sticky="n")
        self.button_begin = tk.Button(self.frame_home, text="Continue", width=25, height=5, command=self.guide)
        self.button_begin.grid(row=2, column=0)
    
    def guide(self): # Tutorial page with gif (gif needs to be made, and needs to be less laggy)
        for i in self.master.winfo_children():
            i.destroy()
        self.frame_guide = tk.Frame(self.master, width=1920, height=1080)
        self.frame_guide.columnconfigure(0, minsize=350)
        self.frame_guide.rowconfigure([0, 1, 2, 3], minsize=200)
        self.frame_guide.pack(expand=True, fill="both")
        self.text1_guide = tk.Label(self.frame_guide,
                                   text="A bounding box is a box drawn around an object of interest in an image, that contains the object as precisely as possible. \n You must draw precise bounding boxes that encapsulate only the stop signs, as perfectly as possible. \n Some images will have slanted or off-centered stop signs which cannot be perfectly bound, but a few pixels worth of leeway is okay. Just try to be as precise as you can.",
                                   font=self.BODY_FONT)
        self.text1_guide.grid(row=0, column=0, sticky="s")
        self.text2_guide = tk.Label(self.frame_guide,
                                   text="For each image, you can freely click and drag to create a box that captures the stop sign. \n You can also click and drag pre-created edges to correct them. \n Press 'Finish' as soon as you are satisfied with your drawing! \n Here is an example of a good bounding box being drawn:",
                                   font=self.BODY_FONT)
        self.text2_guide.grid(row=1, column=0, sticky="s")
        # gif configuration -- NEED TO ADD ANNOTATION GIF
        # file = "annotation.gif" # NEED TO ADD THIS
        # gif = Image.open(file)
        # self.frames = gif.n_frames
        # self.photoimage_objects = []
        # for i in range(self.frames):
        #     obj = tk.PhotoImage(file = file, format = f"gif -index {i}")
        #     self.photoimage_objects.append(obj)
        # self.gif_guide = tk.Label(self.frame_guide)
        # self.gif_guide.grid(row=2, column=0)
        # self.current_frame = 0
        # self.animation()
        # end gif configuration
        self.button_trial = tk.Button(self.frame_guide, text="Do an Example Annotation", width=25, height=5, command=self.trial)
        self.button_trial.grid(row=3, column=0)

    def trial(self): # The testing segment -- opens an OpenCV window
        for i in self.master.winfo_children():
            i.destroy()
        self.fullRectangle = False
        self.frame_trial = tk.Frame(self.master, width=1920, height=1080)
        self.frame_trial.pack(expand=True, fill="both")
        self.button_end = tk.Button(self.frame_trial, text="Finish", width=25, height=5, command=self.begin_screen)
        self.button_end.pack()
        self.image_cv2 = cv2.imread("Untitled.png", cv2.IMREAD_COLOR)
        cv2.namedWindow("Annotator")
        cv2.setMouseCallback("Annotator", self.drawRectangle, self.image_cv2)
        cv2.imshow("Annotator", self.image_cv2)
        self.beginTime = time.time()
        
    def begin_screen(self): # Confirmation screen before starting experiment
        self.pracTime = time.time() - self.beginTime # Times the test trial's duration
        cv2.destroyAllWindows()
        for i in self.master.winfo_children():
            i.destroy()
        print(f"{self.startX}, {self.startY}, {self.endX}, {self.endY}")
        self.frame_begin_screen = tk.Frame(self.master, width=1920, height=1080)
        self.frame_begin_screen.columnconfigure(0, weight=1)
        self.frame_begin_screen.rowconfigure([0, 1, 2], minsize=200)
        self.frame_begin_screen.pack(expand=True, fill="both")
        self.text_begin = tk.Label(self.frame_begin_screen,
                                   text=f"Time: {self.pracTime}. IoU: {self.calculateIoU([19, 65, 342, 393])}. \n You are about to begin the actual data annotation experiment. \n 'Begin Experiment' will start a timer and take you to the images. \n Remember to press 'Finish' after finishing each box. \n After 10 annotations, the program will finish.",
                                   font=self.HEADER_FONT)
        self.startX, self.startY, self.endX, self.endY = 0, 0, 0, 0
        self.clickOffset, self.clickOffsetL, self.clickOffsetT, self.clickOffsetR, self.clickOffsetB = 0, 0, 0, 0, 0
        self.text_begin.grid(row=0, column=0, sticky="s")
        self.button_begin_experiment = tk.Button(self.frame_begin_screen, text="Begin Experiment", width=25, height=5, command=self.begin_experiment)
        self.button_begin_experiment.grid(row=1, column=0, sticky="n")
        self.button_back = tk.Button(self.frame_begin_screen, text="Back to Guide", width=25, height=5, command=self.guide)
        self.button_back.grid(row=2, column=0, sticky="n")

    def begin_experiment(self): # Haven't implemented this yet
        root.destroy()
    
    def animation(self): # For gif, since Tkinter doesn't have built-in gifs
       if self.frames:
           self.gif_guide.config(image=self.photoimage_objects[self.current_frame])
           self.current_frame = self.current_frame + 1 if self.current_frame != self.frames else 0
           self.frame_guide.after(50, self.animation)

    def drawRectangle(self, event, x, y, flags, image): # Main OpenCV data annotation code for bounding boxes
        img = image
        
        # This code is for drawing the initial rectangle
        if event == cv2.EVENT_LBUTTONDOWN and not self.isDrawing and not self.fullRectangle:
            self.isDrawing = True
            self.startX, self.startY = x, y
        elif event == cv2.EVENT_MOUSEMOVE and self.isDrawing:
            self.temp_img = img.copy()
            cv2.rectangle(self.temp_img, (self.startX, self.startY), (x, y), (255, 0, 0), 3)
            cv2.imshow("Annotator", self.temp_img)
        elif event == cv2.EVENT_LBUTTONUP and self.isDrawing and not self.fullRectangle:
            self.isDrawing = False
            self.fullRectangle = True
            self.endX, self.endY = x, y
            # To preserve logic, might need to reverse start and end
            if self.endX < self.startX:
                self.endX, self.startX = self.startX, self.endX
            if self.endY < self.startY:
                self.endY, self.startY = self.startY, self.endY
            img = self.temp_img
            cv2.imshow("Annotator", img)
        
        # This is the code for being able to re-drag the rectangle's edges
        elif event == cv2.EVENT_LBUTTONDOWN and self.fullRectangle and not self.isModifying:
            edges = {
                'l': abs(x - self.startX),
                't': abs(y - self.startY),
                'r': abs(x - self.endX),
                'b': abs(y - self.endY)
            }
            self.edge_being_modified = min(edges, key=edges.get)
            if edges[self.edge_being_modified] > 15:
                return           
            self.isModifying = True
            #print(self.edge_being_modified)
        elif event == cv2.EVENT_MOUSEMOVE and self.isModifying:
            self.temp_img = img.copy()
            L = x if self.edge_being_modified == 'l' else self.startX
            T = y if self.edge_being_modified == 't' else self.startY
            R = x if self.edge_being_modified == 'r' else self.endX
            B = y if self.edge_being_modified == 'b' else self.endY
            cv2.rectangle(self.temp_img, (L, T), (R, B), (255, 0, 0), 3)
            cv2.imshow("Annotator", self.temp_img)
        elif event == cv2.EVENT_LBUTTONUP and self.isModifying:
            self.isModifying = False            
            self.startX = x if self.edge_being_modified == 'l' else self.startX
            self.startY = y if self.edge_being_modified == 't' else self.startY
            self.endX = x if self.edge_being_modified == 'r' else self.endX
            self.endY = y if self.edge_being_modified == 'b' else self.endY
            self.edge_being_modified = None
            if self.endX < self.startX:
                self.endX, self.startX = self.startX, self.endX
            if self.endY < self.startY:
                self.endY, self.startY = self.startY, self.endY
            img = self.temp_img
            cv2.imshow("Annotator", img)
    
    # Calculates IoU
    def calculateIoU(self, ground_truth): # ground_truth is a list: [GTstartX, GTstartY, GTendX, GTendY]
        A_measured = (self.endX - self.startX)*(self.endY - self.startY)
        A_ground_truth = (ground_truth[2] - ground_truth[0])*(ground_truth[3] - ground_truth[1])
        l_overlap = max(self.startX, ground_truth[0]) - min(self.endX, ground_truth[2]) if ((self.startX >= ground_truth[0] and self.startX <= ground_truth[2]) or (self.endX >= ground_truth[0] and self.endX <= ground_truth[2])) else 0
        h_overlap = max(self.startY, ground_truth[1]) - min(self.endY, ground_truth[3]) if ((self.startY >= ground_truth[1] and self.startY <= ground_truth[3]) or (self.endY >= ground_truth[1] and self.endY <= ground_truth[3])) else 0
        A_overlap = l_overlap * h_overlap
        A_union = A_measured + A_ground_truth - A_overlap
        IoU = A_overlap / A_union
        return IoU

if __name__ == '__main__':
    root = tk.Tk()
    App(root)
    root.mainloop()