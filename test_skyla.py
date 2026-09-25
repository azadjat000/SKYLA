import unittest
from unittest.mock import patch

import skyla


class SkylaCoreTests(unittest.TestCase):
    def test_hello_skyla(self):
        self.assertEqual(skyla.respond("hello skyla"), "Hello! I am SKYLA.")

    def test_exit(self):
        self.assertEqual(skyla.respond("exit"), "Goodbye!")

    @patch("builtins.input", side_effect=["hello skyla", "exit"])
    def test_run_stops_after_exit(self, _input):
        skyla.run()
        self.assertEqual(_input.call_count, 2)


if __name__ == "__main__":
    unittest.main()
