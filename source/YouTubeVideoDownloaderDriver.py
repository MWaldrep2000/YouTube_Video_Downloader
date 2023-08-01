"""
Contributor(s):
    Matthew Waldrep

Created Date:
    7/13/2023

Description:
    The objective of this file is to provide the main driving logic for a YouTube Video Downloader.
    The downloader will allow the user to download videos as either an MP3 or as an MP4.
    The currentr version of this utility will accept two command line arguments; one being the URL
    and the other being whether the user wants the video as an MP3 or MP4.
"""

    ##################
    # Module Imports #
    ##################

# Imported to log program progress
import logging

# Imported to join directory paths
import os

# Imported in order to acquire the home path
from pathlib import Path

# Imported to allow for API access to downloading YouTube videos
from pytube import YouTube

# Imported for GUI functionality
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

    ####################
    # Module Constants #
    ####################

# Specifies the valid file types
FILE_TYPES = ('mp3', 'mp4')

# Specify GUI error constants
GUI_ERROR_URL_TITLE = "URL Error"
GUI_ERROR_URL_TEXT_EMPTY = "The URL is empty."
GUI_ERROR_URL_TEXT_INVALID = "The URL is invalid."

GUI_ERROR_AGE_TITLE = "Age Restriction Error"
GUI_ERROR_AGE_TEXT = "The video is age restricted."

GUI_INFO_SUCCESS_TITLE = "Download Successful"
GUI_INFO_SUCCESS_TEXT = "The content was successfully downloaded."

# Specify GUI label constnats
GUI_LABEL_ENTRY = "YouTube URL:"
GUI_LABEL_MP3 = "mp3"
GUI_LABEL_MP4 = "mp4"

# Specify GUI window title
GUI_WINDOW_TITLE = "YouTube Video Downloader"

    ####################
    # Module Functions #
    ####################

# Name:
    # createGUI()
# Description:
    # Creates the GUI for this application
# Parameters:
    # Takes no parameters
# Outputs:
    # True = successful execution
    # False = failed execution
def createGUI():
    
    # Indicate that we are creating the GUI
    logging.info(msg = "Creating GUI.")
    
    # Create an instance of the Tk runtime
    root = tk.Tk()

    # Name the window title
    root.title(GUI_WINDOW_TITLE)

    # Specify window size
    root.resizable(width=0, height=0)

    # Create a frame
    mainframe = ttk.Frame(master = root, padding = "12 12 12 12")

    # Create a grid to align the components
    mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # Create a label for the entry box
    ttk.Label(master = mainframe, text = GUI_LABEL_ENTRY).grid(column = 0, row = 0, sticky = (tk.W, tk.E))

    # Create the URL entry box
    url = tk.StringVar()
    ttk.Entry(master = mainframe, width = 48, textvariable = url).grid(column = 1, row = 0, sticky = (tk.W, tk.E))

    # Create the mp3 download button
    ret = tk.BooleanVar()
    ttk.Button(master = mainframe, command = lambda: downloadYouTubeVideo(url = url, fileType = FILE_TYPES[0], ret = ret), text = GUI_LABEL_MP3, width = 12).grid(column = 2, row = 0, sticky = (tk.W, tk.E))

    # Create the mp4 download button
    ttk.Button(master = mainframe, command = lambda: downloadYouTubeVideo(url = url, fileType = FILE_TYPES[1], ret = ret), text = GUI_LABEL_MP4, width = 12).grid(column = 3, row = 0, sticky = (tk.W, tk.E))

    # Initiate the GUI thread
    root.mainloop()

    logging.info(msg = "GUI creation finished.")
    
    return True

# Name:
    # downloadYouTubeVideo
# Description:
    # Downloads a YouTube video from a given URL
# Parameters:
    # url = the url to download from
    # fileType = the file type to download as
    # ret = the return value to store
# Outputs:
    # Returns True on successful execution
    # Returns False of failed execution
def downloadYouTubeVideo(url = None, fileType = None, ret = None):

    # Instantiate a YouTube object with the URL
    try:
        logging.info(msg = "Attempting to access URL.")
        yt = YouTube(url = url.get(), use_oauth = True)

    # If we are unable to access the URL, set yt to None
    except Exception as e:
        logging.warning(msg = "Unable to access YouTube URL of " + url.get())
        logging.exception(msg = e)
        yt = None

    # Print success message and title if the video was successful; otherwise, dispaly an error box and return
    finally:
        if yt is not None:
            logging.info(msg = "URL access successful. Video has been found.")
            logging.info(msg = "The video's title is " + yt.title)
        else:
            logging.error(msg = "The YouTube link could not be accessed.")
            messagebox.showerror(title = GUI_ERROR_URL_TITLE, message = GUI_ERROR_URL_TEXT_EMPTY if url.get() == "" else GUI_ERROR_URL_TEXT_INVALID)
            ret.set(False)
            return
        
    # Filter the streams for audio files; use a try-except block for age restriction
    try:
        if (fileType == "mp3"):
            logging.info(msg = "Accessing highest quality audio stream.")
            stream = yt.streams.get_audio_only()
        # Filter the streams for video files
        else:
            logging.info(msg = "Accessing highest quality video stream.")
            stream = yt.streams.get_highest_resolution()
    # Fail on age restriction
    # TODO: Figure out a way around the age restriction
    except:
        logging.error(msg = "The YouTube video is age restricted and cannot be downloaded.")
        messagebox.showerror(title = GUI_ERROR_AGE_TITLE, message = GUI_ERROR_AGE_TEXT)
        ret.set(False)
        return
    
    # Log the stream data
    logging.info("Stream data is " + str(stream))

    # Download the stream
    logging.info(msg = "Starting download of stream at " + url.get())
    outFile = stream.download(output_path = os.path.join(Path.home(), 'Downloads'))
    logging.info(msg = "Finished download of stream at " + url.get())

    # Convert to mp3 if applicable
    if (fileType == "mp3"):
        logging.info(msg = "Saving file as .mp3 format.")
        base, ext = os.path.splitext(outFile)
        newFile = base + ".mp3"

        # If an mp3 file like it exists, overwrite
        if (os.path.isfile(newFile)):
            logging.warning(msg = "Overwriting file with identical name.")
            os.remove(newFile)

        os.rename(outFile, newFile)

    # Successful execution
    ret.set(True)
    messagebox.showinfo(title = GUI_INFO_SUCCESS_TITLE, message = GUI_INFO_SUCCESS_TEXT)
    return ret

    ###############
    # Module Main #
    ###############

# Name:
    # main()
# Description:
    # Drives the entire script; read the top level description for more
# Parameters
    # Takes no inputs
# Outputs
    # Returns nothing
def main():

    # Create the GUI with all of its logic
    createGUI()

# Set the logger properties
logging.basicConfig(filename='../logs/YouTubeVideoDownloader.log', filemode = 'w', encoding='utf-8', level = logging.INFO)

# Run the program
main()