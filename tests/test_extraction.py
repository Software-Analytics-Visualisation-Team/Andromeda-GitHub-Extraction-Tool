import unittest
from unittest.mock import Mock
from utils import *
from extraction import *

class TestExtractionTool(unittest.TestCase):

    def test_is_valid_github_url(self):
        """
            Test is_valid_github_url method
        """
        # Test URL
        non_github_url = 'https://galaxyproject.org/'
        non_reachable_url = 'https://github.com/galaxy/moonshot-invalid-url'
        valid_github_url = 'https://github.com/Moonshot-SEP/files-for-AT'
        
        # Test invalid URL
        print('---testing non_github_url---')
        self.assertFalse(is_valid_github_url(non_github_url))
        # Test unreachable URL
        print('---testing non_reachable_url---')
        self.assertFalse(is_valid_github_url(non_reachable_url))
        # Test valid URL
        print('---testing valid_github_url---')
        self.assertTrue(is_valid_github_url(valid_github_url))

    def test_remove_readonly(self):
        """
            Test remove_readonly method
        """
        # Mock function
        mock_func = Mock()
        # Test directory
        test_path = 'tests/read-only'

        # Create a read-only directory
        if not os.path.exists(test_path):
            os.mkdir(test_path)
        os.chmod(test_path, stat.S_IREAD)

        # Call remove_readonly with 'onerror' exception information
        remove_readonly(mock_func, test_path, 'E')

        # Assert that test directory is writable
        print('---checking that file is writable---')
        self.assertTrue(os.access(test_path, os.W_OK))
        # Assert the calls
        print('---checking that function is called---')
        mock_func.assert_called()

    def test_extraction_tool(self):
        """
            Test extraction_tool method
        """
        # Test URL and destination
        repo_url = 'https://github.com/Moonshot-SEP/files-for-AT'
        test_dir = 'tests/'

        # Variables for testing
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        zip_dir = f'{test_dir}/{repo_name}'
        code_files_endings = ('.java', '.cpp', '.h', '.hpp', '.cs', '.py')

        # Run the method
        extraction_tool(repo_url, test_dir)

        # Check that a zip file of the repo is created
        print('---checking if zip file exists---')
        self.assertTrue(os.path.exists(f'{zip_dir}.zip'))

        # Unzip for testing
        shutil.unpack_archive(f'{zip_dir}.zip', zip_dir)

        # Traverse the repository
        for dirpath, dirnames, filenames in os.walk(zip_dir, topdown=True):
            # Check for .git directory
            print('---checking for .git directory---')
            self.assertFalse('.git' in dirnames, '.git found')
            # Check for non-code files
            print('---checking for non-code files---')
            for file in filenames:
                self.assertTrue(file.endswith(code_files_endings), f'{file} is not a code file')

if __name__ == '__main__':
    unittest.main()