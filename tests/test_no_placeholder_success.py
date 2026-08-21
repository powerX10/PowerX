import unittest
from powerx.v2.adapters.moirai_forecast import MoiraiForecastAdapter
class T(unittest.TestCase):
    def test_moirai_does_not_fake_output(self):
        a=MoiraiForecastAdapter("/missing")
        with self.assertRaises(Exception):
            a.run({"values":[1,2,3],"horizon":2})
if __name__=="__main__":unittest.main()
