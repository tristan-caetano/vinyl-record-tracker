# vinyl-record-tracker
A small program with a GUI that will allow me to input my collection of vinyl records into an SQL database.

## Running Instructions
**PLEASE KEEP IN MIND THESE ARE LINUX INSTRUCTIONS, HOWEVER, THIS PROGRAM SHOULD ALSO RUN IN ANY OS**

I tried to make this program as flexible as possible by creating both a GUI and Terminal based program.
The GUI currently uses pysimplegui and may require you to go to the website and sign up for a hobbyist license which should be free.

However, both versions of the program currently require Spotify API keys. You can sign up to get keys on the [Spotify Developer Website](https://developer.spotify.com/).
Once you get the keys, create a file named **spotify_api_info.csv**. The file should be formatted like the following.

|clientid    |clientsecret|
|------------|------------|
|(*CLIENTKEY*)|(*SECRETKEY*)|

Python is also required for this program to work, and the required packages can be found in **packages.md**. These packages are currently organized to be installed in Arch, however all of these packages should be installable regardless of OS.

There is an option to run this program inside of a docker container, however this is only available for the terminal based application.

## How to run the GUI program
The Vinyl Tracker GUI is very simple to run with this command:
`python3 record_gui.py`

This will open a window for pysimplegui to display the program. This is where pysimplegui may ask you to sign up for a license, or use a 30 day free trial.

## How to run the Terminal based program
### Natively:
Simply run: `python3 record_term.py`

### In a Docker Container:
Firstly, you need to install docker, its usually as simple as installing the package. [Click here](https://docs.docker.com/engine/install/) to be sent to the docker install instructions.

Once you install docker, you need to start the daemon: 
`sudo systemctl start docker.service`

Then, build the container:
`sudo docker build -t vinyl_tracker .`

Finally, run the container with terminal interactivity (-ti):
`sudo docker run -ti vinyl_tracker`

END
