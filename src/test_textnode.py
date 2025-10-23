import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
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




if __name__ == "__main__":
    unittest.main()