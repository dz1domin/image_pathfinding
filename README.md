# Authors
- Dominik Dziuba - general idea and implementation of the algorithm, design of the GUI and necessary elements, leading the team
- Przemysław Rodzik - GUI, implementation of Dijkstra pathfinding algorithm
- Łukasz Wajda - GUI
- Mateusz Niepokój - test image generation
- Mariusz Biegański - creating windows and linux release
- Szymon Pawelec - documentation

# How to run
Go to our Release page and select the most suitable option for your system. You can find them under [this link](https://github.com/Dodzik/AiPO_project/releases/latest). Both the releases are created for python version 3.11 as well as the script itself has been tested with that version in mind. Older versions might also work but that has not been tested.
## Linux
Download *.tar.gz from Releases and run e.g. for newest linux 64 bit release
```
tar -xzf aipo_project_linux_64_v.1.0.0.tar.gz 
```
```
./aipo_project/main
```
## Windows
Download *.zip from Releases for your platform and unzip the folder, open aipo_project_windows folder, find main.exe and double click it to start the application.

## Python
If all else fails on a python-supported platform you can also simply download the interpreter and then the source code for the project. Run the following line to install necessary dependencies:
```
pip install -r requirements.txt
```
In the folder you have unpacked the source code in. And then simply launch the program like so:
```
python main.py
```
It is necessary that during the installation of the python interpreter, the tcl/tk additional package is also installed.

# How to use
1. Select an image
2. Change Minimum Pixel Weight(Optional)
3. Change Step Value(Optional)
4. Chose Path Color(Optional)
5. Change Custom Error(Optional)
6. Change Filter Size (Optional)
7. Change Path Width(Optional)
8. Select to points on the image you selected
9. Click Find Path and wait, the path will appear on the image, additionally you will get a popup window with path cost and average cost per pixel
