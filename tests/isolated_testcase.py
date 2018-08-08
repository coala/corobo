import logging
import os

from errbot.backends.test import FullStackTest
from pathlib import Path


class IsolatedTestCase(FullStackTest):

    file_path = Path(__file__).parent / '..' / 'plugins' / 'labhub.plug'
    renamed_file_path = Path(__file__).parent / '..' / 'plugins' / 'hidden'

    @classmethod
    def setUpClass(cls, extra_config=None):
        os.rename(cls.file_path, cls.renamed_file_path)

    @classmethod
    def tearDownClass(cls):
        os.rename(cls.renamed_file_path, cls.file_path)

    def setUp(self, extra_config=None):
        super().setUp(extra_plugin_dir='plugins',
                      loglevel=logging.ERROR,
                      extra_config=extra_config)
