"""
Test point counter functionality
"""

from main import PointCounter
import unittest

class TestPointCounter(unittest.TestCase):
    """Initialize a point counter and test response messages"""

    def __init__(self):
        self.test_prefects = ["prefect"]
        self.prefect = "prefect"
        self.p = PointCounter(test_prefects)


    def test_adding_points(self):
        msg = self.p.award_points("6 points to Gryffendor", test_prefects[0])
        for m in msg:
            self.assertEqual(m,"6 points to Gryffendor")

    def test_adding_points_not_by_prefect(self):
        msg = self.p.award_points("6 points to Gryffendor", "harry potter")
        for m in msg:
            self.assertEqual(m, "1 point to Gryffendor")



    def test_calculate_standings(self):
        self.p.award_points("6 points to Gryffendor", "prefect")
        self.p.award_points("7 points to Ravenclaw", "prefect")
        self.p.award_points("8 points to Hufflepuff", "prefect")
        self.p.award_points("9 points to Slytherin", "prefect")
        self.p.print_status()

if __name__ == "__main__":
    unittest.main()