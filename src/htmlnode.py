from typing import Dict, List

class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: List =  None, props: Dict = None):
        self.tag : str = tag
        self.value : str = value
        self.children : List= children
        self.props: Dict = props

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        prop_html: str = " "  #initialized with space
        if self.props is None:
            return prop_html
        
        for k,v in self.props.items():
            prop_html  += f"{k}={v} "   # space at the end
        
        return prop_html
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag},\nvalue: {self.value},\nchildren: {self.children},\nprops: {self.props})"
    