from bs4 import BeautifulSoup
from PIL import Image
import argparse
import shutil
import os
import sys
import time

# From https://gist.github.com/dmattera/ef11cb37c31d732f9e5d2347eea876c2
def soup_prettify2(soup, desired_indent): #where desired_indent is number of spaces as an int() 
	pretty_soup = str()
	previous_indent = 0
	for line in soup.prettify().split("\n"): # iterate over each line of a prettified soup
		current_indent = str(line).find("<") # returns the index for the opening html tag '<' 
		# which is also represents the number of spaces in the lines indentation
		if current_indent == -1 or current_indent > previous_indent + 2:
			current_indent = previous_indent + 1
			# str.find() will equal -1 when no '<' is found. This means the line is some kind 
			# of text or script instead of an HTML element and should be treated as a child 
			# of the previous line. also, current_indent should never be more than previous + 1.	
		previous_indent = current_indent
		pretty_soup += write_new_line(line, current_indent, desired_indent)
	return pretty_soup

def write_new_line(line, current_indent, desired_indent):
	new_line = ""
	spaces_to_add = (current_indent * desired_indent) - current_indent
	if spaces_to_add > 0:
		for i in range(spaces_to_add):
			new_line += " "		
	new_line += str(line) + "\n"
	return new_line

def htmlcreator(path, old_file, new_file, module_level):
    # Starting
    slide_counter = 1
    h2_counter = 1
    h3_counter = 1
    h3_sub_counter = 1
    is_first_paragraph = False

    def write_basic_tags_begining(title):
        h.write(f"""<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"UTF-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes\">\n<title>{title}</title>\n<script type=\"text/javascript\" async src=\"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML\"></script><link rel=\"stylesheet\" type=\"text/css\" href=\"eLearningStyle.css\">\n</head>\n\n<body>\n<div role=\"main\">\n""")

    def write_basic_tags_ending():
        h.write('</div>\n<script>\nvar queried=[];\ndocument.body.innerText.match(/[A-Z]{2,}/g).forEach(function(a){if(!queried.includes(a))queried.push(a)});\nconsole.log(queried);\n</script>\n</body>\n</html>')

    def write_toc(h2_list, h3_list, order):
        toc_h2_counter = 0
        toc_h3_counter = 0
        toc_h3_sub_counter = 1
        h.write(f'<a href=\"#h2_1\">Skip the Table of Contents</a>\n<div id=\"toc_container\">\n<h2 class=\"toc_title\">Contents</h2>\n<div class=\"toc_list\">')
        for i in order:
            if i == 2:
                if toc_h2_counter > 0:
                    h.write('</ol>\n')
                h.write(f'<h3><a href=\"#h2_{toc_h2_counter + 1}\">{h2_list[toc_h2_counter]}</a></h3>\n<ol>\n')
                toc_h2_counter += 1
                toc_h3_sub_counter = 1
            if i == 3:
                h.write(f'<li><a href=\"#h3_{toc_h3_counter + 1}\">Lesson {module_level}-{toc_h2_counter}.{toc_h3_sub_counter} {h3_list[toc_h3_counter]}</a></li>\n')
                toc_h3_counter += 1
                toc_h3_sub_counter += 1

        if toc_h2_counter > 0:
            h.write('</ol>\n')

        h.write('</div>\n</div>\n\n')
        
    def write_h1(name):
        h.write(f'<h1>{name}</h1>\n')

    def write_h2(name):
        nonlocal h2_counter, h3_sub_counter
        if is_first_paragraph:
            write_transcript_empty()
        h.write(f'<h2 id="h2_{h2_counter}">{name}</h2>\n')
        h2_counter += 1
        h3_sub_counter = 1

    def write_h3(name, url="INSERT"):
        nonlocal h3_counter, h3_sub_counter, is_first_paragraph
        if is_first_paragraph:
            write_transcript_empty()
        h.write(f'<h3 id="h3_{h3_counter}">Lesson {module_level}-{h2_counter - 1}.{h3_sub_counter} {name}</h3>\n<p><a href=\"{url}\" aria-label=\"Media Player for {name}\" alt=\"Opens in a new window\" target=\"_blank\">Media Player for Video</a></p>\n')
        h3_counter += 1
        h3_sub_counter += 1

    def write_slide():
        nonlocal module_level, h2_counter, h3_sub_counter, slide_counter, is_first_paragraph
        if is_first_paragraph:
            write_transcript_empty()
        h.write(f'<div class="avoidPageBreak">\n<h4>INSERT - Slide {slide_counter}</h4>\n<img src=\"Images/{module_level}-{h2_counter - 1}-{h3_sub_counter - 1}_Slide{slide_counter}.png\" width="450" height="250" alt="">\n</div>\n')
        slide_counter += 1

    def write_transcript_begin():
        nonlocal is_first_paragraph
        h.write('<div class="avoidPageBreak">\n<h5>Transcript</h5>\n')
        is_first_paragraph = True
        
    def write_transcript(text):
        nonlocal is_first_paragraph
        h.write(f'<p>{text}</p>\n')
        if is_first_paragraph:
            h.write('</div>\n')
            is_first_paragraph = False

    def write_transcript_empty():
        nonlocal is_first_paragraph
        if is_first_paragraph:
            h.write('<p>No instruction provided</p></div>\n')
            is_first_paragraph = False

    # Renames the image and also converts to png is neccessary
    def image_rename(original_loc):
        nonlocal h2_counter, h3_sub_counter, slide_counter
        new_name = 'Images\\' + str(module_level) + '-' + str(h2_counter - 1) + '-' + str(h3_sub_counter - 1) + '_Slide' + str(slide_counter) + '.png'
        image = Image.open(os.path.join(path, original_loc.replace('%20', ' ')))
        image.save(os.path.join(path, new_name))
        return new_name

    def pretty(file):
        data = open(file).read()
        soup = BeautifulSoup(data, 'lxml')
        pretty = soup_prettify2(soup, desired_indent=4)
        h = open(file, "w")
        h.write(pretty)
        h.close()

    # Delete/create Image folder
    try:
        if os.path.isdir(f'{path}/Images'):
            shutil.rmtree(f'{path}/Images')
        os.mkdir(f'{path}/Images')
    except:
        print("Error in Image folder creation")
        sys.exit(1)

    # h for html :)
    h = open(new_file, "w")

    # For future use, consider implementing a tree structure if there's more than 1 sublevel
    with open(old_file, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

        # Create h1
        h1 = soup.h1.get_text().replace('\n',' ')
        write_basic_tags_begining(h1)
        write_h1(h1)

        h2 = []
        h3 = []
        heading_order = []

        # Create TOC
        for i in soup.find_all(['h2', 'h3']):
            if(str(i).startswith('<h2')):
                h2.append(i.get_text().strip().replace('\n',' '))
                heading_order.append(2)
            elif(str(i).startswith('<h3')):
                h3.append(i.get_text().strip().replace('\n',' '))
                heading_order.append(3)

        write_toc(h2, h3, heading_order)

        # Create rest of file
        for i in soup.find_all(['h2', 'h3', 'p']):
            # Ignore TOC elements
            try:
                if i['class'][0].startswith('MsoToc'):
                    continue
            except:
                pass

            # Potentially use re later, this gets rid of grammar and spelling tags from Word
            text = str(i)
            if(text.startswith('<h2')):
                write_h2(i.get_text().strip())
            elif(text.startswith('<h3')):
                href = i.find('a', href=True)
                # If hyperlinked video exists, add the url
                try:
                    write_h3(i.get_text().strip(), href['href'])
                except:
                    write_h3(i.get_text().strip())
            elif(text.startswith('<p')):
                image = i.find('v:imagedata', src=True)
                text = i.text.strip().replace('\n', ' ')
                if (image is not None):
                    image_rename(image['src'])
                    write_slide()
                    write_transcript_begin()
                    if text != '':
                        write_transcript(text)
                else:
                    if text != '':
                        write_transcript(text)
                        
    if is_first_paragraph:
        write_transcript_empty()
        
    write_basic_tags_ending()
    h.close()

    # Make pretty for humans :)
    pretty(new_file)

if __name__ == "__main__":
    # Arguments
    # -o Old file name
    # -n New file name
    # -m Module level (optional, default 1)
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--oldfile", help="Original HTML file")
    parser.add_argument("-n", "--newfile", help="New HTML file", required=False, default='text.html')
    parser.add_argument("-m", "--modulelevel", help="Module level", type=int, required=False, default='0')

    args = parser.parse_args()

    path = os.path.dirname(os.path.abspath(__file__))

    # Program time
    begin_time = time.time()
    htmlcreator(path, args.oldfile, args.newfile, args.modulelevel)
    print('Finished!')
    print(time.time() - begin_time)
