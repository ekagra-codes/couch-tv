import os
import subprocess
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bridge"))
import config


class TestProductionFeatures(unittest.TestCase):
    def test_inputs_validation(self):
        """Verify _inputs correctly parses valid items and ignores malformed ones."""
        raw = [
            {"port": 1, "label": "PS5", "icon": "ps5"},
            {"match": "HDMI 2", "label": "Switch", "icon": "switch"},
            {"id": "HW5", "label": "Xbox Series X", "icon": "xbox"},
            {"device": "Apple TV", "label": "Apple TV", "icon": "hdmi"},
            {"label": "Invalid because no selector"},
            {"port": 99, "label": "Invalid port"},
            "not a dict",
            {"port": 3, "label": "", "icon": "hdmi"},  # empty label
            {"port": 4, "label": "Generic", "icon": "invalid_icon_fallback"},
        ]
        parsed = config._inputs(raw)
        self.assertEqual(len(parsed), 5)
        self.assertEqual(parsed[0], {"port": 1, "label": "PS5", "icon": "ps5"})
        self.assertEqual(parsed[1], {"match": "HDMI 2", "label": "Switch", "icon": "switch"})
        self.assertEqual(parsed[2], {"id": "HW5", "label": "Xbox Series X", "icon": "xbox"})
        self.assertEqual(parsed[3], {"device": "Apple TV", "label": "Apple TV", "icon": "hdmi"})
        # Fallback icon check
        self.assertEqual(parsed[4]["icon"], "hdmi")
        self.assertEqual(parsed[4]["label"], "Generic")

    def test_home_integration_inputs(self):
        """Verify _home includes sanitized inputs."""
        h = {
            "inputs": [
                {"port": 1, "label": "PlayStation 5", "icon": "ps5"}
            ]
        }
        res = config._home(h)
        self.assertIn("inputs", res)
        self.assertEqual(len(res["inputs"]), 1)
        self.assertEqual(res["inputs"][0]["label"], "PlayStation 5")

    def test_skip_watch_next_default_empty(self):
        """Verify skip_watch_next is empty by default, and only populates if configured."""
        res_default = config._home({})
        self.assertEqual(res_default["skip_watch_next"], [])

        res_configured = config._home({
            "skip_watch_next": ["com.tcl.browser", "com.example.spam", "com.tcl.browser", "invalid;pkg!"]
        })
        self.assertEqual(res_configured["skip_watch_next"], ["com.tcl.browser", "com.example.spam"])

    def test_watch_next_per_app(self):
        """Verify watch_next_per_app defaults to 5 and clamps between 1 and 20."""
        self.assertEqual(config._home({})["watch_next_per_app"], 5)
        self.assertEqual(config._home({"watch_next_per_app": 10})["watch_next_per_app"], 10)
        self.assertEqual(config._home({"watch_next_per_app": 0})["watch_next_per_app"], 1)
        self.assertEqual(config._home({"watch_next_per_app": 99})["watch_next_per_app"], 20)

    def test_home_config_tool_serialization(self):
        """Verify home-config.py correctly serializes home settings to JSON."""
        root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
        res = subprocess.run(
            [sys.executable, os.path.join(root, "tv-home", "tools", "home-config.py"), "--json"],
            capture_output=True,
            text=True,
            check=True
        )
        self.assertIn('"home"', res.stdout)
        self.assertIn('"skip_watch_next"', res.stdout)
        self.assertIn('"watch_next_per_app"', res.stdout)


if __name__ == "__main__":
    unittest.main()
