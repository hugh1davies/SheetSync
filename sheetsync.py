import os
import subprocess
import sys
# List of required modules
required_modules = ['cv2', 'numpy', 'math', 'fpdf', 'pytube', 'tkinter', 'PIL', 'super_image', 'tqdm', 'BeautifulSoup4', 'yt_dlp', 'tqdm']

# Check and install required modules
def install_module(module):
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', module])
    except subprocess.CalledProcessError:
        print(f"Failed to install {module}")

def check_install_modules():
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            print(f"{module} is not installed. Installing...")
            install_module(module)

if __name__ == "__main__":
    check_install_modules()

import shutil
import cv2
import numpy as np
import math
from fpdf import FPDF
from pytube import YouTube
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from io import BytesIO
from super_image import EdsrModel, ImageLoader
from PIL import Image
import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tqdm import tqdm
import time
import inspect
import os
import re
import yt_dlp
import requests
from bs4 import BeautifulSoup
from tkinter import Scale



class CustomFPDF(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation=orientation, unit=unit, format=format)

    def image(self, image, x=None, y=None, w=0, h=0, type='', link=''):
        self._out('<q>')
        super().image(image, x, y, w, h, type, link)
        self._out('</q>')


class SheetMusicDownloader:
    def __init__(self):
        self.window = Tk()
        self.window.title("Sheet Music Downloader")
        self.window.geometry("800x600")

        self.source_var = StringVar()
        self.source_var.set("youtube")  # Default to YouTube as the source

        self.source_label = Label(self.window, text="Source Type:")
        self.source_label.pack()

        self.source_radio_frame = Frame(self.window)
        self.source_radio_frame.pack()

        self.youtube_radio = Radiobutton(self.source_radio_frame, text="YouTube", variable=self.source_var, value="youtube", command=self.update_entry_label)
        self.youtube_radio.pack(side=LEFT, padx=5)

        self.local_radio = Radiobutton(self.source_radio_frame, text="Local MP4", variable=self.source_var, value="local", command=self.update_entry_label)
        self.local_radio.pack(side=LEFT, padx=5)

        self.link_mp4_label = Label(self.window, text="YouTube Link or MP4 File Path:")
        self.link_mp4_label.pack()
        
        self.link_mp4_entry = Entry(self.window)
        self.link_mp4_entry.pack(pady=5)
        self.link_mp4_entry.bind("<KeyRelease>", self.validate_link)

        self.num_images_label = Label(self.window, text="Number of Images per Page:")
        self.num_images_label.pack()

        self.num_images_entry = Entry(self.window)
        self.num_images_entry.pack(pady=5)

        self.download_button = ttk.Button(self.window, text="Download", command=self.download_sheet_music)
        self.download_button.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self.window, orient=HORIZONTAL, mode='determinate')
        self.progress_bar.pack(fill=X, padx=10, pady=10)

        self.orientation_var = StringVar()
        self.orientation_var.set("portrait")  # Default to portrait orientation

        self.orientation_label = Label(self.window, text="PDF Orientation:")
        self.orientation_label.pack()

        self.orientation_radio_frame = Frame(self.window)
        self.orientation_radio_frame.pack()

        self.portrait_radio = Radiobutton(self.orientation_radio_frame, text="Portrait", variable=self.orientation_var, value="portrait")
        self.portrait_radio.pack(side=LEFT, padx=5)

        self.landscape_radio = Radiobutton(self.orientation_radio_frame, text="Landscape", variable=self.orientation_var, value="landscape")
        self.landscape_radio.pack(side=LEFT, padx=5)

        self.upscale_var = StringVar()
        self.upscale_var.set("Disabled")  # Default to no upscaling

        self.upscale_label = Label(self.window, text="AI Upscaler:")
        self.upscale_label.pack()

        self.upscale_radio_frame = Frame(self.window)
        self.upscale_radio_frame.pack()

        self.no_upscale_radio = Radiobutton(self.upscale_radio_frame, text="Disabled", variable=self.upscale_var, value="Disabled")
        self.no_upscale_radio.pack(side=LEFT, padx=5)

        self.waifu2x_radio = Radiobutton(self.upscale_radio_frame, text="Enabled", variable=self.upscale_var, value="Enabled", command=self.update_upscale_label)
        self.waifu2x_radio.pack(side=LEFT, padx=5)

        self.image_buttons = []
        self.selected_images = []
        
        self.window.bind_all("<Control-a>", self.select_all_images)
        self.window.bind_all("<Control-A>", self.select_all_images)


        
        self.include_title_page_var = IntVar()
        self.include_title_page_var.set(1)  # Default to including the title page

        # Checkbox to allow the user to include or exclude the title page
        self.include_title_page_checkbox = Checkbutton(self.window, text="Include Title Page", variable=self.include_title_page_var)
        self.include_title_page_checkbox.pack(pady=5)
        
        
        self.threshold_label = Label(self.window, text="Threshold Value:")
        self.threshold_label.pack()

        self.threshold_slider = Scale(self.window, from_=180, to=255, orient=HORIZONTAL, length=200,
                                      command=self.update_threshold)
        self.threshold_slider.set(254)  # Initial threshold value
        self.threshold_slider.pack()
        
        
        
        
        
        self.folder_path = None


    

    


    def validate_link(self, event):
        link_mp4 = self.link_mp4_entry.get()

        # Remove quotation marks from the link
        link_mp4 = link_mp4.strip('"')

        # Check if the entry is not blank before performing validation
        if link_mp4:
            if self.source_var.get() == "local":
                # If the source is local, validate the local file
                self.validate_local_file(link_mp4)
            elif self.is_valid_youtube_link(link_mp4):
                # Valid YouTube link, set the background color to a lighter shade of green
                self.link_mp4_entry.config(bg='#d7ffd9')  # You can adjust the color code
            else:
                # Invalid YouTube link, set the background color to a lighter shade of red
                self.link_mp4_entry.config(bg='#ffb5b5')  # You can adjust the color code
        else:
            # Blank entry, set the background color to default (white or any other color you prefer)
            self.link_mp4_entry.config(bg='white')

    def is_valid_youtube_link(self, link):
        try:
            YouTube(link)
            return True
        except:
            return False



    def run(self):
        self.window.mainloop()
        create_pdf_button = ttk.Button(self.window, text="Create PDF", command=self.create_pdf)
        create_pdf_button.pack(pady=10)



    def update_upscale_label(self):
            if self.upscale_var.get() == "Disabled":
                print()
            elif self.upscale_var.get() == "Enabled":
                messagebox.showwarning("Upscale Warning", "Enabling AI upscaling can be resource-intensive and may significantly increase the time to create the PDF. Are you sure you want to proceed?")
                self.upscale_warning_shown = True
                
                
                
                
    def update_threshold(self, value):
        # Update the threshold value based on the slider
        self.threshold_value = int(value)



    
    def update_entry_label(self):
        source_type = self.source_var.get()

        if source_type == "local":
            self.link_mp4_label.config(text="MP4 File Path:")

            # Validate the file existence and set the background color accordingly
            link_mp4 = self.link_mp4_entry.get()
            self.validate_local_file(link_mp4)  # Pass the file path as an argument

            # Hide the title page checkbox for local source
            self.include_title_page_checkbox.pack_forget()
        else:
            self.link_mp4_label.config(text="YouTube Link:")

            # Show the title page checkbox for non-local sources
            self.include_title_page_checkbox.pack(pady=5)

    def validate_local_file(self, file_path):
    # Remove quotation marks from the file path
        file_path = file_path.strip('"')

        # Check if the file exists
        if os.path.exists(file_path):
            # File exists, set the background color to a lighter shade of green
            self.link_mp4_entry.config(bg='#d7ffd9')  # You can adjust the color code
        else:
            # File doesn't exist, set the background color to a lighter shade of red
            self.link_mp4_entry.config(bg='#ffb5b5')  # You  codeYou can adjust the color code
            
            
            
            
    def get_video_description(self, youtube_link):
        try:
            ydl_opts = {
                'format': 'best',
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(youtube_link, download=False)
                return result.get('description')
        except Exception as e:
            print(f"Error fetching video description: {str(e)}")
            return None

    def find_links(self, youtube_link):
        try:
            # Download the video description using yt_dlp
            video_description = self.get_video_description(youtube_link)

            # Check if the video description is empty or None
            if not video_description:
                print("Video description is empty.")
                return None

            # Extract all links using regular expressions
            all_links = re.findall(r'https?://\S+', video_description)

            # Filter links related to sheet music
            sheet_music_links = []

            # Split the video description into sentences
            sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', video_description)

            for sentence, link in zip(sentences, all_links):
                # Check if the sentence contains keywords related to sheet music
                if 'sheet music' in sentence.lower() or 'music sheet' in sentence.lower() or 'music' in sentence.lower() or 'muse' in sentence.lower() or 'score' in sentence.lower() or 'pdf' in sentence.lower():
                    sheet_music_links.append(link)

            return sheet_music_links

        except Exception as e:
            print(f"Error: {str(e)}")

        return None
            
            


    def download_sheet_music(self):
        source_type = self.source_var.get()
        num_images_per_page = int(self.num_images_entry.get())
        link_mp4 = self.link_mp4_entry.get()

        if not link_mp4 or not num_images_per_page:
            messagebox.showerror("Error", "Please provide the YouTube link or MP4 file path and number of images per page.")
            return

        folder_path = filedialog.askdirectory(title="Select Folder")
        if not folder_path:
            return

        self.folder_path = folder_path  # Set the instance variable

        frame_folder_path = os.path.join(self.folder_path, "frames")
        os.makedirs(frame_folder_path, exist_ok=True)

        cap = None
        count = 0

        try:
            if source_type == "youtube":
                video = YouTube(link_mp4)
                video_stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                video_stream.download(output_path=folder_path, filename="video.mp4")
                cap = cv2.VideoCapture(os.path.join(folder_path, "video.mp4"))

                sheet_music_links = self.find_links(link_mp4)

                if sheet_music_links:
                    # Display an information message box with the found sheet music links
                    message = "Potential sheet music links found:\n\n" + "\n".join(sheet_music_links)
                    messagebox.showinfo("Sheet Music Links", message)
                else:
                    # Display a message box indicating no sheet music links were found
                    messagebox.showinfo("Sheet Music Links", "No potential sheet music links found.")

                
                
            elif source_type == "local":
                # Copy the local MP4 file to the selected folder and rename it to "video.mp4"
                shutil.copy(link_mp4.strip('"'), os.path.join(folder_path, "video.mp4"))

                cap = cv2.VideoCapture(os.path.join(folder_path, "video.mp4"))

            if cap is None or not cap.isOpened():
                messagebox.showerror("Error", "Failed to open the video file. Please check if the file path is correct.")
                return

            frame_rate = math.ceil(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            self.progress_bar['maximum'] = total_frames

            prev_frame = None

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                if total_frames > 0:
                    self.progress_bar['value'] = total_frames - cap.get(cv2.CAP_PROP_FRAME_COUNT)

                if cap.get(cv2.CAP_PROP_POS_FRAMES) % frame_rate == 0:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    # Apply adaptive thresholding
                    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

                    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    max_area = 0
                    best_cnt = None
                    for cnt in contours:
                        area = cv2.contourArea(cnt)
                        if area > max_area:
                            max_area = area
                            best_cnt = cnt

                    if best_cnt is not None:
                        x, y, w, h = cv2.boundingRect(best_cnt)
                        crop = frame[y:y + h, x:x + w]

                        if prev_frame is not None:
                            if prev_frame.shape != crop.shape:
                                prev_frame = cv2.resize(prev_frame, crop.shape[:2][::-1])

                            diff = cv2.absdiff(prev_frame, crop)
                            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
                            _, thresh = cv2.threshold(gray, self.threshold_value, 255, cv2.THRESH_BINARY)

                            if np.sum(thresh) == 0:
                                continue

                        cv2.imwrite(os.path.join(frame_folder_path, f"frame{count}.jpg"), crop)
                        prev_frame = crop
                    else:
                        file_path = os.path.join(frame_folder_path, f"frame{count}.jpg")
                        try:
                            os.remove(file_path)
                        except OSError as e:
                            print(f"Error removing file {file_path}: {e}")

                count += 1
                self.progress_bar['value'] = count
                self.window.update()


            frame_files = sorted(os.listdir(frame_folder_path),
                                 key=lambda x: int(x.split('frame')[1].split('.jpg')[0]))

            blank_frames = []
            for i in range(len(frame_files)):
                img_path = os.path.join(frame_folder_path, frame_files[i])
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                _, thresh = cv2.threshold(img, 1, 255, cv2.THRESH_BINARY)
                if np.sum(thresh) == 0:
                    blank_frames.append(i)

            for i in blank_frames[::-1]:
                frame_file = frame_files[i]
                os.remove(os.path.join(frame_folder_path, frame_file))
                frame_files.pop(i)

            selection_window = Toplevel(self.window)
            selection_window.title("Image Selection")
            selection_window.geometry("800x600")

            canvas = Canvas(selection_window, width=780, height=560)
            canvas.pack(side=LEFT, fill=BOTH, expand=True)

            scrollbar = ttk.Scrollbar(selection_window, command=canvas.yview)
            scrollbar.pack(side=RIGHT, fill=Y)

            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

            image_frame = Frame(canvas)
            canvas.create_window((0, 0), window=image_frame, anchor="nw")

            def toggle_selection(image_index):
                if image_index in self.selected_images:
                    self.selected_images.remove(image_index)
                    self.image_buttons[image_index].config(relief=RAISED)
                else:
                    self.selected_images.append(image_index)
                    self.image_buttons[image_index].config(relief=SUNKEN)

            def delete_image(image_index):
                image_path = os.path.normpath(os.path.join(frame_folder_path, frame_files[image_index]))

                if os.path.exists(image_path):
                    os.remove(image_path)
                    frame_files.pop(image_index)
                    for i in range(len(self.selected_images)):
                        if self.selected_images[i] > image_index:
                            self.selected_images[i] -= 1
                    update_preview()

            selection_window.bind("<KeyPress>", self.on_key_press)

            self.image_buttons = []
            for i, file_name in enumerate(frame_files):
                img_path = os.path.join(frame_folder_path, file_name)
                img = Image.open(img_path)
                img = img.resize((200, 200))
                photo = ImageTk.PhotoImage(img)

                row = i // 5
                column = i % 5

                image_button = Button(image_frame, image=photo, command=lambda i=i: toggle_selection(i))
                image_button.image = photo
                image_button.grid(row=row, column=column, padx=5, pady=5)
                self.image_buttons.append(image_button)

                # Bind the right-click event to the image button
                image_button.bind("<Button-3>", lambda event, img_path=img_path: self.show_enlarged_image(img_path))

            create_pdf_button = ttk.Button(selection_window, text="Create PDF", command=self.create_pdf)
            create_pdf_button.pack(pady=10)

            canvas.config(scrollregion=canvas.bbox("all"))

        except Exception as e:
            messagebox.showerror("Error", f"{str(e)} Error at line {inspect.currentframe().f_lineno}")
        
        finally:
            if cap is not None:
                cap.release()

    def on_key_press(self, event):
        if event.keysym == 'BackSpace':
            if len(self.selected_images) > 0:
                image_index = self.selected_images[-1]
                self.delete_image(image_index)

    def delete_image(self, image_index):
        image_path = os.path.join(frame_folder_path, frame_files[image_index])
        if os.path.exists(image_path):
            os.remove(image_path)
            frame_files.pop(image_index)
            for i in range(len(self.selected_images)):
                if self.selected_images[i] > image_index:
                    self.selected_images[i] -= 1
            self.update_preview()
            
            
            
    def show_enlarged_image(self, img_path):
        # Function to show an enlarged version of the image when right-clicked
        enlarged_window = Toplevel(self.window)
        enlarged_window.title("Enlarged Image")
        img = Image.open(img_path)
        img = img.resize((800, 800))
        photo = ImageTk.PhotoImage(img)

        label = Label(enlarged_window, image=photo)
        label.image = photo
        label.pack(padx=10, pady=10)
        
        
        
    
        
        
        
    

    def upscale_image(self, img):

        model = EdsrModel.from_pretrained('eugenesiow/edsr-base', scale=2)
        inputs = ImageLoader.load_image(img)
        preds = model(inputs)

        # Save the scaled image
        upscale_path = os.path.join(self.folder_path, "upscaled_image.jpg")
        ImageLoader.save_image(preds, upscale_path)
        
        
        
        with tqdm(total=100, desc="Upscaling Images", dynamic_ncols=True) as pbar:
            for _ in range(100):
                time.sleep(0.1)  # Simulate the upscale process (you can replace this with the actual upscale process)
                pbar.update(1)

        # Convert the PIL image to OpenCV format for sharpening
        cv_image = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        # Define a sharpening kernel (3x3 matrix)
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])

        # Apply the sharpening filter
        sharpened = cv2.filter2D(cv_image, -1, kernel)

        # Save the sharpened image with a new name
        sharpened_output_path = upscale_path.replace('frame', 'upscaled_frame')
        cv2.imwrite(sharpened_output_path, sharpened)

        return sharpened_output_path
    
    
    
    def select_all_images(self, event):
        # Function to select all images when Ctrl + A is pressed
        self.selected_images = list(range(len(self.image_buttons)))

        # Update the buttons to show them as selected
        for button in self.image_buttons:
            button.config(relief=SUNKEN)
        

    def create_pdf(self):
        if self.folder_path is None:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        pdf_folder_path = os.path.join(self.folder_path, "pdf")
        if os.path.exists(pdf_folder_path):
            shutil.rmtree(pdf_folder_path)
        os.mkdir(pdf_folder_path)

        pdf = CustomFPDF(orientation=self.orientation_var.get(), unit="pt", format="A4")
        pdf.set_auto_page_break(auto=True, margin=0)

        try:
            if self.source_var.get() == "youtube" and self.include_title_page_var.get():
                # Get YouTube video details for the title page
                video = YouTube(self.link_mp4_entry.get())
                video_title = video.title
                video_channel = video.author

                # Add title page only if the checkbox is selected
                pdf.add_page()
                pdf.set_font("Arial", style="B", size=20)

                # Center the YouTube video title on the page
                title_x = (pdf.w - pdf.get_string_width(video_title)) / 2
                pdf.set_x(title_x)
                pdf.cell(0, 10, video_title, ln=True, align="C")

                pdf.ln(10)
                pdf.set_font("Arial", style="I", size=16)
                pdf.cell(0, 10, f"Composer/Arranger: {video_channel}", ln=True, align="C")
                pdf.ln(20)

            image_folder_path = os.path.join(self.folder_path, "frames")
            frame_files = sorted(os.listdir(image_folder_path), key=lambda x: int(x.split('frame')[1].split('.jpg')[0]))
            num_images_per_page = int(self.num_images_entry.get())
            selected_images = sorted(self.selected_images)  # Sort the selected image indices

            for i, img_index in enumerate(selected_images):
                if i % num_images_per_page == 0:
                    pdf.add_page()

                img_path = os.path.join(image_folder_path, frame_files[img_index])
                img = Image.open(img_path)

                # Upscale image using AI upscaler if enabled
                if self.upscale_var.get() == "Enabled":
                    upscale_path = self.upscale_image(img)
                    img = Image.open(upscale_path)

                    # Save the upscaled image directly to the frames folder with the same name
                    img.save(img_path, "JPEG")

                # Calculate the maximum dimensions to fit within the PDF page while maintaining aspect ratio
                pdf_width, pdf_height = pdf.w, pdf.h
                aspect_ratio = img.width / img.height
                max_img_width = pdf_width
                max_img_height = pdf_height / num_images_per_page  # Divide by the number of images per page

                if aspect_ratio > 1:
                    img_width = min(max_img_width, max_img_height * aspect_ratio)
                    img_height = img_width / aspect_ratio
                else:
                    img_height = min(max_img_height, max_img_width / aspect_ratio)
                    img_width = img_height * aspect_ratio

                # Calculate the position for each image on the page
                x_position = (pdf_width - img_width) / 2
                y_position = (i % num_images_per_page) * (pdf_height / num_images_per_page)

                # Create a temporary file to store the resized image (not needed anymore)
                # temp_img_path = os.path.join(self.folder_path, f"temp_{i}.jpg")
                # img = img.resize((int(img_width), int(img_height)), Image.ANTIALIAS)
                # img.save(temp_img_path, "JPEG")

                pdf.image(img_path, x=x_position, y=y_position, w=img_width, h=img_height)

                # Remove the temporary files (not needed anymore)
                # os.remove(temp_img_path)

            pdf.output(os.path.join(pdf_folder_path, "sheet_music.pdf"))
            messagebox.showinfo("Success", "PDF created successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.window.destroy()









if __name__ == "__main__":
    app = SheetMusicDownloader()
    app.run()

