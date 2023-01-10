import unittest

class SimpleMath:
    @staticmethod
    def addition(x, y):
        return x + y

@staticmethod
def subtraction(x, y):
    return x - y

class TestSimpleMath(unittest.TestCase):
    def test_addition(self):
        result = SimpleMath.addition(5, 3)
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = SimpleMath.subtraction(5, 3)
        self.assertEqual(result, 2)

if __name__ == '__main__':
    unittest.main()