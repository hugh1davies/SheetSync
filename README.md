# 🎵 Sheet Music Downloader 🎶

![sheet_music_downloader_logo (1)](https://github.com/hugh1davies/SheetSync/assets/78705624/41bacb54-dccb-4041-8c54-736d18b2c840)


An intuitive Python application for downloading and compiling sheet music from YouTube videos or local MP4 files into a convenient PDF document. Available both as a Python script and an executable file for easy usage.

## Features

✨ **User-Friendly Interface**: Enjoy a sleek and easy-to-navigate GUI built with Tkinter.

📹 **Source Selection**: Choose between YouTube or local MP4 files as your source.

🔗 **Link Validation**: Automatically validate YouTube links and local file paths.

🎨 **Frame Selection**: Preview frames and select the ones you want to include in the PDF.

📄 **PDF Customization**: Specify the number of images per page and choose between portrait or landscape orientation.

🚀 **AI Upscaling**: Optionally upscale images using AI for enhanced quality.

🔍 **Enlarged Image**: View enlarged versions of images with a simple right-click.

🔑 **Shortcut Support**: Select all images with a quick Ctrl + A shortcut.

⚠️ **Warning System**: Receive warnings for potentially resource-intensive tasks.

## Usage

### Python Script

1. **Install Python**: If you haven't already, install Python on your system.
2. **Download Source Code**: Clone or download the source code of this project.
3. **Run the Application**: Execute the `sheetsync.py` script:
    ```
    python sheetsync.py
    ```
4. Follow the on-screen instructions to use the application (It may take a while when launching for the first-time).

### Executable File

1. **Download Executable**: Download the executable file for your operating system.
2. **Run the Application**: Double-click the executable file to launch the application.
3. Follow the on-screen instructions to use the application.


## How to Use 

### 1️⃣ Program Interface:


Upon running the program, a graphical user interface (GUI) will appear. Here's how to use the different components of the interface:

- ⚙️ **Source Type:** Select the source type (YouTube or local MP4) from the radio buttons.
- 🔗 **YouTube Link or MP4 File Path:** Enter the YouTube video link or local MP4 file path in the respective entry field.
- 🖼️ **Number of Images per Page:** Specify the number of sheet music images to display per page in the PDF.
- 📏 **PDF Orientation:** Choose the orientation of the PDF (portrait or landscape) using the radio buttons.
- 🔄 **AI Upscaler:** Enable or disable AI upscaling for the sheet music images using the radio buttons.
- 📄 **Include Title Page:** Check this box to include a title page in the PDF.
- 📥 **Download Button:** Click this button to download the sheet music and proceed to the image selection phase.
- 🖼️ **Image Selection:** After downloading the sheet music, a new window will appear displaying the extracted sheet music images. You can select/deselect images by clicking on them. Use Ctrl + A to select all images or press Backspace to delete the last selected image.
- 📄 **Create PDF Button:** Once you've selected the desired images, click this button to generate the PDF containing the selected sheet music images.

### 2️⃣ Output:

The program will create a folder named `pdf` inside the selected folder (where the downloaded images are stored). Inside the `pdf` folder, you'll find the generated PDF file named `sheet_music.pdf`.


## Dependencies

If running the Python script:
- `cv2`
- `numpy`
- `math`
- `fpdf`
- `pytube`
- `tkinter`
- `PIL`
- `super_image`
- `tqdm`
- `BeautifulSoup4`
- `yt_dlp`

## Acknowledgments

Special thanks to the developers of the libraries used in this project for their contributions.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

