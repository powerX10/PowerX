import unittest
from powerx.production.security import APIKeyValidator, SlidingWindowRateLimiter

class SecurityTests(unittest.TestCase):
    def test_key(self):
        v = APIKeyValidator("a" * 32)
        self.assertTrue(v.validate("a" * 32))
        self.assertFalse(v.validate("b" * 32))

    def test_rate_limit(self):
        r = SlidingWindowRateLimiter(requests=2, window_seconds=60)
        self.assertTrue(r.allow("u", now=1))
        self.assertTrue(r.allow("u", now=2))
        self.assertFalse(r.allow("u", now=3))
        self.assertTrue(r.allow("u", now=62))

if __name__ == "__main__":
    unittest.main()
