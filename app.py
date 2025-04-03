from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtGui import QMovie, QImage
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import *

import cv2
import sys
import time
import pandas as pd
from openpyxl import load_workbook
from ui_mainwindow import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showFullScreen()

        self.isDrawing = False
        self.isModifying = False
        self.fullRectangle = False
        self.edge_being_modified = None
        self.startX, self.startY, self.endX, self.endY = 0, 0, 0, 0
        self.temp_img = None
        self.results = [0]*11
        self.IoUs = [0]*11
        self.times = [0]*11
        self.begin_time = 0
        self.name = ""
        self.distracted = 0 # 0 = no, 1 = yes
        # startX, startY, endX, endY
        self.ground_truths = [[370, 551, 642, 806], # example
                              [289, 573, 599, 891], # 1
                              [417, 413, 649, 646], # 2
                              [476, 567, 624, 830], # 3
                              [346, 511, 824, 964], # 4
                              [284, 401, 690, 793], # 5
                              [403, 460, 730, 791], # 6
                              [253, 529, 535, 802], # 7
                              [485, 742, 554, 811], # 8
                              [508, 590, 672, 843], # 9
                              [114, 832, 506, 1209],] # 10
        
        self.tutorial_gif = QMovie("annotation.gif")
        self.label_gif.setMovie(self.tutorial_gif)
        self.label_gif.setVisible(False)
        self.label_gif.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # replace with actual images
        self.images = [cv2.imread("images/example.jpg", cv2.IMREAD_COLOR),
                       cv2.imread("images/1.jpg", cv2.IMREAD_COLOR),
                       cv2.imread("images/2.jpg", cv2.IMREAD_COLOR),
                       cv2.imread("images/3.jpg", cv2.IMREAD_COLOR),
                       cv2.imread("images/4.jpg", cv2.IMREAD_COLOR),
                       cv2.imread("images/5.jpg", cv2.IMREAD_COLOR),
                       cv2.imread("images/6.jpg", cv2.IMREAD_COLOR),
                       cv2.imread("images/7.jpg", cv2.IMREAD_COLOR),
                       cv2.imread("images/8.jpg", cv2.IMREAD_COLOR),
                       cv2.imread("images/9.jpg", cv2.IMREAD_COLOR),
                       cv2.imread("images/10.jpg", cv2.IMREAD_COLOR)]
        self.c = 0

        # defining widget functionality from Ui_MainWindow
        self.button_home.clicked.connect(self.next_page)
        self.button_next.clicked.connect(self.next_page)
        self.button_previous.clicked.connect(self.previous_page)
        self.button_next_2.clicked.connect(self.next_page)
        self.button_previous_2.clicked.connect(self.previous_page)
        self.stackedWidget.currentChanged.connect(self.display_annotator)
        self.button_finished_tutorial.clicked.connect(self.finish_annotation)
        self.button_finished_tutorial.clicked.connect(self.next_page)
        self.button_guide.clicked.connect(self.back_to_guide)
        self.button_begin.clicked.connect(self.next_page)
        self.button_finished.clicked.connect(self.finish_annotation)
        self.lineEdit.textChanged.connect(self.get_data)
        self.button_begin.clicked.connect(self.get_data)
        self.button_done.clicked.connect(exit)
        self.button_begin.setDisabled(True)
    def get_data(self):
        self.name = self.lineEdit.text()
        self.distracted = 1 if self.radioButton.isChecked() else 0
        self.button_begin.setEnabled(True)
    def display_annotator(self):
        if self.stackedWidget.currentIndex() == 3 or self.stackedWidget.currentIndex() == 5:
            self.display_image()
        else:
            cv2.destroyAllWindows()

    def next_page(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() + 1)
        self.play_gif()
    def previous_page(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.currentIndex() - 1)
        self.play_gif()
    def back_to_guide(self):
        self.stackedWidget.setCurrentIndex(1)
    def finish_annotation(self):
        self.times[self.c] = time.time() - self.begin_time
        cv2.destroyAllWindows()
        self.isDrawing = False
        self.isModifying = False
        self.fullRectangle = False
        self.edge_being_modified = None
        self.results[self.c] = [self.startX, self.startY, self.endX, self.endY]
        self.startX, self.startY, self.endX, self.endY = 0, 0, 0, 0
        self.temp_img = None
        self.IoUs[self.c] = self.calculateIoU(self.results[self.c], self.ground_truths[self.c])
        self.label_start.setText(QtCore.QCoreApplication.translate("MainWindow", f"<html><head/><body><p align=\"center\"><span style=\" font-size:18pt; font-weight:700;\">Your Practice Results: Accuracy (IoU): {self.IoUs[0]}. Time (s): {self.times[0]}. </span></p><p align=\"center\"><span style=\" font-size:12pt;\">You are about to begin the actual data annotation experiment. &quot;BEGIN EXPERIMENT&quot; will start a timer and take you to the images. </span></p><p align=\"center\"><span style=\" font-size:12pt;\">You will annotate each of 10 images sequentially. Press &quot;FINISHED&quot; after you are satisfied with each box, and the next image will automatically appear.</span></p><p align=\"center\"><span style=\" font-size:12pt;\">You may return to the guide now if you would like a refresher. If you are ready to start the experiment, please fill out the following:</span></p></body></html>"))
        self.c += 1
        if self.c < 11:
            self.display_annotator()
        if self.c == 11:
            self.finish_experiment()

    def play_gif(self):
        if (self.stackedWidget.currentIndex() == 2):
            self.label_gif.setVisible(True)
            self.tutorial_gif.start()
        else:
            self.label_gif.setVisible(False)
            self.tutorial_gif.stop()

    def display_image(self):
        img = self.images[self.c]
        cv2.namedWindow("Annotator")
        cv2.moveWindow("Annotator", 878, -100)
        cv2.setWindowProperty("Annotator", cv2.WND_PROP_VISIBLE, 1)
        cv2.setWindowProperty("Annotator", cv2.WND_PROP_TOPMOST, 1)
        cv2.setMouseCallback("Annotator", self.drawRectangle, img)
        cv2.imshow("Annotator", img)
        self.begin_time = time.time()
    def finish_experiment(self):
        self.stackedWidget.setCurrentIndex(6)
        df_results = pd.DataFrame([self.name, self.distracted,
                                   self.times[1], self.IoUs[1],
                                   self.times[2], self.IoUs[2],
                                   self.times[3], self.IoUs[3],
                                   self.times[4], self.IoUs[4],
                                   self.times[5], self.IoUs[5],
                                   self.times[6], self.IoUs[6],
                                   self.times[7], self.IoUs[7],
                                   self.times[8], self.IoUs[8],
                                   self.times[9], self.IoUs[9],
                                   self.times[10], self.IoUs[10]]).T
        wb = load_workbook("results.xlsx")
        ws = wb["Sheet1"]
        data = df_results.values.flatten().tolist()
        ws.append(data)
        wb.save("results.xlsx")
    
    def drawRectangle(self, event, x, y, flags, img): # Main OpenCV data annotation code for bounding boxes
        # This code is for drawing the initial rectangle
        if event == cv2.EVENT_LBUTTONDOWN and not self.isDrawing and not self.fullRectangle:
            self.isDrawing = True
            self.startX, self.startY = x, y
        elif event == cv2.EVENT_MOUSEMOVE and self.isDrawing:
            self.temp_img = img.copy()
            cv2.rectangle(self.temp_img, (self.startX, self.startY), (x, y), (255, 0, 0), 4)
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
        elif event == cv2.EVENT_MOUSEMOVE and self.isModifying:
            self.temp_img = img.copy()
            L = x if self.edge_being_modified == 'l' else self.startX
            T = y if self.edge_being_modified == 't' else self.startY
            R = x if self.edge_being_modified == 'r' else self.endX
            B = y if self.edge_being_modified == 'b' else self.endY
            cv2.rectangle(self.temp_img, (L, T), (R, B), (255, 0, 0), 4)
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
    def calculateIoU(self, results, ground_truth): # ground_truth is a list: [GTstartX, GTstartY, GTendX, GTendY]
        A_measured = (results[2] - results[0])*(results[3] - results[1])
        A_ground_truth = (ground_truth[2] - ground_truth[0])*(ground_truth[3] - ground_truth[1])
        l_overlap = min(results[2], ground_truth[2]) - max(results[0], ground_truth[0])
        h_overlap = min(results[3], ground_truth[3]) - max(results[1], ground_truth[1])
        A_overlap = l_overlap * h_overlap
        if results[0] >= ground_truth[2] or results[1] >= ground_truth[3] or results[2] <= ground_truth[0] or results[3] <= ground_truth[1]:
            A_overlap = 0
        A_union = A_measured + A_ground_truth - A_overlap
        IoU = A_overlap / A_union
        return IoU


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())