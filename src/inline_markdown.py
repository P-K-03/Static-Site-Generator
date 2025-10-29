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
                if sub_nodes[i] != "":
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


# node = TextNode("**How to Train Your Dragon** is a 2025 American fantasy adventure film", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
# print(new_nodes)

# node = TextNode("Nico Parker played Sarah Miller in the first season of the HBO series _The Last of Us_", TextType.TEXT)
# new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
# print(new_nodes)