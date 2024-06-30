from django.test import TestCase
from unittest.mock import patch, Mock, MagicMock

FILE_PATH = 'downloads/'
filename = 'test_File_name190224_ptm.pdf'
projectname = 'test_Projectname'


def create_file_path(file_name: str, project_name: str) -> str:
    new_file, file_extension = file_name.split(".")
    file_path = "{}/{}/{}.{}".format(
        FILE_PATH, project_name.replace(' ', '_'),
        new_file.replace(' ', '_'),
        file_extension
    )
    return file_path


mock_obj = Mock(spec='create_file_path', return_value="Test/file/path.pdf", name='test_mock')

# print(mock_obj)
# print(mock_obj())
# print(mock_obj.name)
