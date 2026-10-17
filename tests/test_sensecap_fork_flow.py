"""Test-only fork source routing, not hardware or ESPHome compilation proof."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(ROOT / 'screen_manager/app'))

import core
import firmware
import generate_entries
import yaml

REPO = 'https://github.com/sillevl/homeassistant_espscreen'
REF = 'test/sensecap-d1l-ha-flow'


class SenseCAPForkFlow(unittest.TestCase):
    def setUp(self):
        self.previous_channel = core.channel()
        core.set_channel(None)

    def tearDown(self):
        core.set_channel(self.previous_channel)

    def test_new_screen_is_recognized_and_uses_the_fork(self):
        text = core.installation_yaml({
            'board': 'sensecapd1l', 'name': 'test-panel', 'friendly_name': 'Test panel',
        })
        data = yaml.load(text, Loader=firmware.LenientLoader)
        package = data['packages']['display']
        self.assertEqual(package['url'], REPO)
        self.assertEqual(package['ref'], REF)
        self.assertEqual(package['files'], ['packages/sensecapd1l.yaml'])
        meta = firmware.profile_meta(text)
        self.assertTrue(meta['screen'])
        self.assertEqual(meta['package'], 'packages/sensecapd1l.yaml')
        self.assertEqual(meta['node'], 'test-panel')

    def test_package_components_and_fonts_use_the_same_fork_branch(self):
        data = yaml.load(generate_entries.package_entry('sensecapd1l'), Loader=firmware.LenientLoader)
        self.assertEqual(data['substitutions']['GITHUB_REF'], REF)
        self.assertEqual(data['substitutions']['FONT_DIR'],
                         'https://raw.githubusercontent.com/sillevl/homeassistant_espscreen/${GITHUB_REF}/fonts')
        source = data['external_components'][0]['source']
        self.assertEqual(source['url'], REPO + '.git')
        self.assertEqual(source['ref'], '${GITHUB_REF}')
        self.assertEqual(source['path'], 'components')
        self.assertEqual(data['external_components'][0]['components'], ['smart_display'])

    def test_committed_sensecap_entry_matches_the_generator(self):
        self.assertEqual((ROOT / 'packages/sensecapd1l.yaml').read_text(),
                         generate_entries.package_entry('sensecapd1l'))


if __name__ == '__main__':
    unittest.main()
