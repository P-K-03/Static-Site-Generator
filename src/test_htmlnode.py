import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_node_props_tohtml(self):
        # node = HTMLNode()
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

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_2(self):
        child_node_1 = LeafNode("b", "Bold text")
        child_node_2 = LeafNode(None, "Normal text")
        child_node_3 = LeafNode("i", "italic text")
        child_node_4 = LeafNode(None, "Normal text")
        node = ParentNode("p", [child_node_1, child_node_2, child_node_3, child_node_4])
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_without_children(self):
        parent_node = ParentNode("div", [], {"class" : "shadowbox"})
        self.assertEqual(parent_node.to_html(), "<div class=shadowbox></div>")

    def test_to_html_nested_parents(self):
        child_node_1 = LeafNode("code", 'fmt.println("Hello World")')
        child_node_2 = LeafNode("a", "https://www.example.com")
        child_node_3 = LeafNode("b", "Bold text")
        parent_node_1 = ParentNode("div", [child_node_1])
        parent_node_2 = ParentNode("caption", [child_node_2], {"align" : "bottom"})
        parent_node_3 = ParentNode("q", [child_node_3], {"class" : "crumbs"})
        grandparent_node_1 = ParentNode("div", [parent_node_1, parent_node_2, child_node_3], {"class" : "shadowbox"})
        grandparent_node_2 = ParentNode("p", [parent_node_2, parent_node_3], {"id" : "p01"})
        self.assertEqual(grandparent_node_1.to_html(), '<div class=shadowbox><div><code>fmt.println("Hello World")</code></div><caption align=bottom><a>https://www.example.com</a></caption><b>Bold text</b></div>')
        self.assertEqual(grandparent_node_2.to_html(), '<p id=p01><caption align=bottom><a>https://www.example.com</a></caption><q class=crumbs><b>Bold text</b></q></p>') 

if __name__ == "__main__":
    unittest.main()