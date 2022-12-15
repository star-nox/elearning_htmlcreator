# HTML Creator
Turns Word files into skeleton HTML files with the correct formatting.

## Purpose
The main purpose of this project is so people not familiar with HTML can turn Word video transcript files into HTML files with relative ease. The script creates skeleton code that can be utilized by the user to add more detailed information afterward.

## Download
** Note that the Python version is the *UPDATED VERSION* which handles all the transcript issues (missing images, file not generated, etc.) ** 

If using the Python version, you can download the files from above as a zip file.

** Executable version is the *OLDER VERSION* **

Executable versions of the script can be downloaded below. These executable versions have larger file sizes, however they can be run without downloading any prerequisites.
- Windows (15.2 MB): [htmlcreator_WIN.zip](https://uofi.box.com/shared/static/uhyobtu6ty9d63jauyqh8y4dssnpgi4m.zip)
- Mac (14.5 MB): [htmlcreator_MAC.zip](https://uofi.box.com/shared/static/ii826fh1fyk4dzu19swvf2jk9nxyxg6b.zip)

## Prerequisites (Python)
Make sure you have Python 3 installed. The most recent version can be found at [Python's download page](https://www.python.org/downloads/).

If you download the requirements.txt, in the same folder, you can run:
```pip install -r requirements.txt```

Else, you can install the packages individually:
- BeautifulSoup used for parsing
```pip install beautifulsoup4```
- lxml also used for parsing
```pip install lxml```
- Pillow used for converting images to .png
```pip install Pillow```

## Instructions
1. In the transcript Word document, save the document as a Web Page (*htm, *html). Make sure you DON'T save it as a filtered web page or other similar file type or else the script will not work.
2. A .htm/.html file and a folder of the same name should be saved. Move the file and folder to the same location where the script is. Do not rename the files after they are saved.
3. If you are using the python version, run the python script. You can run it by clicking on it and running with python or running ```python3 htmlcreator.py``` in the folder with CMD/Terminal. If you are using the executable version, click on the application, if there are warnings, dismiss them. If you are on Mac, you may need to allow unknown authors for the application.
4. A folder will appear with the module level and name of the HTML. If the folder was already created, the script will not create another folder.

## Notes
- If multiple .htm/.html files are in the folder during execution, the script will convert all valid files.
- If the eLearning CSS file and/or the Gies logo is in the same folder as the script, the script will automatically copy them into the folder.
