from typing import List
import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):

    def test_code_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(new_nodes,[TextNode("This is text with a ", TextType.TEXT, None), 
        TextNode("code block", TextType.CODE, None), TextNode(" word", TextType.TEXT, None)] )

    def test_bold_delimiter(self):
        node = TextNode("**How to Train Your Dragon** is a 2025 American fantasy adventure film", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(new_nodes, [TextNode("How to Train Your Dragon", TextType.BOLD, None), 
        TextNode(" is a 2025 American fantasy adventure film", TextType.TEXT, None)])

    def test_italic_delimiter(self):
        node = TextNode("Nico Parker played Sarah Miller in the first season of the HBO series _The Last of Us_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(new_nodes, [TextNode("Nico Parker played Sarah Miller in the first season of the HBO series ", TextType.TEXT, None), 
        TextNode("The Last of Us", TextType.ITALIC, None)] )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_extract_markdown_images(self):
        markdown_string: str = """Here sre some of the most popular Ben 10 aliens: ![Ghostfreak](https://static.wikia.nocookie.net/ben10/images/0/07/Ghostfreak_Ghost_Town_1.PNG/revision/latest/scale-to-width/360?cb=20140618131654), 
        ![Chromastone](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnN00wnNFW-mIGpaeg2IiIjE9e6m4CPjLgKtQQZIva4VQ6a5ACh6AEBV7iQSOf14rBzi8&usqp=CAU),
        ![Ultimate Echo Echo](https://i.ytimg.com/vi/OSNxIw6NUhk/maxresdefault.jpg) and
        ![Atomix](https://ben10hero.com/wp-content/uploads/2018/04/fafbm_686.png)"""

        output: List = extract_markdown_images(markdown_string)
        self.assertListEqual(output, [('Ghostfreak', 'https://static.wikia.nocookie.net/ben10/images/0/07/Ghostfreak_Ghost_Town_1.PNG/revision/latest/scale-to-width/360?cb=20140618131654'), 
        ('Chromastone', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTnN00wnNFW-mIGpaeg2IiIjE9e6m4CPjLgKtQQZIva4VQ6a5ACh6AEBV7iQSOf14rBzi8&usqp=CAU'), 
        ('Ultimate Echo Echo', 'https://i.ytimg.com/vi/OSNxIw6NUhk/maxresdefault.jpg'), ('Atomix', 'https://ben10hero.com/wp-content/uploads/2018/04/fafbm_686.png')])
        
    def test_extract_markdown_links(self):
        markdown_string: str = "1.[Home](https://sitegpt.ai/)/n2. [Tools](https://sitegpt.ai/tools)/n3. [Convert Webpage to Markdown](https://sitegpt.ai/tools/convert-webpage-to-markdown)"
        output: List = extract_markdown_links(markdown_string)
        self.assertListEqual(output, [('Home', 'https://sitegpt.ai/'), ('Tools', 'https://sitegpt.ai/tools'), ('Convert Webpage to Markdown', 'https://sitegpt.ai/tools/convert-webpage-to-markdown')])

    def test_split_nodes_image_1(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_nodes_image_2(self):
        node = TextNode("Image 1: ![Batman](https://media.tenor.com/j8m4rwG-sFkAAAAm/batman.webp), Image 2: ![Batmobile](https://tinyurl.com/4cjh9y8s) and the final image, Image 3: ![Batwing](https://tinyurl.com/msyzfk28). Some Text.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode('Image 1: ', TextType.TEXT), 
                              TextNode('Batman', TextType.IMAGE, 'https://media.tenor.com/j8m4rwG-sFkAAAAm/batman.webp'), 
                              TextNode(', Image 2: ', TextType.TEXT), 
                              TextNode('Batmobile', TextType.IMAGE, 'https://tinyurl.com/4cjh9y8s'), 
                              TextNode(' and the final image, Image 3: ', TextType.TEXT), TextNode('Batwing', TextType.IMAGE , 'https://tinyurl.com/msyzfk28'),
                                TextNode(". Some Text.", TextType.TEXT, None)], new_nodes)
    
    def test_split_nodes_image_3(self):
        node = TextNode("This is some text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is some text with no images.", TextType.TEXT)], new_nodes)

    def test_split_nodes_image_single(self):
        node = TextNode("![Loki](https://tinyurl.com/429m7byt)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode('Loki', TextType.IMAGE, 'https://tinyurl.com/429m7byt')], new_nodes)

    def test_split_nodes_link_1(self):
        node = TextNode("For further information, visit: [Support website](https://theuselessweb.com/) and this forum: [Reddit](https://www.reddit.com/r/InternetIsUseless/)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode('For further information, visit: ', TextType.TEXT, None), 
                              TextNode('Support website', TextType.LINK, 'https://theuselessweb.com/'), 
                              TextNode(' and this forum: ', TextType.TEXT, None), 
                              TextNode('Reddit', TextType.LINK, 'https://www.reddit.com/r/InternetIsUseless/')], new_nodes)
    
    def test_split_nodes_link_2(self):
        node = TextNode("The links present in the navbar are as follows: [Home](https://www.tomarkdown.org/en), [Calculator](https://www.calculatoronline.io/), [Compressor](https://www.compress.run/), [Markdown Syntax Guide](https://www.tomarkdown.org/en/guides/markdown-syntax)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("The links present in the navbar are as follows: ", TextType.TEXT), 
                              TextNode("Home", TextType.LINK, "https://www.tomarkdown.org/en"), TextNode(", ", TextType.TEXT, None), 
                              TextNode("Calculator", TextType.LINK, "https://www.calculatoronline.io/"), 
                              TextNode(", ", TextType.TEXT, None), TextNode("Compressor", TextType.LINK,"https://www.compress.run/"), 
                              TextNode(", ", TextType.TEXT, None), TextNode("Markdown Syntax Guide", TextType.LINK, "https://www.tomarkdown.org/en/guides/markdown-syntax")], new_nodes)

    def test_split_nodes_link_3(self):
        node = TextNode("This is a sentence with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("This is a sentence with no links.", TextType.TEXT)], new_nodes)

    def test_split_nodes_link_single(self):
        node = TextNode("[Doctor Who](https://www.doctorwho.tv/)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode('Doctor Who', TextType.LINK, 'https://www.doctorwho.tv/')], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),], 
        new_nodes)


if __name__ == "__main__":
    unittest.main()