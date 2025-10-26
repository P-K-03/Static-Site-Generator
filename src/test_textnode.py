import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq_true(self):
        node = TextNode("Bird", TextType.IMAGE, "https://www.example.com/imgs/15")
        node2 = TextNode("Bird", TextType.IMAGE, "https://www.example.com/imgs/15")
        self.assertEqual(node, node2)
    
    def test_text_noteq(self):
        node = TextNode("Text3", TextType.CODE, "https://www.example.com")
        node2 = TextNode("Text4", TextType.CODE, "https://www.example.com")
        self.assertNotEqual(node, node2)

    def text_text_type_noteq(self):
        node = TextNode("Text3", TextType.CODE, "https://www.example.com")
        node2 = TextNode("Text3", TextType.ITALIC, "https://www.example.com")
        self.assertNotEqual(node, node2)

    def test_url_noteq(self):
        node = TextNode("John", TextType.ITALIC, "/home/usr/name/")
        node2 = TextNode("John", TextType.ITALIC, "/usr/bin/name/")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.example.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.example.dev)", repr(node)
        )

    def test_text_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_text_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_link(self):
        node = TextNode("This is an anchor node", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is an anchor node")
        self.assertEqual(html_node.props, {"href":"https://www.example.com"})


    def test_text_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "~/pictures/birds/bird01.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"alt": "This is an image node", "src" : "~/pictures/birds/bird01.jpg"})

    

if __name__ == "__main__":
    unittest.main()