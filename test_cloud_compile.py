import unittest
from pathlib import Path
from cloud_compile import command, assess

class TestRunner(unittest.TestCase):
    def test_command(self):
        c=command(Path('C:/Program Files/WB.exe'),Path('C:/My Mod/mod.gproj'),Path('C:/runs/test'), 'ALL', True)
        self.assertIn(str(Path('C:/My Mod/mod.gproj')),c)
        self.assertIn('-enableWARP',c)
        self.assertIn('-wbSilent',c)
        self.assertIn('-validate',c)
    def test_success(self): self.assertEqual(assess(0,'SCRIPT : Script validation successful.')[0],'validation_reported_success')
    def test_unconfirmed(self): self.assertEqual(assess(0,'Engine started')[0],'unconfirmed')
    def test_error(self): self.assertEqual(assess(0,'SCRIPT (E): Undefined variable')[0],'errors_in_log')
    def test_false_success(self): self.assertEqual(assess(0,'Script validation successful\nSCRIPT (E): error')[0],'errors_in_log')
    def test_exit(self): self.assertEqual(assess(4294967295,'')[0],'validation_failed_or_engine_error')
    def test_timeout(self): self.assertEqual(assess(None,'',True)[0],'timeout')
    def test_launch(self): self.assertEqual(assess(None,'')[0],'launch_error')

if __name__ == '__main__': unittest.main()
