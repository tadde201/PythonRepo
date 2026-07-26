import sys
import unittest
from unittest.mock import patch

from app import main as app_main


class TestAppMain(unittest.TestCase):
    def test_parse_arguments_no_email(self):
        testargs = ["app/main.py", "--dry-run", "--no-email", "--output", "out.json"]
        with patch.object(sys, "argv", testargs):
            args = app_main.parse_arguments()
            self.assertTrue(args.dry_run)
            self.assertTrue(args.no_email)
            self.assertEqual(args.output, "out.json")

    @patch("app.main.send_email")
    @patch("app.main.save_results")
    @patch("app.main.print")
    def test_main_dry_run_no_email(self, mock_print, mock_save_results, mock_send_email):
        candidate = {
            "name": "Test User",
            "location": "Remote",
            "skills": ["python"],
            "experience": ["developer"],
            "target_roles": ["Engineer"],
        }
        jobs = [
            {
                "title": "Python Developer",
                "company": "Acme",
                "description": "Looking for a python developer with automation skills.",
            }
        ]

        with patch("app.main.load_candidate_profile", return_value=candidate), \
             patch("app.main.load_jobs", return_value=jobs), \
             patch.object(sys, "argv", ["app/main.py", "--dry-run", "--no-email"]):
            app_main.main()

        mock_save_results.assert_called_once()
        mock_send_email.assert_not_called()
        self.assertTrue(
            any(
                "Email notifications skipped because --no-email was provided." in str(call.args[0])
                for call in mock_print.call_args_list
                if call.args
            )
        )


if __name__ == "__main__":
    unittest.main()
