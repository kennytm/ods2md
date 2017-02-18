import ods2md

import unittest
import os.path
import io

class Test(unittest.TestCase):
    def perform_test(self, base):
        output = io.StringIO()
        ods2md.main(os.path.join('test', base + '.ods'), output)
        with open(os.path.join('test', base + '.md'), 'r') as f:
            self.assertMultiLineEqual(f.read(), output.getvalue())

    def test_sample(self):
        self.perform_test('sample')

    def test_padded(self):
        self.perform_test('padded')
