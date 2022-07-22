import unittest
from napster import short_to_id, get_albs, list_genres, random_album


class TestNapster(unittest.TestCase):
    def test_short_to_id(self):
        self.assertEqual(short_to_id(rock), g.5)
        self.assertEqual(short_to_id(pop), g.115)

    def test_get_albs(self):
        self.assertEqual(type(get_albs(rock)), type([]))
        self.assertEqual(len(get_albs(pop)), 2)

    def test_random_album(self):
        self.assertEqual(type(random_album(albums)), type([]))
        self.assertEqual(len(random_album(albums)), 2)


if __name__ == '__main__':
    unittest.main()
