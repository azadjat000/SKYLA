import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import skyla


class SkylaCoreTests(unittest.TestCase):
    def config(self, directory):
        path = Path(directory) / "config.json"
        path.write_text(json.dumps({"version": "test", "model": "test-model", "log_file": str(Path(directory) / "skyla.log")}), encoding="utf-8")
        return path

    def test_startup_and_commands(self):
        with tempfile.TemporaryDirectory() as directory:
            config = skyla.load_config(self.config(directory))
            with patch("builtins.input", side_effect=["hello skyla", "exit"]), patch("sys.stdout") as output:
                skyla.run(config)
            self.assertIn("SKYLA started", "".join(call.args[0] for call in output.write.call_args_list if call.args))
            self.assertEqual(skyla.respond("hello skyla"), "Hello! I am SKYLA.")

    def test_exit(self):
        self.assertEqual(skyla.respond("exit"), "Goodbye!")

    def test_configuration(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.config(directory)
            self.assertEqual(skyla.load_config(path)["model"], "test-model")

    def test_status_does_not_require_ollama(self):
        with patch("skyla.shutil.which", return_value=None):
            result = skyla.status({"version": "test", "model": "test-model"})
        self.assertIn("healthy", result)
        self.assertIn("not installed", result)

    def test_configuration_error(self):
        with self.assertRaises(ValueError):
            skyla.load_config("/path/that/does/not/exist.json")


if __name__ == "__main__":
    unittest.main()
