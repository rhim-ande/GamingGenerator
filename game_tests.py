import unittest
from games import get_games


# tests if get_games output is a list of 3 items
class TestGames(unittest.TestCase):
    def test_get_games(self):
        self.assertEqual(type(get_games(horror)), type([]))
        self.assertEqual(len(get_games(horror)), 3)


if __name__ == '__main__':
    unittest.main()
