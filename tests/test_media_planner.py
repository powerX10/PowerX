import tempfile,unittest
from powerx.v2.media.planner import LongFormPlanner
from powerx.v2.media.schema import MediaProjectRequest
class T(unittest.TestCase):
    def test_exact_duration(self):
        with tempfile.TemporaryDirectory() as d:
            p=LongFormPlanner(d).plan(MediaProjectRequest("course",25,segment_seconds=8))
            self.assertEqual(len(p.segments),4)
            self.assertEqual(sum(x.duration_seconds for x in p.segments),25)
            self.assertEqual((p.width,p.height),(1280,720))
if __name__=="__main__":unittest.main()
