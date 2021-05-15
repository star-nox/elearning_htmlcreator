# HTML Creator
Turns Word HTML files into formatted HTML files for efficiency. 
## Purpose
The main purpose of this project is so people not familiar with HTML can turn Word video transcript files into HTML files with relative ease. The script creates skeleton code that can be utilized by the user to add more detailed information afterward.

## Prerequisites
- BeautifulSoup used for parsing
```pip install bs4```
- lxml also used for parsing
```pip install lxml```
- Pillow used for converting images to .png
```pip install Pillow```


## Instructions
As of now, some exceptions aren't handled, so having the correct format for a Word document is crucial. 
1. In the transcript Word document, save the document as a Web Page (*htm, *html). We DON'T want to save it as a filtered web page since there were issues with seeing the correct text when converting.
2. A .htm file and a folder of the same name should be saved. Move them to the same folder which the Python script is.
3. Open the current folder in cmd or terminal.
4. You can run the program with the following flags:
    - -o Name of saved .htm file
    - -n Name of new .html file (the one you want to be creating)
    - -m Module level (optional, default is 1)

```htmlcreator.py -o "MBA 548 MOOC 1 Module 1.htm" -n "MBA 548 MOOC 1 Module 1.html" -m 1 -p```
This would take the transcript named "MBA 548 MOOC 1 Module 1.htm" and create a new "MBA 548 MOOC 1 Module 1.html" with an Images folder. -m signifies that this is module 1 and the -p will make the resulting HTML file formatted (somewhat). Remember to include the .htm and .html extensions.

Video Tutorial:

[![Video Tutorial](https://img.youtube.com/vi/uOSD2idum08/0.jpg)](https://www.youtube.com/watch?v=uOSD2idum08)

## Notes
If there is already an "Images" folder in the same folder as the program, the program will fail to run. You will need to remove the "Images" folder or move it elsewhere.
This program may take a while to run and will crash if there are issues with the transcript files. Hopefully, I can resolve those but in the meantime, I think this will work.
Also, things like slide information and slide names will need to be replaced later on. I have labeledd places that need manual correction with "INSERT," so you can just find those in the HTML file later on.
