import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

import skyla


class SkylaCoreTests(unittest.TestCase):
    def config(self, directory, model="test-model"):
        path = Path(directory) / "config.json"
        path.write_text(
            json.dumps({
                "version": "test",
                "model": model,
                "ollama_url": "http://localhost:11434",
                "log_file": str(Path(directory) / "skyla.log"),
            }),
            encoding="utf-8",
        )
        return path

    def test_startup_and_commands(self):
        """Test that SKYLA starts and processes basic commands."""
        with tempfile.TemporaryDirectory() as directory:
            config = skyla.load_config(self.config(directory))
            with patch("builtins.input", side_effect=["hello skyla", "exit"]), patch("sys.stdout") as output:
                skyla.run(config)
            self.assertEqual(skyla.respond("hello skyla"), "Hello! I am SKYLA.")

    def test_exit(self):
        """Test that exit command returns correct response."""
        self.assertEqual(skyla.respond("exit"), "Goodbye!")

    def test_configuration(self):
        """Test that configuration is loaded correctly."""
        with tempfile.TemporaryDirectory() as directory:
            path = self.config(directory, model="test-model")
            config = skyla.load_config(path)
            self.assertEqual(config["model"], "test-model")
            self.assertEqual(config["ollama_url"], "http://localhost:11434")

    def test_status_does_not_require_ollama(self):
        """Test that --status works without requiring Ollama to be running."""
        with patch("skyla.shutil.which", return_value=None):
            result = skyla.status({"version": "test", "model": "test-model", "ollama_url": "http://localhost:11434"})
        self.assertIn("healthy", result)
        self.assertIn("not installed", result)
        self.assertIn("Python:", result)
        self.assertIn("Platform:", result)

    def test_configuration_error(self):
        """Test that loading a non-existent config file raises an error."""
        with self.assertRaises(ValueError):
            skyla.load_config("/path/that/does/not/exist.json")

    def test_invalid_configuration_empty_model(self):
        """Test that an empty model name is rejected."""
        config = {
            "model": "",
            "ollama_url": "http://localhost:11434",
            "log_file": "/tmp/skyla-test.log",
        }
        with self.assertRaises(ValueError):
            skyla.validate_config(config)

    def test_invalid_configuration_url(self):
        """Test that an invalid Ollama URL is rejected."""
        config = {
            "model": "test-model",
            "ollama_url": "not-a-url",
            "log_file": "/tmp/skyla-test.log",
        }
        with self.assertRaises(ValueError):
            skyla.validate_config(config)

    def test_valid_configuration(self):
        """Test that a valid configuration passes validation."""
        config = {
            "model": "test-model",
            "ollama_url": "http://localhost:11434",
            "log_file": "/tmp/skyla-test.log",
        }
        self.assertIsNone(skyla.validate_config(config))

    def test_ollama_successful_response(self):
        """Test that Ollama response is correctly parsed."""
        config = {"model": "test-model", "ollama_url": "http://localhost:11434"}
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__iter__.return_value = iter([
                (json.dumps({"response": "This is "}) + "\n").encode("utf-8"),
                (json.dumps({"response": "a test response", "done": True}) + "\n").encode("utf-8"),
            ])
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response
            response = skyla.respond("test prompt", config)
            self.assertEqual(response, "This is a test response")

    def test_ollama_malformed_stream_response(self):
        """Test that malformed streaming data is reported as a communication error."""
        config = {"model": "test-model", "ollama_url": "http://localhost:11434"}
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__iter__.return_value = iter([
                b'not-valid-json\\n',
            ])
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response

            response = skyla.respond("test prompt", config)

            self.assertIn("Error: Ollama communication error:", response)

    def test_ollama_empty_stream_response(self):
        """Test that an empty Ollama stream is handled safely."""
        config = {"model": "test-model", "ollama_url": "http://localhost:11434"}
        with patch("urllib.request.urlopen") as mock_urlopen:
            mock_response = MagicMock()
            mock_response.__iter__.return_value = iter([])
            mock_response.__enter__.return_value = mock_response
            mock_urlopen.return_value = mock_response

            response = skyla.respond("test prompt", config)

            self.assertEqual(response, "")

    def test_ollama_unavailable(self):
        """Test error handling when Ollama server is unavailable."""
        import urllib.error

        config = {"model": "test-model", "ollama_url": "http://localhost:11434"}
        with patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Connection refused")):
            response = skyla.respond("test prompt", config)
            self.assertIn("Ollama server not available", response)

    def test_ollama_model_missing(self):
        """Test error handling when the configured model is missing."""
        import urllib.error

        config = {"model": "missing-model", "ollama_url": "http://localhost:11434"}
        with patch("urllib.request.urlopen", side_effect=urllib.error.HTTPError(
            "http://localhost:11434/api/generate", 404, "Not Found", {}, None
        )):
            response = skyla.respond("test prompt", config)
            self.assertIn("not available", response)
            self.assertIn("ollama pull", response)

    def test_built_in_commands_without_config(self):
        """Test that built-in commands work even without configuration."""
        self.assertEqual(skyla.respond("hello skyla"), "Hello! I am SKYLA.")
        self.assertEqual(skyla.respond("exit"), "Goodbye!")

    def test_built_in_commands_are_normalized(self):
        """Test that built-in commands ignore case and surrounding spaces."""
        self.assertEqual(skyla.respond("  HELLO SKYLA  "), "Hello! I am SKYLA.")
        self.assertEqual(skyla.respond("  Exit  "), "Goodbye!")

    def test_builtin_command_names_are_defined(self):
        """Test that SKYLA exposes its supported built-in command names."""
        self.assertEqual(
            set(skyla.BUILTIN_COMMANDS),
            {"hello skyla", "exit", "--status"},
        )

    def test_similar_text_is_not_treated_as_built_in_command(self):
        """Test that longer prompts are still sent to Ollama."""
        config = {"model": "test-model", "ollama_url": "http://localhost:11434"}
        with patch("skyla.query_ollama", return_value="AI response") as mock_query:
            response = skyla.respond("hello skyla, tell me about Linux", config)

        self.assertEqual(response, "AI response")
        mock_query.assert_called_once_with(
            "hello skyla, tell me about Linux",
            "test-model",
            "http://localhost:11434",
            on_chunk=None,
        )

    def test_version_constant(self):
        """Test that VERSION is correctly set."""
        self.assertEqual(skyla.VERSION, "0.3.0")

    def test_blank_input_is_ignored(self):
        """Test that blank input does not contact Ollama."""
        config = {
            "model": "test-model",
            "ollama_url": "http://localhost:11434",
        }
        with patch("skyla.respond") as mock_respond, \
             patch("builtins.input", side_effect=["   ", "exit"]), \
             patch("sys.stdout"):
            skyla.run(config)

        mock_respond.assert_called_once_with(
            "exit",
            config,
            unittest.mock.ANY,
            on_chunk=unittest.mock.ANY,
        )

    def test_session_continues_after_ollama_error(self):
        """Test that an Ollama error does not terminate the session."""
        config = {
            "model": "test-model",
            "ollama_url": "http://localhost:11434",
        }

        with patch(
            "skyla.respond",
            side_effect=[
                "Error: Ollama server not available",
                "Goodbye!",
            ],
        ) as mock_respond, \
             patch("builtins.input", side_effect=["first question", "exit"]), \
             patch("sys.stdout"):
            skyla.run(config)

        self.assertEqual(mock_respond.call_count, 2)


if __name__ == "__main__":
    unittest.main()
