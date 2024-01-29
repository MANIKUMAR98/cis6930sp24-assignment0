import unittest
from unittest.mock import patch, mock_open, Mock

from assignment0.main import fetchincidents, extractincidents, createdb, status


class TestFetchIncidents(unittest.TestCase):

    @patch('urllib.request.urlopen')
    @patch('builtins.open', new_callable=mock_open)
    def test_fetchincidents_success(self, mock_open, mock_urlopen):
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

    @patch('assignment0.main.PdfReader')
    def test_extractincidents(self, mock_pdf_reader):
        # Create a mock PdfReader object
        mock_pdf_reader_instance = mock_pdf_reader.return_value
        mock_pdf_reader_instance.pages = [Mock()]

        # Set up the mock PdfReader with one page
        mock_page = mock_pdf_reader_instance.pages[0]

        # Mock the extract_text method to return a string with newline characters
        mock_page.extract_text.side_effect = [
            "NORMAN POLICE DEPARTMENT\nDate / Time   Incident Number   Location   Nature    Incident ORI\n1/1/2024 0:01   2024-00000001    "
            "3603 N FLOOD AVE    Traffic Stop    OK0140200\n1/2/2024 10:25"
        ]

        # Call the extractincidents method
        with patch('builtins.open', unittest.mock.mock_open(read_data="")):
            result = extractincidents()
        # Assert the result
        expected_result = [
            ("1/1/2024 0:01", "2024-00000001", "3603 N FLOOD AVE", "Traffic Stop", "OK0140200")
        ]
        self.assertEqual(result, expected_result)

        # Assert that PdfReader was called with the correct file path
        mock_pdf_reader.assert_called_once_with("docs/downloaded_file.pdf")

        # Assert that Page.extract_text was called once
        mock_page.extract_text.assert_called_once_with(extraction_mode="layout")

    @patch('assignment0.main.sqlite3.connect')
    def test_createdb_success(self, mock_sqlite_connect):
        # Arrange
        mock_connection = Mock()
        mock_sqlite_connect.return_value = mock_connection

        # Act
        result = createdb()

        # Assert
        # Check if sqlite3.connect was called with the correct argument
        mock_sqlite_connect.assert_called_once_with("resources/normanpd.db")

        # Check if the result is an instance of sqlite3.Connection
        self.assertIsInstance(result, Mock)
        self.assertIsInstance(result, mock_connection.__class__)

    @patch('assignment0.main.sqlite3.connect', side_effect=Exception("Connection Error"))
    def test_createdb_exception(self, mock_sqlite_connect):
        # Act
        result = createdb()

        # Assert
        # Check if sqlite3.connect was called with the correct argument
        mock_sqlite_connect.assert_called_once_with("resources/normanpd.db")

        # Check if the result is None when an exception occurs
        self.assertIsNone(result)

    @patch('assignment0.main.sqlite3.connect')
    def test_status_success(self, mock_sqlite_connect):
        # Arrange
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connection.cursor.return_value = mock_cursor
        mock_sqlite_connect.return_value = mock_connection

        # Expected SQL query
        expected_query = "SELECT nature, COUNT(*) as occurrence FROM incidents GROUP BY nature ORDER BY occurrence DESC, nature"

        # Expected result from the database
        mock_results = [('Abdominal Pains/Problems', 100), ('Cough', 10), ('Sneeze', 20)]

        # Configure the mock cursor to return the expected results
        mock_cursor.fetchall.return_value = mock_results

        # Capture the print output
        with patch('builtins.print') as mock_print:
            # Act
            status(mock_connection)

            # Assert
            # Check if the cursor executed the expected SQL query
            mock_cursor.execute.assert_called_once_with(expected_query)

            # Check if the print output matches the expected result for each call
            mock_print.assert_has_calls(
                [unittest.mock.call(f"{nature}|{occurrence}") for nature, occurrence in mock_results])

            # Check if the print function was called the expected number of times
            expected_print_calls = [unittest.mock.call(f"{nature}|{occurrence}") for nature, occurrence in mock_results]
            mock_print.assert_has_calls(expected_print_calls)
            self.assertEqual(mock_print.call_count, len(expected_print_calls))


if __name__ == '__main__':
    unittest.main()
