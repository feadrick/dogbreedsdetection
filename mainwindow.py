
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\fead\Desktop\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import sys
import time
import numpy as np
import tensorflow as tf
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
filename=""
def load_graph(model_file):
	graph=tf.Graph()
	graph_def=tf.GraphDef()
	with open(model_file,"rb") as f:
		graph_def.ParseFromString(f.read())
	with graph.as_default():
		tf.import_graph_def(graph_def)
	return graph
def load_labels(label_file):
	label = []
	proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
	for l in proto_as_ascii_lines:
		label.append(l.rstrip())
	return label
def read_tensor_from_image_file(file_name, input_height=299, input_width=299,input_mean=0, input_std=255):
	input_name = "file_reader"
	output_name = "normalized"
	file_reader = tf.read_file(file_name, input_name)
	if file_name.endswith(".png"):
		image_reader = tf.image.decode_png(file_reader, channels = 3,name='png_reader')
	elif file_name.endswith(".gif"):
		image_reader = tf.squeeze(tf.image.decode_gif(file_reader,name='gif_reader'))
	elif file_name.endswith(".bmp"):
		image_reader = tf.image.decode_bmp(file_reader, name='bmp_reader')
	else:
		image_reader = tf.image.decode_jpeg(file_reader, channels = 3,name='jpeg_reader')
	float_caster = tf.cast(image_reader, tf.float32)
	dims_expander = tf.expand_dims(float_caster, 0);
	resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
	normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
	sess = tf.Session()
	result = sess.run(normalized)
	return result
class Ui_MainWindow(object):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(650, 417)
		MainWindow.setAutoFillBackground(False)
		MainWindow.setStyleSheet("background-color:rgb(213,100,90)")
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.imagelabel = QtWidgets.QLabel(self.centralwidget)
		self.imagelabel.setGeometry(QtCore.QRect(200, 30, 411, 251))
		self.imagelabel.setFrameShape(QtWidgets.QFrame.Box)
		self.imagelabel.setText("")
		self.imagelabel.setObjectName("imagelabel")
		self.getimage = QtWidgets.QPushButton(self.centralwidget)
		self.getimage.setGeometry(QtCore.QRect(54, 90, 131, 41))
		font = QtGui.QFont()
		font.setFamily("Kozuka Mincho Pro R")
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.getimage.setFont(font)
		self.getimage.setStyleSheet("color:white")
		self.getimage.setObjectName("getimage")
		self.imageresult = QtWidgets.QLabel(self.centralwidget)
		self.imageresult.setGeometry(QtCore.QRect(200, 300, 411, 71))
		self.imageresult.setFrameShape(QtWidgets.QFrame.Box)
		self.imageresult.setText("")
		self.imageresult.setObjectName("imageresult")
		font = QtGui.QFont()
		font.setFamily("Kozuka Mincho Pro R")
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.imageresult.setFont(font)
		self.imageresult.setStyleSheet("color:white")
		self.Analyseimage = QtWidgets.QPushButton(self.centralwidget)
		self.Analyseimage.setGeometry(QtCore.QRect(54, 150, 131, 41))
		font = QtGui.QFont()
		font.setFamily("Kozuka Mincho Pro R")
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.Analyseimage.setFont(font)
		self.Analyseimage.setStyleSheet("color:white")
		self.Analyseimage.setObjectName("Analyseimage")
		self.Opencamera = QtWidgets.QPushButton(self.centralwidget)
		self.Opencamera.setGeometry(QtCore.QRect(54,200, 131, 41))
		font = QtGui.QFont()
		font.setFamily("Kozuka Mincho Pro R")
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.Opencamera.setFont(font)
		self.Opencamera.setStyleSheet("color:white")
		self.Opencamera.setObjectName("Opencamera")
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 650, 21))
		self.menubar.setObjectName("menubar")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		self.getimage.clicked.connect(self.setImage)
		self.Analyseimage.clicked.connect(self.analyse)
	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Dog Breeds Detection"))
		self.getimage.setText(_translate("MainWindow", "Select Images"))
		self.Analyseimage.setText(_translate("MainWindow", "Analyse Image"))
		self.Opencamera.setText(_translate("MainWindow", "Open webcam"))
	def setImage(self):
		fileName,  _  = QtWidgets.QFileDialog.getOpenFileName(None, "Select Image", "", "Image Files (*.png *.jpg *jpeg *.bmp)")
		global filename
		filename= fileName
		if fileName:
			pixmap = QtGui.QPixmap(fileName) # Setup pixmap with the provided image
			pixmap = pixmap.scaled(self.imagelabel.width(), self.imagelabel.height(), QtCore.Qt.KeepAspectRatio) # Scale pixmap
			self.imagelabel.setPixmap(pixmap) # Set the pixmap onto the label
			self.imagelabel.setAlignment(QtCore.Qt.AlignCenter) # Align the label to center
	def analyse(self):
		global filename
		file_name =filename
		model_file = "retrained_graph.pb"
		label_file = "retrained_labels.txt"
		input_height = 299
		input_width = 299
		input_mean = 128
		input_std = 128
		input_layer = "Mul"
		output_layer = "final_result"
		graph = load_graph(model_file)
		t = read_tensor_from_image_file(file_name,input_height=input_height,input_width=input_width,input_mean=input_mean,input_std=input_std)
		input_name = "import/" + input_layer
		output_name = "import/" + output_layer
		input_operation = graph.get_operation_by_name(input_name);
		output_operation = graph.get_operation_by_name(output_name);

		with tf.Session(graph=graph) as sess:
			start = time.time()
			results = sess.run(output_operation.outputs[0],{input_operation.outputs[0]: t})
			end=time.time()
		results = np.squeeze(results)
		top_k = results.argsort()[-5:][::-1]
		labels = load_labels(label_file)

		print('\nEvaluation time (1-image): {:.3f}s\n'.format(end-start))
		template = "{} (score={:0.5f})"
		highest=0
		indexofhighest=0
		for i in top_k:
			if(results[i]>highest):
				highest=results[i]
				indexofhighest=i
		if(highest>0.84):
			self.imageresult.setText(template.format(labels[indexofhighest],highest))
		else:
			self.imageresult.setText("the image is not recorgnized")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
	
			