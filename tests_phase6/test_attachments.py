import unittest
from powerx.final.attachments.router import attachment_kind, required_task
class T(unittest.TestCase):
    def test_image(self):
        self.assertEqual(attachment_kind("x.png"),"image")
        self.assertEqual(required_task("image"),"vision_analysis")
if __name__=="__main__":unittest.main()
