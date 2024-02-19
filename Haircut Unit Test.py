import unittest
from your_module import HairCuttable  # Import the HairCuttable class from your module

class TestHairCuttable(unittest.TestCase):
    def test_receive_haircut(self):
        # Create an instance of HairCuttable
        haircuttable = HairCuttable()

        # Test initial state
        self.assertEqual(haircuttable.current_hair_cut_length, 0)

        # Test receive_haircut method
        haircuttable.receive_haircut(5)
        self.assertEqual(haircuttable.current_hair_cut_length, 5)

    def test_reduce_haircut_time(self):
        # Create an instance of HairCuttable
        haircuttable = HairCuttable()

        # Test initial state
        self.assertEqual(haircuttable.current_hair_cut_length, 0)

        # Test reduce_haircut_time method with non-zero initial length
        haircuttable.receive_haircut(5)
        haircuttable.reduce_haircut_time()
        self.assertEqual(haircuttable.current_hair_cut_length, 4)

        # Test reduce_haircut_time method with zero initial length
        haircuttable.reduce_haircut_time()
        self.assertEqual(haircuttable.current_hair_cut_length, 0)

if __name__ == '__main__':
    unittest.main()
