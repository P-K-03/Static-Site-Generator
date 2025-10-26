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


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[LeafNode], props: Dict = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("All parent nodes must have a tag")
        elif self.children is None:
            raise ValueError("All parent nodes should atleast have one child")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    

    

# node1 = LeafNode("a", "Link Text", {"href" : "https://www.example.com", "target" : "_blank"})
# node2 = LeafNode("p", "Some paragraph text", {"class" : "shadowbox"})
# node3 = ParentNode("div", [node1, node2], {"class" : "shadowbox"})
# print(node3.to_html())

# child_node_1 = LeafNode("code", 'fmt.println("Hello World")')
# child_node_2 = LeafNode("a", "https://www.example.com")
# child_node_3 = LeafNode("b", "Bold text")
# parent_node_1 = ParentNode("div", [child_node_1])
# parent_node_2 = ParentNode("caption", [child_node_2], {"align" : "bottom"})
# parent_node_3 = ParentNode("q", [child_node_3], {"class" : "crumbs"})
# grandparent_node_1 = ParentNode("div", [parent_node_1, parent_node_2, child_node_3], {"class" : "shadowbox"})
# grandparent_node_2 = ParentNode("p", [parent_node_2, parent_node_3], {"id" : "p01"})
                
# print(grandparent_node_1.to_html())
# print(grandparent_node_2.to_html())