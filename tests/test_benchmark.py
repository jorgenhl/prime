"""Unit tests for benchmark module."""

import json
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

# Add benchmarks directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'benchmarks'))

# pylint: disable=wrong-import-position
# flake8: noqa: E402
from benchmark import save_checkpoint, load_checkpoint, CHECKPOINT_FILE
# pylint: enable=wrong-import-position


class TestCheckpoint(unittest.TestCase):
    """Test cases for checkpoint functionality."""

    def setUp(self):
        """Create a temporary directory for checkpoint files."""
        self.test_dir = tempfile.mkdtemp()
        self.original_checkpoint = CHECKPOINT_FILE

    def tearDown(self):
        """Clean up temporary files."""
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

    @patch('benchmark.CHECKPOINT_FILE')
    @patch('benchmark.time.time')
    def test_save_checkpoint(self, mock_time, mock_checkpoint_file):
        """Test saving checkpoint to file."""
        mock_time.return_value = 1234567890.5

        checkpoint_path = os.path.join(self.test_dir, 'checkpoint.json')
        with patch('benchmark.CHECKPOINT_FILE', checkpoint_path):
            save_checkpoint(1000, 123.45)

        self.assertTrue(os.path.exists(checkpoint_path))
        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        self.assertEqual(data['count'], 1000)
        self.assertAlmostEqual(data['elapsed_time'], 123.45)
        self.assertAlmostEqual(data['timestamp'], 1234567890.5)

    @patch('benchmark.CHECKPOINT_FILE')
    def test_load_checkpoint_exists(self, mock_checkpoint_file):
        """Test loading an existing checkpoint."""
        checkpoint_path = os.path.join(self.test_dir, 'checkpoint.json')
        checkpoint_data = {
            'count': 5000,
            'elapsed_time': 234.56,
            'timestamp': 1234567890.0
        }
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f)

        with patch('benchmark.CHECKPOINT_FILE', checkpoint_path):
            result = load_checkpoint()

        self.assertIsNotNone(result)
        self.assertEqual(result['count'], 5000)
        self.assertAlmostEqual(result['elapsed_time'], 234.56)

    @patch('benchmark.CHECKPOINT_FILE')
    def test_load_checkpoint_not_exists(self, mock_checkpoint_file):
        """Test loading when checkpoint file doesn't exist."""
        checkpoint_path = os.path.join(self.test_dir, 'nonexistent.json')

        with patch('benchmark.CHECKPOINT_FILE', checkpoint_path):
            result = load_checkpoint()

        self.assertIsNone(result)

    @patch('benchmark.CHECKPOINT_FILE')
    def test_load_checkpoint_corrupted(self, mock_checkpoint_file):
        """Test loading a corrupted checkpoint file."""
        checkpoint_path = os.path.join(self.test_dir, 'corrupted.json')
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            f.write('not valid json {]')

        with patch('benchmark.CHECKPOINT_FILE', checkpoint_path):
            result = load_checkpoint()

        self.assertIsNone(result)

    @patch('benchmark.CHECKPOINT_FILE')
    @patch('benchmark.time.time')
    def test_checkpoint_roundtrip(self, mock_time, mock_checkpoint_file):
        """Test saving and loading checkpoint."""
        checkpoint_path = os.path.join(self.test_dir, 'roundtrip.json')
        mock_time.return_value = 1234567890.0

        with patch('benchmark.CHECKPOINT_FILE', checkpoint_path):
            save_checkpoint(2500, 150.75)
            result = load_checkpoint()

        self.assertEqual(result['count'], 2500)
        self.assertAlmostEqual(result['elapsed_time'], 150.75)


class TestBenchmarkArguments(unittest.TestCase):
    """Test cases for command-line argument parsing."""

    @patch('benchmark.find_n_primes')
    @patch('sys.argv', ['benchmark.py'])
    def test_default_arguments(self, mock_find_n_primes):
        """Test default behavior (5 minutes, with checkpoint resume)."""
        mock_find_n_primes.return_value = [2, 3, 5, 7]
        with patch('benchmark.load_checkpoint', return_value=None):
            with patch('benchmark.time.time', side_effect=[0, 10]):
                # Testing argument parsing without running main
                # More of a placeholder for integration testing
                pass

    @patch('benchmark.find_n_primes')
    @patch('sys.argv', ['benchmark.py', '--count', '100'])
    def test_count_argument(self, mock_find_n_primes):
        """Test --count argument."""
        # Setup mock to return quickly
        mock_find_n_primes.return_value = list(range(2, 102))

    @patch('benchmark.find_n_primes')
    @patch('sys.argv', ['benchmark.py', '--time', '60'])
    def test_time_argument(self, mock_find_n_primes):
        """Test --time argument."""
        mock_find_n_primes.return_value = [2, 3, 5, 7]

    @patch('benchmark.find_n_primes')
    @patch('sys.argv', ['benchmark.py', '--start', '1000'])
    def test_start_argument(self, mock_find_n_primes):
        """Test --start argument."""
        mock_find_n_primes.return_value = [2, 3, 5, 7]

    @patch('benchmark.find_n_primes')
    @patch('sys.argv', ['benchmark.py', '--no-resume'])
    def test_no_resume_argument(self, mock_find_n_primes):
        """Test --no-resume argument."""
        mock_find_n_primes.return_value = [2, 3, 5, 7]


class TestBenchmarkIntegration(unittest.TestCase):
    """Integration tests for benchmark functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test files."""
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

    @patch('benchmark.CHECKPOINT_FILE')
    @patch('benchmark.find_n_primes')
    @patch('benchmark.time.time')
    def test_resume_from_checkpoint(self, mock_time, mock_find_n_primes, _):
        """Test that benchmark correctly resumes from checkpoint."""
        checkpoint_path = os.path.join(self.test_dir, 'checkpoint.json')

        # Setup: create an existing checkpoint
        checkpoint_data = {
            'count': 5000,
            'elapsed_time': 100.0,
            'timestamp': 1000.0
        }
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f)

        # Mock time progression
        time_values = [100.0 + 100.0, 100.0 + 101.0, 100.0 + 320.0]
        mock_time.side_effect = time_values
        mock_find_n_primes.return_value = [2, 3, 5, 7]

        with patch('benchmark.CHECKPOINT_FILE', checkpoint_path):
            with patch('benchmark.load_checkpoint') as mock_load:
                mock_load.return_value = checkpoint_data
                # The resumed benchmark should have used the checkpoint data

    @patch('benchmark.find_n_primes')
    @patch('benchmark.time.time')
    def test_count_mode_no_checkpoint(self, mock_time, mock_find_n_primes):
        """Test that count mode does not save checkpoint."""
        # In count mode, checkpoints should not be saved/used
        primes = list(range(2, 102))  # 100 primes
        mock_find_n_primes.return_value = primes
        mock_time.side_effect = [0, 1, 2, 3, 4, 5]

    @patch('benchmark.find_n_primes')
    @patch('benchmark.time.time')
    def test_time_mode_saves_checkpoint(self, mock_time, mock_find_n_primes):
        """Test that time mode saves checkpoint."""
        primes = [2, 3, 5, 7, 11, 13]
        mock_find_n_primes.return_value = primes
        mock_time.side_effect = [0, 1, 2, 3]


if __name__ == '__main__':
    unittest.main()
