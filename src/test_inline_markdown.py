from typing import List
import unittest

from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

    def text_extract_markdown_images(self):
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

    # def test_extract_markdown_links_and_images(self):
    #     markdown_string: str = """Ben was an ordinary 10-year-old boy until he found the Omnitrix, a powerful watch-like device that allowed him to turn into 10 different aliens.
    #     ![Ben Tennyson](https://ben10.fandom.com/wiki/Ben_Tennyson_(Classic)).
    #     Ben's most powerful alien is Alien X, a Celestial Sapien. This article redirects to [Alien X](https://ben10.fandom.com/wiki/Alien_X_(Classic))."""

    #     output_image = extract_markdown_images(markdown_string)
    #     output_link = extract_markdown_links(markdown_string)
    #     self.assertListEqual(output_image, [('Ben Tennyson', 'https://ben10.fandom.com/wiki/Ben_Tennyson_(Classic)')])
    #     self.assertListEqual(output_link, [('Alien X', 'https://ben10.fandom.com/wiki/Alien_X_(Classic)')])

if __name__ == "__main__":
    unittest.main()