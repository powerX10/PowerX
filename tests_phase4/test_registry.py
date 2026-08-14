import unittest
from powerx.production.runtime_registry import RuntimeRegistry, RuntimeTarget

class RegistryTests(unittest.TestCase):
    def test_priority(self):
        r = RuntimeRegistry()
        r.register(RuntimeTarget("b","m","cpu","http://b/v1",20))
        r.register(RuntimeTarget("a","m","gpu16","http://a/v1",10))
        self.assertEqual(r.all()[0].id, "a")

if __name__ == "__main__":
    unittest.main()
