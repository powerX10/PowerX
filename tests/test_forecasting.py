import unittest
from powerx.v2.forecasting import ForecastEnsemble
class T(unittest.TestCase):
    def test_median(self):
        r=ForecastEnsemble.consensus([
            {"model":"a","forecast":[1,5]},{"model":"b","forecast":[3,7]},{"model":"c","forecast":[100,9]}
        ])
        self.assertEqual(r["forecast"],[3.0,7.0])
        self.assertTrue(r["ok"])
if __name__=="__main__":unittest.main()
