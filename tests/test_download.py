import unittest
from unittest.mock import patch, mock_open, Mock

from assignment0.main import fetchincidents


class TestFetchIncidents(unittest.TestCase):

    @patch('urllib.request.urlopen')
    @patch('builtins.open', new_callable=mock_open)
    def test_fetchincidents(self, mock_open, mock_urlopen):
        # Arrange
        url = 'https://example.com/incidents.pdf'
        mock_response = unittest.mock.Mock()
        mock_response.read.return_value = b'Test PDF content'
        mock_urlopen.return_value = mock_response

        # Act
        fetchincidents(url)
        # Assert
        mock_urlopen.assert_called_once_with(url)
        mock_open.assert_called_once_with('docs/downloaded_file.pdf', 'wb')
        mock_open().write.assert_called_once_with(b'Test PDF content')


if __name__ == '__main__':
    unittest.main()
