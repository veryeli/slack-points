"""
Test point counter functionality
"""

TEST_PREFECTS = ["prefect"]

from main import PointCounter
import unittest

class TestPointCounter(unittest.TestCase):
    """Initialize a point counter and test response messages"""

    def test_adding_points(self):
        p = PointCounter(TEST_PREFECTS)
        msg = p.award_points("6 points to Gryffendor", TEST_PREFECTS[0])
        for m in msg:
            self.assertEqual(m,"6 points to Gryffendor")

    def test_adding_points_not_by_prefect(self):
        p = PointCounter(TEST_PREFECTS)
        msg = p.award_points("6 points to Gryffendor", "harry potter")
        for m in msg:
            self.assertEqual(m, "1 point to Gryffendor")

    def test_calculate_standings(self):
        p = PointCounter(TEST_PREFECTS)
        p.award_points("6 points to Gryffendor", TEST_PREFECTS[0])
        p.award_points("7 points to Ravenclaw", TEST_PREFECTS[0])
        p.award_points("8 points to Hufflepuff", TEST_PREFECTS[0])
        p.award_points("9 points to Slytherin", TEST_PREFECTS[0])
        p.print_status()

if __name__ == "__main__":
    unittest.main()