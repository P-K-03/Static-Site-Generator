from htmlnode import *
from textnode import * 

def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):
    """Takes a list of "old nodes", a delimiter, and a text type. Returns a new list of nodes, 
        where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax."""