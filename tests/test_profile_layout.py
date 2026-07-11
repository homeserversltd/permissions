import hashlib
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASELINE_ROOT_POLICIES = {
    "flask-admin": "d1a735b2aeb039eebd3672535c90f51bf5755e964382e368e033bc7fbb09c08a",
    "flask-cat": "92659b33ac38281428c6deddced955119f22ebff4f558bdf74971d5686314768",
    "flask-commands": "5c4ad8b21f016d82c45fe91593afef6454ffa3713c12ae8f59ed041d1a7addd4",
    "flask-config": "5c5e8c8f2a20dbb38152b1b08b65f43ef7a12deffb5c363eaf2897763ef88e5c",
    "flask-disk": "03a36a2cfa0509e28871b6f42b4fcb413278710d2b4963161b98dd1980d36abb",
    "flask-files": "60e845ee141ecebe01bb143db6ccd98897c3b027ca9df4db95de1c5a881207f8",
    "flask-keyman": "9ded89275af973857ab7504f216b0f1544b97d0db19fdd35f879d8049f412f2e",
    "flask-systemctl": "521c1f731869726e24983948f68a4176caa6382ff63c98e651ffa091de1d1338",
    "flask-tailscale": "8fcfd95a8328e051bfa9ebd07b4e8eaaaae4cd93153d275c457d429cb774657e",
    "flask-updates": "bafcf5ce78f3cbef0aeb24d11365a27f2ea94b2f03d3ee61cdd8e08d995d31f7",
    "flask-vault": "5bb69c974824174be6f6a223bca2baff4e68183a5f4d907842e0aaec363ffa7c",
    "flask-vpn": "97bcdf6b7ce5fa14c08f5fe7ca7f0ebeaaba8a6b951bd81b023efa9d8c2a9757",
}

class ProfileLayoutTests(unittest.TestCase):
    def test_root_flask_policies_are_unchanged(self):
        actual = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in ROOT.iterdir() if path.is_file() and path.name.startswith("flask-")}
        self.assertEqual(BASELINE_ROOT_POLICIES, actual)

    def test_updates_harvester_discovery_still_finds_root_policies(self):
        manifest = json.loads((ROOT / "manifest.json").read_text())
        consumer = manifest["consumers"]["updates_harvester"]
        self.assertEqual("iterdir", consumer["discovery"])
        pattern = re.compile(consumer["policy_pattern"])
        discovered = sorted(path.name for path in ROOT.iterdir() if path.is_file() and pattern.match(path.name))
        self.assertEqual(sorted(BASELINE_ROOT_POLICIES), discovered)

    def test_profile_registry_and_sources_resolve(self):
        manifest = json.loads((ROOT / "manifest.json").read_text())
        for profile_id, relative_path in manifest["profiles"].items():
            profile = json.loads((ROOT / relative_path).read_text())
            self.assertEqual(profile_id, profile["profile_id"])
            for policy in profile["policies"]:
                source = Path(policy["source"])
                self.assertEqual(policy["basename"], source.name)
                self.assertTrue((ROOT / source).is_file(), policy["source"])
        homeserver = json.loads((ROOT / manifest["profiles"]["homeserver"]).read_text())
        self.assertTrue(all(item["source"] == item["basename"] for item in homeserver["policies"]))

if __name__ == "__main__":
    unittest.main()
