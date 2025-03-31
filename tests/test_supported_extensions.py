import unittest
from parsethisio import get_supported_extensions

class TestSupportedExtensions(unittest.TestCase):
    def test_supported_extensions(self):
        # Get all supported extensions
        exts = get_supported_extensions()
        
        # Verify expected extensions are present
        self.assertIn('.pdf', exts)  # PDFParser
        self.assertIn('.jpg', exts)  # ImageParser
        self.assertIn('.png', exts)  # ImageParser
        self.assertIn('.mp3', exts)  # AudioParser
        self.assertIn('.txt', exts)  # TextParser
        
        # Verify extensions are properly formatted
        for ext in exts:
            self.assertTrue(ext.startswith('.'), f"Extension {ext} should start with a dot")
