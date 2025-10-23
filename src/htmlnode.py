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
        prop_html: str = "" 
        if self.props is None:
            return prop_html
        
        for k,v in self.props.items():
            prop_html  += f" {k}={v}"   # space at the start of every property
        
        return prop_html
    
    def __repr__(self):
        return f"HTMLNode(tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: Dict = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag == None:
            # return the value as raw text
            return self.value
        else:
            # return the HTML string
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>" 
    
    def __repr__(self):
        return f"LeafNode(tag: {self.tag}, value: {self.value}, props: {self.props})"
