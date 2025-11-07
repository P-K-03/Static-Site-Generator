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

def split_nodes_image(old_nodes: List[TextNode]):
    """"""
    resultant_nodes: List = []
    for node in old_nodes:
        images: List = extract_markdown_images(node.text)
        if len(images) == 0:
            resultant_nodes.append(node)
        else:
            unprocessed_node: str = node.text
            for x in images:
                # x[0] has alt text and x[1] has the image URL
                # split the node based on the extracted image, one image at a time
                sub_nodes: List = unprocessed_node.split(f"![{x[0]}]({x[1]})", 1)

                # The list will have 2 elements, element 0 - text before the image, element 1 - text after the element. 
                # Element 0 will either be some text or empty. element 2 can contain more images. process it in the next iteration
                unprocessed_node = sub_nodes[-1]

                # if the element is empty, don't create a TextNode
                if sub_nodes[0]:
                # First add the Text as a TextNode and then add the image as the TextNode
                    resultant_nodes.append(TextNode(sub_nodes[0], TextType.TEXT))
                resultant_nodes.append(TextNode(x[0], TextType.IMAGE, x[1]))

                # print(f"{x}, {sub_nodes}")

            # Unprocessed node could still have some text but not images. In that case, convert it into a TextNode
            if unprocessed_node:
              resultant_nodes.append(TextNode(unprocessed_node, TextType.TEXT))  

    return resultant_nodes

def split_nodes_link(old_nodes: List[TextNode]):
    """"""
    resultant_nodes: List = []
    for node in old_nodes:
        links: List = extract_markdown_links(node.text)
        if len(links) == 0:
            resultant_nodes.append(node)
        else:
            unprocessed_node: str = node.text
            for x in links:
                # x[0] has the title and x[1] has the link URL
                # split the node based on the extracted link, one link at a time
                sub_nodes: List = unprocessed_node.split(f"[{x[0]}]({x[1]})", 1)

                # The list will have 2 elements, element 0 - text before the link, element 1 - text after the element. 
                # Element 0 will either be some text or empty. element 2 can contain more links. Process it in the next iteration
                unprocessed_node = sub_nodes[-1]

                # if the element is empty, don't create a TextNode
                if sub_nodes[0]:
                # First add the Text as a TextNode and then add the link as the TextNode
                    resultant_nodes.append(TextNode(sub_nodes[0], TextType.TEXT))
                resultant_nodes.append(TextNode(x[0], TextType.LINK, x[1]))
                
                # print(f"{x}, {sub_nodes}")

            # Unprocessed node could still have some text but not links. In that case, convert it into a TextNode
            if unprocessed_node:
              resultant_nodes.append(TextNode(unprocessed_node, TextType.TEXT)) 

    return resultant_nodes

def text_to_textnodes(text: str) -> List[TextNode]:
    node = TextNode(text, TextType.TEXT)
    
    # The order in which these functions are called doesn't matter
    new_nodes: List[TextNode] = []
    new_nodes = split_nodes_link([node])
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD)
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC)

    return new_nodes

# print(extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"))
# print(extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"))


# This doesn't work because the regex for image doesnt recognise the image link correctly
# markdown_string: str = """Ben was an ordinary 10-year-old boy until he found the Omnitrix, a powerful watch-like device that allowed him to turn into 10 different aliens.
# ![Ben Tennyson](https://ben10.fandom.com/wiki/Ben_Tennyson_(Classic)).
# Ben's most powerful alien is Alien X, a Celestial Sapien. This article redirects to [Alien X](https://ben10.fandom.com/wiki/Alien_X_(Classic))."""

# output_image = extract_markdown_images(markdown_string)
# output_link = extract_markdown_links(markdown_string)
# print(output_image)
# print(output_link)

# print(split_nodes_image([TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif), another pic - ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and this one too: ![THE DOCTOR](https://www.rollingstone.com/wp-content/uploads/2018/06/pc1-3eeaf1a0-8577-4352-884c-dc0ec0919d51.jpg?w=1581&h=1054&crop=1)", TextType.TEXT]))
# print(split_nodes_link(["This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"]))
# print(split_nodes_image([TextNode("Image 1: ![Batman](https://media.tenor.com/j8m4rwG-sFkAAAAm/batman.webp), Image 2: ![Batmobile](https://tinyurl.com/4cjh9y8s) and the final image, Image 3: ![Batwing](https://tinyurl.com/msyzfk28). Some Text.", TextType.TEXT)]))
# print(split_nodes_link([TextNode("The links present in the navbar are as follows: [Home](https://www.tomarkdown.org/en), [Calculator](https://www.calculatoronline.io/), [Compressor](https://www.compress.run/), [Markdown Syntax Guide](https://www.tomarkdown.org/en/guides/markdown-syntax)", TextType.TEXT)]))

# print(text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"))
