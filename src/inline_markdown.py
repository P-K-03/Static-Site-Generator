import re

from typing import List, Dict
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType) -> List[TextNode]:
    """It takes a list of "old nodes", a delimiter, and a text type. It should return a new list of nodes, 
    where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax. 
    """
    DELIMITERS: Dict = {"bold" : "**", "code": "`", "italic" : "_"}
    resultant_nodes: List = []
    
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            resultant_nodes.append(node)
        else:
            sub_nodes: List = node.text.split(delimiter)
            
            # If there aren't even no. of delimiters/odd no. of elements in the list, something is wrong
            if len(sub_nodes) % 2 != 1:
                raise Exception(f"Error: Delimiter {delimiter} not closed")
            
            for i in range(0,len(sub_nodes)):

                # If the element is empty, don't create a textnode 
                if sub_nodes[i] == "":
                    continue

                # Elements at the odd indexes will be between the delimiters
                elif i%2 == 1:
                    if delimiter == DELIMITERS['bold']:
                        resultant_nodes.append(TextNode(sub_nodes[i], TextType.BOLD))
                    elif delimiter == DELIMITERS['code']:
                        resultant_nodes.append(TextNode(sub_nodes[i], TextType.CODE))
                    elif delimiter == DELIMITERS['italic']:
                        resultant_nodes.append(TextNode(sub_nodes[i], TextType.ITALIC))
                    else:
                        raise Exception(f"Invalid delimiter encountered in Markdown: {delimiter}")
                else:
                    resultant_nodes.append(TextNode(sub_nodes[i], TextType.TEXT))

    return resultant_nodes   

def extract_markdown_images(text: str):
    """Takes raw markdown text and returns a list of tuples. Each tuple contains the alt text and the URL of any markdown images"""
    markdown_image_regex: str = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches: List = re.findall(markdown_image_regex, text)
    return matches

def extract_markdown_links(text: str):
    """Extracts markdown links from the text. Returns tuples of anchor text and URLs"""
    markdown_link_regex: str = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches: List = re.findall(markdown_link_regex, text)
    return matches

# print(extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"))
# print(extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"))


# This doesn't work
# markdown_string: str = """Ben was an ordinary 10-year-old boy until he found the Omnitrix, a powerful watch-like device that allowed him to turn into 10 different aliens.
# ![Ben Tennyson](https://ben10.fandom.com/wiki/Ben_Tennyson_(Classic)).
# Ben's most powerful alien is Alien X, a Celestial Sapien. This article redirects to [Alien X](https://ben10.fandom.com/wiki/Alien_X_(Classic))."""

# output_image = extract_markdown_images(markdown_string)
# output_link = extract_markdown_links(markdown_string)
# print(output_image)
# print(output_link)