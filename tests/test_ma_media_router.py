import unittest
from powerx.v2.ma_media_router import choose_capability
class T(unittest.TestCase):
    def test_routes(self):
        self.assertEqual(choose_capability("4 hour course video bana"),"long_video_generate")
        self.assertEqual(choose_capability("generate image"),"image_generate")
        self.assertEqual(choose_capability("forecast nifty time series"),"forecasting")
if __name__=="__main__":unittest.main()
