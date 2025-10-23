from typing import Dict, List

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: List =  None, props: Dict = None):
        self.tag : str = tag
        self.value : str = value
        self.children : List= children
        self.props: Dict = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        html_string: str = " "  #initialized with space
        if self.props is None:
            return html_string
        
        for k,v in self.props.items():
            html_string  = html_string + f"{k}={v} "   # space at the end
        
        return html_string
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag},\nvalue: {self.value},\nchildren: {self.children},\nprops: {self.props})"
    