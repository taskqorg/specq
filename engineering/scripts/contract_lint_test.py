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

    def test_budget_below_target_above_target_and_over_cap(self):
        below = CLEAN + '\n' * (43008 - len(CLEAN.encode('utf-8')))
        self.assertEqual(lint(below)[1], [])
        above = below + '\n'
        self.assertEqual(messages(above), [])
        self.assertEqual(messages(above, 'compact'), ['43009 bytes > target 43008 (cap 61440)'])
        over = below + '\n' * (61441 - 43008)
        self.assertTrue(any('bytes > cap 61440' in m for m in messages(over)))
        self.assertEqual(messages(over, 'compact'), [])

    def test_cli_byte_target_and_cap(self):
        import contextlib, io, tempfile
        from contract_lint import main
        for size, expected in ((43009, 0), (61441, 1)):
            with self.subTest(size=size), tempfile.TemporaryDirectory() as directory:
                path = pathlib.Path(directory) / 'demo.md'
                path.write_text(CLEAN + '\n' * (size - len(CLEAN.encode('utf-8'))), encoding='utf-8')
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = main([str(path)])
                self.assertEqual(code, expected)
                self.assertEqual('COMPACT:' in out.getvalue(), expected == 0)
                self.assertIn(' lines, longest line ', out.getvalue())

    def test_declared_cap(self):
        for comment in ('bytes=100000', 'bytes=100000 lines=1'):
            with self.subTest(comment=comment):
                declared = '<!-- contract-budget: ' + comment + ' -->\n' + CLEAN + 'x\n' * 300
                self.assertEqual(lint(declared)[0]['max_bytes'], 100000)
                self.assertEqual(lint(declared)[1], [])

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
