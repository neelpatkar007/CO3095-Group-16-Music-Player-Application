# CO3095 Software Measurement and Quality Assurance - Group 16 Music Player Application

## Team Members:
- Neel Patkar
- Raiyan Alam 
- Sanil Panchal 
- Samuel Ameyaw

## About the Project:
A command-line music player application developed as part of the CO3095 Software Measurement and Quality Assurance module at the University of Leicester. 

### Project Structure:
- `music_player/`: Main package containing the source code for the music player application.
- Inside the `music_player` python package:
   - `main.py`: Entry point, command routing and main CLI loop.
   - `config.py`: global configuration constants.
   - `library.py`: Loads tracks from disk into the library, reads metadata.
   - `player_core.py`: Core playback functionality - play, pause, stop.
   - `player_audio.py`: Audio controls setting volume level and mute
   - `player_seek.py`: Seek backwards or forwards within a track to any time. 
  - `player_state.py`: Shared player state.
  - `player_queue.py`: Queue management - add, remove, next, previous.
  - `player_help.py`: Help commands.
  - `player_ui.py`: progress bar, list and other visual outputs.
  - `player_shortcuts.py`: Shortcut commands for core features.
  - `playlist_model.py`, `playlists_basic.py`, `playlists_edit.py`, `playlists_advanced.py`: Playlist features.
  - `player_metrics.py`: Likes and top tracks.
  - `player_config.py`: Persistent player settings and tagging.
  - `player_time.py`: Resume track state, scheduling alarms, recently added songs.
  - `player_io.py`: Import songs, export playlists and update metadata.
  - `user_data.py`: User profiles, advanced search, ratings.
  - `audio_backend.py`: Audio playback backend implementation using pygame or simulated without pygame.
  - `library_search_scan.py`: Library search and scanning.
  - `time_utils.py`: Time formatting utilities.
- `songs/`: Directory where audio files should be placed for playback.
- `ra495/`, `np343/`, `sp871/`, `sa1077/`: Directories that contains all of the testing files including:
  - Black-box Specification
  - Black-box Random
  - White-box Statement
  - White-box Branch
  - White-box Symbolic
  - White-box Concolic

## Prerequisites:
- Python 3.10.x installed on your system.
  - verify installation by running `python --version` or `python3 --version` in your terminal or command prompt.
- pip package manager installed.
  - verify installation by running `pip --version` in your terminal or command prompt.
- PyCharm IDE installed on your system.
  - Download link: https://www.jetbrains.com/pycharm/download/
- Source code downloaded as a zip file (CO3095-Group-16-Music-Player-Application-1.0.zip).
  - From the Blackboard submission.

## Uncompressing the Project:
- Extract the contents of the zip file to a desired location on your system using whatever extraction tool you prefer (Windows built in extraction, Winrar, 7-Zip, etc.). 
- At the location you extracted the zip file, you should see a folder named "CO3095-Group-16-Music-Player-Application-1.0".
- You have now successfully uncompressed the project.

## Importing the Project into PyCharm:
- Right click the uncompressed extracted folder "CO3095-Group-16-Music-Player-Application-1.0" and select "Open as PyCharm Project".
- Or, alternatively, open PyCharm, select "Open", and navigate to the location where you extracted the zip file and select the folder "CO3095-Group-16-Music-Player-Application-1.0".
- PyCharm will now load the project.
- Wait for PyCharm to finish indexing the project files.
- Once indexing is complete, you should see the project files in the "Project" pane on the left side of the PyCharm window.
- You have now successfully imported the project into PyCharm.

## Installing Dependencies (requirements.txt):
- Run the following command in the terminal to install most of the required dependencies:
    ```
    pip install -r requirements.txt
    ```
## Additional Dependency - ffmpeg:
- ffmpeg must be installed separately as it is cannot be installed via pip and instead must be installed directly on your system.
- Linux installation instructions:
  - On Linux Ubuntu run this command:
    ```
    sudo apt-get install ffmpeg
    ```
    - If this does not work download from https://ffmpeg.org/download.html and select the appropriate build for your distribution (Ubuntu).
    - Follow the instructions provided on the website for installation.
- Windows installation instructions:
  - Download the Windows build from https://ffmpeg.org/download.html
  - Extract the downloaded zip file to a location of your choice.
  - Add the `bin` folder inside the extracted folder to your system's PATH environment variable.
    - For example, if you extracted ffmpeg to `C:\ffmpeg`, add `C:\ffmpeg\bin` to your PATH.
  - To verify the installation, open a new command prompt and run:
    ```
    ffmpeg -version
    ```
  - If the installation was successful, you should see the version information for ffmpeg displayed in the terminal.
  - You have now successfully installed ffmpeg.

## How to Run the Application:
- Once you have installed all the dependencies, you can run the music player application.
- In PyCharm, open the `music_player` python package project folder. Inside should be a file named `main.py`.
- Right-click on `main.py` and select "Run 'main'".
- The application should start running in the terminal within PyCharm.
- Follow the on-screen instructions to use the music player application.

### Key Commands:
- 

## Adding Audio Files:
- The application does not include any audio files by default.
- If you want to test the application with audio files, you will need to add your own audio files to the `songs` directory located inside the project folder `music_player`.
- Currently supported audio formats are mp3, wav, flac, m4a and ogg.
