import collections
import cv2
import datetime
import gdown
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")
import numpy as np
import os
from sys import platform
from tkinter import *       
import tkinter as tk
from tkinter import ttk
from model import Classifier
from PIL import ImageTk, Image

if platform == "win32":
	from win10toast import ToastNotifier

def notify(title, text):
	if platform == 'linux' or platform == 'linux2':
		pass
	elif platform == "darwin":
	    os.system("""
	              osascript -e 'display notification "{}" with title "{}"'
	              """.format(text, title))
	elif platform == "win32":
		n = ToastNotifier() 
		n.show_toast(title, text, 
			duration = 5) 



if __name__ == "__main__":
	print("Loading up Remind A.I.")

	# download weights if not currently in directory
	if "model_resnet1" not in os.listdir():
		print("Downloading model ...")
		url = "https://drive.google.com/drive/folders/1FdiZFf07GAd6sm5rij2JM_bH0XuVleaD?usp=sharing"
		output = "model"
		gdown.download_folder(url, quiet=False)
	else:
		print("Model already downloaded")

	assert "model_resnet1" in os.listdir()

	classifierobj = Classifier()

	class app:
		def __init__(self, master):
			self.master = master
			self.master.geometry("800x600")

			logo_frame_in_use = Image.open("logo.png")
			width, height = logo_frame_in_use.size
			logo_aspect_ratio = width/height * 1.0
			new_width, new_height = int(logo_aspect_ratio*250), 250

			self.img = ImageTk.PhotoImage(logo_frame_in_use.resize((new_width, new_height)))

			self.intro()

			self.camera_initialized = False
			self.initialize_plots = False
			self.check_user_status_in_secs = 3 # how often to check status of user sitting and standing


		def intro(self):
			for i in self.master.winfo_children():
				i.destroy()
			self.frame1 = Frame(self.master)
			self.frame1.pack(fill="both")

			self.titlebarframe = Frame(self.frame1, background="black")
			self.titlebarframe.pack(fill="x")
			self.title_name = Label(self.titlebarframe, text="Remind A.I", font=('Lato', '38'), 
				fg="white", bg="#405982", bd=0)
			self.title_name.pack(fill="x", padx=1, pady=1)

			self.bottomframe = Frame(self.frame1)
			self.bottomframe.pack(pady=20, padx=20)

			self.logoframe = Frame(self.bottomframe, background="black")
			self.logoframe.pack(side="left")
			self.reg_img = Label(self.logoframe, image=self.img)
			self.reg_img.photo = self.img
			self.reg_img.pack(fill="both", padx=2, pady=2)

			self.start_btn = Button(self.bottomframe, text="Start", font=('Lato 32 bold'), command=self.main)
			self.start_btn.pack(side="left", pady=10, padx=20)


		def main(self):
			for i in self.master.winfo_children():
				i.destroy()

			self.frame2 = Frame(self.master)
			self.frame2.pack(fill="both")

			self.quickdescrptitlebar = Frame(self.frame2, background="black")
			self.quickdescrptitlebar.pack(fill="x")

			self.main_description = Label(self.quickdescrptitlebar, text="Using machine learning to prevent back-pain \n and improve physical health while working remote",
				font=('Lato 22'), fg="white", bg="#405982", bd=0, height=2)
			self.main_description.pack(fill="x", padx=2)
			self.small_description = Label(self.quickdescrptitlebar, text="Remind A.I \"reminds\" users to stand when sitting for prolonged periods of time",
				font=('Lato 16'), fg="white", bg="#405982", bd=0, height=2)
			self.small_description.pack(fill="x", padx=2)

			self.section1 = Frame(self.frame2)

			self.camera_test_section = Frame(self.section1)
			self.test_camera_error = Label(self.camera_test_section)
			self.test_camera_error.pack(fill="both")
			self.test_camera_description = Label(self.camera_test_section, text="Test out camera", font=('Lato', '14', 'bold'))
			self.test_camera_description.pack(fill="both")
			self.test_camera_button = Button(self.camera_test_section, text="Click to test", command=self.test_camera, font=('Lato', '12', 'bold'))
			self.test_camera_button.pack(fill="both")
			self.camera_status = Label(self.camera_test_section)
			self.camera_test = Label(self.camera_test_section)
			self.camera_test_section.pack(side="left", padx=20)

			self.limit_section = Frame(self.section1)
			self.limit_error_msg = Label(self.limit_section)
			self.limit_error_msg.pack(fill="both")
			self.sit_limit_label = Label(self.limit_section, text="Set a limit on how long you should sit (in minutes):", font=('Lato', '14', 'bold'))
			self.sit_limit_label.pack(fill="both")
			self.sit_limit_entry = ttk.Entry(self.limit_section, width=5)
			self.sit_limit_entry.pack()
			self.limit_section.pack(side="left", padx=20)

			self.section1.pack()

			self.selection_error_msg = Label(self.frame2)
			self.selection_error_msg.pack()
			self.selection_msg = Label(self.frame2, text="Select 1 or more of the options below.", font=('Lato', '12', 'bold'))
			self.selection_msg.pack()
			self.notification_option = IntVar(value=0)
			self.sound_alarm_option = IntVar(value=0)
			self.noption = Checkbutton(self.frame2, text='Notification', 
				variable=self.notification_option, onvalue=1, offvalue=0)
			self.aoption = Checkbutton(self.frame2, text='Sound alert', 
				variable=self.sound_alarm_option, onvalue=1, offvalue=0)
			self.noption.pack()
			self.aoption.pack()

			self.begin_rai = Button(self.frame2, text="Begin", command=self.error_check, font=('Lato 18 bold'), width=4)
			self.begin_rai.pack(padx=10, pady=10)


		def test_camera(self):
			if self.camera_initialized == False:
				self.cap = cv2.VideoCapture(0)
				if not self.cap.isOpened():
					self.camera_status.config(text="Cannot open video camera", font=('Lato 12 bold'))
					self.camera_status.config(fg="red")
					return
				else:
					self.camera_initialized = True
					self.camera_status.config(text="Successfully opened video camera", font=('Lato 12 bold'))
					self.camera_status.config(fg="green")

				self.test_camera_description.pack_forget()
				self.test_camera_button.pack_forget()

				self.camera_status.pack()
				self.camera_test.pack()

			# Capture the video frame by frame 
			_, frame = self.cap.read() 

			opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
			opencv_image = cv2.resize(opencv_image[:,::-1,:], (200,200))
			captured_image = Image.fromarray(opencv_image) 
			photo_image = ImageTk.PhotoImage(image=captured_image) 

			self.camera_test.photo_image = photo_image 
			self.camera_test.configure(image=photo_image)
			self.camera_test.after(10, self.test_camera) 
			return


		def error_check(self):
			selection_error, limit_error, camera_error = False, False, False

			if self.notification_option.get() == 0 and self.sound_alarm_option.get() == 0:
				self.selection_error_msg.config(text="Make sure to set at least 1 option below.")
				self.selection_error_msg.config(fg='#f00')
				self.selection_error_msg.config(font=('Lato 12 bold'))
				selection_error = True

			if not str.isdigit(self.sit_limit_entry.get()):
				self.limit_error_msg.config(text="Make sure limit is an integer.")
				self.limit_error_msg.config(fg='#f00')
				self.limit_error_msg.config(font=('Lato 12 bold'))
				limit_error = True
			else: 
				if int(self.sit_limit_entry.get()) > 30: # set limit of 30 minutes for now 
					self.limit_error_msg.config(text="Make sure to set limit <= 30 minutes")
					self.limit_error_msg.config(fg='#f00')
					self.limit_error_msg.config(font=('Lato 12 bold'))
					limit_error = True

			if self.camera_initialized == False:
				self.test_camera_error.config(text="Make sure to test camera before continuing")
				self.test_camera_error.config(fg="red")
				self.test_camera_error.config(font=('Lato 12 bold'))
				camera_error = True

			if selection_error or limit_error or camera_error:
				return

			self.sit_limit = int(self.sit_limit_entry.get())*60.0 # sit limit in seconds now
			self.sit_streak = 0

			return self.run()


		def run(self):
			for i in self.master.winfo_children():
				i.destroy()

			self.frame3 = Frame(self.master)
			self.frame3.pack(fill="both")

			self.main_description = Label(self.frame3, text="Tracking your sit and stand frequency ... ", font=('Lato 24'), 
				bg="#405982", fg="white")
			self.main_description.pack(fill="both")
			self.sub_description = Label(self.frame3, text="Feel free to minimize this window and continue with your work ", font=('Lato 16'), 
				bg="#405982", fg="white")
			self.sub_description.pack(fill="both")

			if self.initialize_plots == False:
				self.figure = Figure(figsize=(8, 4), dpi=100)
				self.figure.set_tight_layout(True)
				self.status_plt = self.figure.add_subplot(121)
				self.status_plt.tick_params(axis='x', labelrotation=45)
				self.freq_status_plt = self.figure.add_subplot(122)
				self.plots = FigureCanvasTkAgg(self.figure, self.frame3)
				self.plots.get_tk_widget().pack(fill=BOTH, expand=0, padx=20, pady=20)
				self.plots.draw()
				self.initialize_plots = True
				self.datay = []
				self.datax = []


			self.background_bottom_track_bar = Frame(self.frame3, background="#1c2b3b")
			self.bottom_track_bar = Frame(self.background_bottom_track_bar, background="#1c2b3b")	

			self.init_dt_frame = Frame(self.bottom_track_bar, background="#1c2b3b")
			init_curr_dt = datetime.datetime.now()
			init_curr_dt_str = datetime.datetime.strftime(init_curr_dt, "%H:%M:%S")
			self.initial_start_time_info = Label(self.init_dt_frame, text="Initial start time", font=('Lato 12'), fg="#9e9e9e", bg="#1c2b3b")
			self.initial_start_time = Label(self.init_dt_frame, text=init_curr_dt_str, font=('Lato 18 bold'), fg="white", bg="#1c2b3b")
			self.initial_start_time_info.pack()
			self.initial_start_time.pack()
			self.init_dt_frame.grid(row=0, column=0, padx=10, pady=10)

			self.user_sit_limit_frame = Frame(self.bottom_track_bar, background="#1c2b3b")
			self.user_sit_limit_info = Label(self.user_sit_limit_frame, text="User sit limit", font=('Lato 12'), fg="#9e9e9e", bg="#1c2b3b")
			self.user_sit_limit = Label(self.user_sit_limit_frame, text="{} (mins)".format(self.sit_limit//60), font=('Lato 18 bold'), fg="white", bg="#1c2b3b")
			self.user_sit_limit_info.pack()
			self.user_sit_limit.pack()
			self.user_sit_limit_frame.grid(row=0, column=1, padx=10, pady=10)

			self.end_rai = Button(self.bottom_track_bar, text="Stop", command=self.end_rai, font=('Lato 24 bold'), width=4)
			self.end_rai.grid(row=0, column=2, padx=10, pady=10)

			self.bottom_track_bar.pack()
			self.background_bottom_track_bar.pack(fill="both")

			self.track()
				

		def track(self):

			self.status_plt.clear()
			self.freq_status_plt.clear()

			curr_dt = datetime.datetime.now()
			curr_dt_str = datetime.datetime.strftime(curr_dt, "%H:%M:%S")

			_, frame = self.cap.read() 

			user_status = classifierobj.run_inference(frame) #random.choice(["sit","stand"])
			if user_status == 0:
				self.sit_streak += 1
			else:
				self.sit_streak = 0

			if (self.sit_streak * self.check_user_status_in_secs) > self.sit_limit:
				if self.notification_option.get() == 1:
					notify("Remind A.I.", "Time to take a break/stand.")

				if self.sound_alarm_option.get() == 1:
					# TODO: Work on adding alarm to notification if user requests it ... 
					notify("Remind A.I.", "Time to take a break/stand.")

			self.datay.append(user_status)
			self.datax.append(curr_dt_str)

			frequency = collections.Counter(self.datay)

			self.status_plt.step(self.datax[-10:], self.datay[-10:])
			self.status_plt.set_ylim((-.5, 1.5))
			self.status_plt.set_yticks([0, 1])
			self.status_plt.set_yticklabels(["sit", "stand"])
			self.status_plt.set_title("Status through time")

			self.freq_status_plt.bar(list(frequency.keys()), np.array(list(frequency.values()))/len(self.datay) * 1.0)
			self.freq_status_plt.set_ylim((0.0, 1.0))
			self.freq_status_plt.set_xlim((-.5, 1.5))
			self.freq_status_plt.set_xticks([0, 1])
			self.freq_status_plt.set_xticklabels(["sit", "stand"])
			self.freq_status_plt.set_title("Frequency of each status")

			self.plots.draw()
			self.frame3.after(self.check_user_status_in_secs*1000, self.track)


		def end_rai(self):
			for i in self.master.winfo_children():
				i.destroy()
			self.master.destroy()


	root = Tk()
	root.configure(background='gray')
	root.title("Remind A.I.")
	logo_photo = PhotoImage(file = 'logo.png')
	root.wm_iconphoto(False, logo_photo)     
	app(root)
	root.mainloop()















