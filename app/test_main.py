import os
import unittest
from unittest.mock import patch

import main


class StudentAppTests(unittest.TestCase):
    def test_personalized_defaults(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(
                main.student_info(),
                {
                    "name": "Temirlan",
                    "surname": "Alzhan",
                    "group": "IT2-2307",
                    "id": "38372",
                },
            )

    def test_environment_overrides(self):
        values = {
            "STUDENT_NAME": "Changed",
            "STUDENT_SURNAME": "Example",
            "STUDENT_GROUP": "TEST-1",
            "STUDENT_ID": "000001",
        }
        with patch.dict(os.environ, values, clear=True):
            text = main.render()
            for expected in [
                "Name: Changed",
                "Surname: Example",
                "Group: TEST-1",
                "Student ID: 000001",
            ]:
                self.assertIn(expected, text)

    def test_application_output(self):
        text = main.render()
        self.assertIn("DevOps Student Application", text)
        self.assertIn("Application Version:", text)
        self.assertIn("Application is running successfully!", text)


if __name__ == "__main__":
    unittest.main()
