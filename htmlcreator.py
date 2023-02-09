from bs4 import BeautifulSoup
from PIL import Image
import shutil
import os
import sys
import time
import re
import unicodedata

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

def get_htm_files():
    dir_files = os.listdir()
    valid_files = []
    for file in dir_files:
        filename, file_extension = os.path.splitext(file)
        if (file_extension == '.htm' and os.path.isdir(filename + '_files')) or (file_extension == '.html' and os.path.isdir(filename +'.fld')):
            valid_files.append(file)

    return valid_files

def create_folder(title):
    folder_name = slugify(title)
    if os.path.isdir(folder_name):
        return False
    
    os.makedirs(os.path.join(folder_name, 'Images'))

    if os.path.isfile('eLearningStyle.css'):
        shutil.copy('eLearningStyle.css', folder_name)

    if os.path.isfile('giesorange.png'):
        shutil.copy('giesorange.png', os.path.join(folder_name, 'Images'))

    return folder_name

def write_tags_begining(html, title):
    html.write(
        '<!doctype html>\n'
        '<html lang=\"en\">\n'
        '<head>\n'
        '<meta charset=\"UTF-8\">\n'
        '<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes\">\n'
        f'<title>{title}</title>\n'
        '<script type=\"text/javascript\" async src=\"https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/latest.js?config=TeX-MML-AM_CHTML\"></script><link rel=\"stylesheet\" type=\"text/css\" href=\"eLearningStyle.css\">\n'
        '</head>\n'
        '<body>\n'
        '<div role=\"main\">\n'
        f'<h1>{title}</h1>\n')

def write_tags_ending(html):
    html.write(
        '</div>\n'
        '<script>\n'
        'var queried=[];\n'
        'document.body.innerText.match(/[A-Z]{2,}/g).forEach(function(a){if(!queried.includes(a))queried.push(a)});\n'
        'console.log(queried);\n'
        '</script>\n'
        '</body>\n'
        '</html>\n')

def write_toc(html, title, h2_and_h3):
    html.write(
        '<a href=\"#h2_1\">Skip the Table of Contents</a>\n'
        '<div id=\"toc_container\">\n'
        '<h2 class=\"toc_title\">Contents</h2>\n'
        '<div class=\"toc_list\">\n')

    formatted_headings = []
    module = 0
    title_split = unicodedata.normalize('NFC', title.replace(':', '')).split()
    if title_split[0].lower() == 'module' and title_split[1].isdigit():
        module = int(title_split[1])
    
    h2_href_level = 1
    h3_href_level = 1
    h2_level = 0
    h3_level = 0
    for level, heading in h2_and_h3:
        heading_split = unicodedata.normalize('NFC', heading).split()

        heading = ' '.join(heading_split)
        if level == 'h2':
            h2_level += 1
            h3_level = 0
            if h2_href_level >= 2:
                html.write('</ol>\n')

            if heading_split[0].lower() == 'lesson':
                lesson_num = heading_split[1].replace(':', '').split('-')
                if lesson_num[0].isdigit():
                    module = lesson_num[0]
                
                if lesson_num[1].replace(':', '').isdigit():
                    h2_level = int(lesson_num[1])
                
                heading = ' '.join(heading_split[2:])


            html.write(f'<h3><a href=\"#h2_{h2_href_level}\">Lesson {module}-{h2_level} {heading}</a></h3>\n<ol>\n')
            
            formatted_headings.append((h2_href_level, level, module, h2_level, h3_level, heading))
            h2_href_level += 1

        elif level == 'h3':
            h3_level += 1
            if heading_split[0].lower() == 'lesson':
                lesson_num = heading_split[1].replace(':', '').split('.')
                if lesson_num[1].isdigit():
                    h3_level = int(lesson_num[1])

                heading = ' '.join(heading_split[2:])

            html.write(f'<li><a href=\"#h3_{h3_href_level}\">Lesson {module}-{h2_level}.{h3_level} {heading}</a></li>\n')
            
            formatted_headings.append((h3_href_level, level, module, h2_level, h3_level, heading))
            h3_href_level += 1

    html.write('</ol>\n</div>\n</div>\n')

    return formatted_headings

def write_header(html, href_level, level, module, h2_level, h3_level, heading, url="INSERT"):
    if level == 'h2':
        html.write(f'<{level} id="{level}_{href_level}">Lesson {module}-{h2_level} {heading}</{level}>\n')
    elif level == 'h3':
        html.write(f'<{level} id="{level}_{href_level}">Lesson {module}-{h2_level}.{h3_level} {heading}</{level}>\n')
        html.write(f'<p><a href=\"{url}\" aria-label=\"Media Player for {heading}\" alt=\"Opens in a new window\" target=\"_blank\">Media Player for Video</a></p>\n')

def write_slide(html, slide_num, module, h2_level, h3_level):
    html.write(
        f'<div class="avoidPageBreak">\n'
        f'<h4>INSERT - Slide {slide_num}</h4>\n'
        f'<img src=\"Images/{module}-{h2_level}-{h3_level}_Slide{slide_num}.png\" width="450" height="250" alt="">\n'
        '</div>\n'
        '<div class="avoidPageBreak">\n'
        '<h5>Transcript</h5>\n')

def write_transcript(html, text, is_first_transcript):
    html.write(f'<p>{text}</p>\n')
    if is_first_transcript:
        html.write('</div>\n')

def write_transcript_empty(html):
    html.write('<p>No instruction provided</p></div>\n')

def image_converter(folder_name, img_path, module, h2_level, h3_level, slide_num):
    img_folder, img_file = img_path.replace('%20', ' ').split('/')
    img_extension = os.path.splitext(img_file)[1]
    new_image_folder = os.path.join(folder_name, "Images")
    new_image_name = f'{module}-{h2_level}-{h3_level}_Slide{slide_num}.png'
    if img_extension == '.png':
        shutil.copy(os.path.join(img_folder, img_file), new_image_folder)
        os.rename(os.path.join(new_image_folder, img_file), os.path.join(new_image_folder, new_image_name))
    else:
        image = Image.open(os.path.join(img_folder, img_file))
        image.save(os.path.join(new_image_folder, new_image_name))


# From https://gist.github.com/dmattera/ef11cb37c31d732f9e5d2347eea876c2
def soup_prettify2(soup, desired_indent): #where desired_indent is number of spaces as an int() 
	pretty_soup = str()
	previous_indent = 0
	for line in soup.prettify(formatter="html").split("\n"): # iterate over each line of a prettified soup
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


def pretty(file):
    data = open(file, encoding='utf-8').read()
    soup = BeautifulSoup(data, 'lxml')
    pretty = soup_prettify2(soup, desired_indent=4)
    h = open(file, "w", encoding='utf-8')
    h.write(pretty)
    h.close()


def html_creator(file):
    with open(file, 'r') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')

        title = soup.find('h1').text.strip()
        folder_name = create_folder(title)
        if folder_name == False:
            return False
        
        html = open(os.path.join(folder_name, f'{folder_name}.html'), "w", encoding='utf-8')
        write_tags_begining(html, title)
        h2_and_h3 = []
        for j in soup.find_all(['h2', 'h3']):
            if j.name == 'h2':
                h2_and_h3.append((j.name, j.text))
            elif j.name == 'h3':
                span = j.find('span')
                h2_and_h3.append((j.name, span.text))
        headings = write_toc(html, title, h2_and_h3)
        slide_num = 1
        is_first_transcript = False
        for element in soup.find_all(['h2', 'h3', 'p']):
            if element.has_attr('class') and element['class'][0].startswith('MsoToc'):
                continue

            if element.name == 'h2':
                href_level, level, module, h2_level, h3_level, heading = headings.pop(0)
                if level != element.name:
                    continue
                
                if is_first_transcript:
                    write_transcript_empty(html)
                    is_first_transcript = False

                write_header(html, href_level, level, module, h2_level, h3_level, heading)
            elif element.name == 'h3':
                href_level, level, module, h2_level, h3_level, heading = headings.pop(0)
                if level != element.name:
                    continue
                
                if is_first_transcript:
                    write_transcript_empty(html)
                    is_first_transcript = False

                href = element.find('a', href=True)
                # If hyperlinked video exists, add the url
                try:
                    write_header(html, href_level, level, module, h2_level, h3_level, heading, href['href'])
                except:
                    write_header(html, href_level, level, module, h2_level, h3_level, heading)

            elif element.name == 'p':
                # split image to fetch from either of the tags
                image = element.find('v:imagedata', src=True)
                if not image:
                    image = element.find('img', src=True)

                # was getting some extra tags in the transcript and headers
                text_elements = unicodedata.normalize('NFC', element.text).strip().split()
                text_elements = [x for x in text_elements if '<' not in x and '>' not in x]
                text = ' '.join(text_elements)

                if image:
                    image_converter(folder_name, image['src'], module, h2_level, h3_level, slide_num)
                    if is_first_transcript:
                        write_transcript_empty(html)

                    is_first_transcript = True
                    write_slide(html, slide_num, module, h2_level, h3_level)
                    slide_num += 1

                if text != '':
                    write_transcript(html, text, is_first_transcript)
                    is_first_transcript = False
                
        if is_first_transcript:
            write_transcript_empty(html)
        
        write_tags_ending(html)

    html.close()
    pretty(os.path.join(folder_name, f'{folder_name}.html'))

    return True

def main():
    print('Conversion in progress...')
    application_path = ''
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    os.chdir(application_path)
    htm_files = get_htm_files()
    for file in htm_files:
        begin_time = time.time()
        finished = html_creator(file)
        if not finished:
            print(f'{file} was not converted since folder already exists!')
        else:
            print(f'Finished {file} in {time.time() - begin_time} seconds!')

    input("Press enter to exit")

if __name__ == "__main__":
    main()
