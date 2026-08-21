import tempfile,unittest
from pathlib import Path
from powerx.v2.media.checkpoints import CheckpointStore
class T(unittest.TestCase):
    def test_complete_only_with_file(self):
        with tempfile.TemporaryDirectory() as d:
            s=CheckpointStore(d); p=Path(d)/"x.mp4"
            s.mark_complete("a",str(p),{})
            self.assertFalse(s.is_complete("a"))
            p.write_bytes(b"x")
            self.assertTrue(s.is_complete("a"))
if __name__=="__main__":unittest.main()
