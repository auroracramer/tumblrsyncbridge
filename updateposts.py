"""

Filename: updateposts.py
Author: Jason Cramer

A bridge between tumblr and jasontcramer.com to update the
local xml listing of blog posts from tumblr.

"""

import urllib.request as URL
from sys import exit
from xml.etree import ElementTree as ET
from json import JSONDecoder 

# CONSTANTS

SITEUPDATES = '/home/admin/public_html/blog/posts/siteupdates.xml'
DEVUPDATES = '/home/admin/public_html/blog/posts/devupdates.xml'

BASEHOSTNAME = ''
APIKEY =''

postsets = [SITEUPDATES, DEVUPDATES]
tags_dict = {'siteupdates':'siteupdates',
 'devupdates':'devupdates'}

def get_filename(post_file):
    return post_file.name.split(r'/')[-1][-4]

def get_etree(post_file):
    return ET.ElementTree(ET.fromstring(post_file.read()))

def save_etree(etree, xmlfile):
    xmlfile.seek(0)
    etree.write(xmlfile,"utf-8", True)

def get_posts_uri(tag, limit=20, type = ''):
    """ Returns the URI that returns JSON file with posts of a certain tag"""
    if type:
        type = r'/' + type
    limit = str(limit)
    tag = tag.replace(' ', '+')
    return 'http://api.tumblr.com/v2/blog/' + BASEHOSTNAME + '/posts' + type + '?api_key=' + APIKEY + '&limit=' + limit

def init_posts(post_filenames):
    """ Initializes XML post files if they do not exist already."""
    result = []
    for f in post_filenames:
        try:
            with open(f): pass 
        except:
            init_post(f)
        finally:
            result.append(init_post(open(f, 'r+b')))
    return result

def init_post(post_filename):
    """ Initializes a single XML post file. """
    with open(post_filename, 'r+') as post_file:
        root = ET.Element('postset')
        root.attrib['blogname'] = get_filename(post_file)
        root.attrib['tags'] = tags_dict[root.attrib['blogname']]
        ET.write(post_file, 'UTF-8', True)

def generate_post(etree):
    """ Adds a post child to the root level node and returns it. """
    post = ET.Element('post')
    etree.getroot().insert(0, post)
    return post

def make_child(element, tag):
    return ET.SubElement(element, tag)

def add_full_child(element, tag, text):
    make_child(element, tag).text = text

def open_post_files():
    """ Opens the XML post files for writing and returns them
        as a list. If the files do not exist, creates and
        initializes them before returning them. """
    return init_posts(postsets)    

def get_text_post(post, post_element):
    add_full_child(post_element, 'title', post['title'])
    add_full_child(post_element, 'body', post['body'])

def get_photo_post(post, post_element):
    for photo in post["photos"]:
        caption = photo["caption"]
        for size in photo["alt_sizes"]:
            width = size["width"]
            height = size["height"]
            url = size["url"]
    


def get_video_post(post, post_element):
    pass

def get_quote_post(post, post_element):
    text = post["text"]
    source = post["source"]

def get_link_post(post, post_element):
    title = post["title"]
    url = post[""]

def get_chat_post(post, post_element):
    pass

def get_audio_post(post, post_element):
    pass



def add_post_element(post, etree):
    """ Returns the ElementTree element representing a post."""
    attrs = {"href" : post["post_url"], "type" : post["type"], "date" : post["date"]}
    post_element = generate_post(etree)
    for attr in attrs.items():
        add_full_child(post_element, attr[0], attr[1])

    post_type = attrs["type"]

    if post_type == "text":
        get_text_post(post, post_element)
    elif post_type == "photo":
        get_photo_post(post, post_element)
    elif post_type == "video":
        get_video_post(post, post_element)
    elif post_type == "quote":
        get_quote_post(post, post_element)
    elif post_type == "link":
        get_link_post(post, post_element)
    elif post_type == "chat":
        get_chat_post(post, post_element)
    elif post_type == "audio":
        get_audio_post(post_element)
    
def update_posts(post_file):
    """ Updates the post set. """
    try:
        # Get the URL and request the json
        with URL.urlopen(get_posts_uri(tags_dict[get_filename(post_file)])) as uri:
            rawjson = uri.read().decode() # Returned in encoded byte format, so we must DECODE

            post_tree = get_etree(post_file)

            # Decode json to python objects
            new_posts = JSONDecoder().decode(rawjson)["response"]["posts"]

            for post in new_posts:
                get_post_element(post, etree)
            save_etree(post_tree, post_file)
    except:
        pass
    finally:
        post_file.close()

def main():
    """ Main file function """
    for post_file in open_post_files():
        update_posts(post_file)


if __name__ == '__main__':
    sys.exit(main())
