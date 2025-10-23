import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_node_props_tohtml(self):
        node = HTMLNode()
        node2 = HTMLNode()
        self.assertEqual(node2.props_to_html(), "")

    def test_full_node_props_tohtml(self):
        node = HTMLNode("p", "This is a paragraph", ['a', 'a'], {"class" : "flex", "id" : "p01", "lang" : "en"})
        node2 = HTMLNode("p", "This is a paragraph", ['a', 'a'], {"class" : "flex", "id" : "p01", "lang" : "en"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
    
    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def text_repr(self):
        node = HTMLNode("p", "This is a paragraph", ['a', 'a'], {"class" : "flex", "id" : "p01", "lang" : "en"})
        self.assertEqual(node.__repr__(),"HTMLNode(tag: p, value: This is a paragraph, children: ['a', 'a'], props: {'class': 'flex', 'id': 'p01', 'lang': 'en'})")
        
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    

    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_no_value_to_html(self):
        node = LeafNode("p", None, {"id" : "K01"})
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_2(self):
        node1 = LeafNode("a", "Link Text", {"href" : "https://www.example.com", "target" : "_blank"})
        node2 = LeafNode("a", "Link Text", {"href" : "https://www.example.com", "target" : "_blank"})
        self.assertEqual(node1.to_html(), node2.to_html())

    def test_leaf_repr(self):
        node = LeafNode("p", "Some paragraph text", {"class" : "shadowbox"})
        self.assertEqual(node.__repr__(),"LeafNode(tag: p, value: Some paragraph text, props: {'class': 'shadowbox'})")

if __name__ == "__main__":
    unittest.main()