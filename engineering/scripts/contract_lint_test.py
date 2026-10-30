"""Regression cases for contract_lint.py; every contract text here is invented."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from contract_lint import lint  # noqa: E402

CLEAN = '# demo\n\nDemo stores notes.\n\n## Principles\n\n- **R1.** Notes stay local.\n\n## Storage\n\n### Files\n\nOne file per note.\n'


def messages(text, level='error'):
    return [message for found_level, _, message in lint(text)[1] if found_level == level]


class ContractLintTest(unittest.TestCase):
    def test_clean_contract_passes(self):
        self.assertEqual(lint(CLEAN)[1], [])

    def test_budget_cap_headroom_and_declared_cap(self):
        self.assertTrue(any('lines > cap 300' in m for m in messages(CLEAN + 'x\n' * 300)))
        self.assertTrue(any('70% of cap 300' in m for m in messages(CLEAN + 'x\n' * 200, 'warning')))
        declared = '<!-- contract-budget: bytes=100000 lines=1000 -->\n' + CLEAN + 'x\n' * 300
        self.assertEqual([m for m in messages(declared) if 'cap' in m], [])

    def test_line_length_ignores_link_targets_and_code(self):
        self.assertTrue(any('401 chars' in m for m in messages(CLEAN + 'a' * 401 + '\n')))
        self.assertEqual(messages(CLEAN + '[a](' + 'u' * 500 + ')\n'), [])
        self.assertEqual(messages(CLEAN + '```\n' + 'a' * 500 + '\n```\n'), [])

    def test_dates_outside_code_only(self):
        self.assertTrue(any('2026-10-17' in m for m in messages(CLEAN + 'Accepted target2026-10-17.\n')))
        self.assertEqual(messages(CLEAN + '```\n2026-10-17\n```\n'), [])

    def test_decision_log_phrases_without_state_false_positives(self):
        self.assertTrue(messages(CLEAN + 'Config absent before the owner chose.\n'))
        self.assertTrue(messages(CLEAN + 'Tags come from main (owner answer on #134).\n'))
        self.assertEqual(messages(CLEAN + '`CHANGELOG.md` lists board changes. Previously authorized grants resume.\n'), [])
        self.assertEqual(messages(CLEAN + 'A block no longer stored is unknown.\n'), [])

    def test_heading_outline(self):
        self.assertTrue(any('must be Principles' in m for m in messages('# demo\n\nPurpose.\n\n## Scope\n')))
        self.assertTrue(any('no purpose paragraph' in m for m in messages('# demo\n\n## Principles\n')))
        self.assertTrue(any('skips from H2 to H4' in m for m in messages(CLEAN + '## Extra\n\n#### Deep\n')))
        self.assertTrue(any('duplicate heading' in m for m in messages(CLEAN + '## Storage\n')))
        self.assertTrue(any('history' in m for m in messages(CLEAN + '## Decisions still open\n')))
        self.assertTrue(any('generic heading' in m for m in messages(CLEAN + '## Notes\n')))


if __name__ == '__main__':
    unittest.main()
