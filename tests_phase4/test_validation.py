import unittest
from powerx.production.validation import validate_messages

class ValidationTests(unittest.TestCase):
    def test_valid(self):
        validate_messages([{"role":"user","content":"hello"}])

    def test_bad_role(self):
        with self.assertRaises(ValueError):
            validate_messages([{"role":"root","content":"hello"}])

if __name__ == "__main__":
    unittest.main()
