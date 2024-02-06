## Name: Manikumar Honnenahalli Lakshminarayana Swamy

## Project Description 
In this project, we aim to retrieve incident PDF reports from the Norman Police Department API. Subsequently, we will extract relevant data from the PDF files and organize it in a structured format within the normanpd database. 
The next phase involves printing a list of incident natures along with their respective occurrence frequencies in the console. 
The resulting list will be sorted based on the total number of incidents, followed by alphabetical sorting of incident natures.

## How to install and run
1. Create a virtual environment with pipenv using: **'pipenv shell'**.
2. Install all dependencies specified in the Pipfile by running: **'pipenv install'**. This command downloads all required dependencies.
3. Run the application using: **'pipenv run python assignment0/main.py --incidents {URL}'**. Replace <url> with the actual incidents URL.
4. To execute test cases and verify functionality, use the command: **'pipenv run python -m pytest'**.

## Video 
**[Video](https://drive.google.com/file/d/1ywBblwuHaP6bcoB-jQJiwSWJgMkbixCe/view?usp=sharing)**  - The demonstration video illustrates the steps for installing and running the application.

## Functions
#### main.py
1. **'fetchincidents(url)':** Takes a URL as a parameter, downloads incident data from the specified URL, creates a 'docs' directory if needed, and saves the data as 'downloaded_file.pdf'.
2. **'extractincidents(path)':** The extractincidents method utilizes the PyMuPDF library to parse PDF documents containing incident data. It iterates through each page, extracts text information, and groups the data into incidents. The resulting list of incident tuples includes relevant attributes, filtering out irrelevant information from the PDF.
3. **'createdb()':** The 'createdb' method employs the sqlite3 library to create an SQLite database. It uses the os library to check for the existence of a 'resources' directory and creates one if not present. The SQLite database, named 'normanpd.db', is then established within the 'resources' directory. The method returns the connection to the created database. In the event of any exceptions during the connection process, an error message is printed.
4. **'populatedb(db, incidents)':** The 'populatedb' method takes a database connection ('db') and incident data as parameters. It utilizes the connection to instantiate a cursor, which is then used to execute queries. Initially, the method creates a table named 'incidents' in the database with columns 'incident_time', 'incident_number', 'incident_location', 'nature', and 'incident_ori'. Subsequently, the provided incident data is stored in this table, and the changes are committed to the database.
5. **'status(db)':**  The 'status' method accepts a database connection ('db') and executes an SQL query on the 'incidents' table. It calculates the occurrence count for each unique nature of incidents, orders the results in descending order by count and then alphabetically by nature. The method prints the nature and occurrence count in the format "{nature}|{occurrence}". After processing, it ensures the closure of the database connection for proper resource management 

## Database Development
For effective management and analysis of incident data, the application relies on SQLite3 for database operations. Ensure that SQLite3 is installed on your system using the command sudo apt-get install sqlite3. The main code includes robust database development functionality, initializing with the creation of an SQLite database connection. This connection is established and configured within the 'resources' directory, ensuring proper isolation. Subsequently, the application creates the 'incidents' table within the database to structure the data. The populatedb function facilitates the insertion of incident information into this table, enabling efficient storage and retrieval. The status function retrieves and analyzes data from the 'incidents' table, generating insightful reports on incident occurrences.

## Test Cases
#### test_download.py
1. **test_extract():** This test function checks the accuracy of the extractincidents method. It loads a sample PDF file (tests/test_file.pdf), extracts incident data, and compares it with an expected dataset (expected_data). If the actual data matches the expected data, the test passes; otherwise, it fails.
2. **test_create_db_and_populate_data():** This test ensures the successful creation of the database (normanpd.db) and the removal of the resource folder. It uses the check_and_remove_resource_folder function and checks if the database file exists after calling the createdb method. If the file exists, the test passes, indicating the successful creation of the database.
3. **test_populate_data():** This test validates the populatedb method by inserting incident data into the database (con). It retrieves the first row from the incidents table and checks if the results are not None, indicating that the data has been successfully populated into the database.
4. **test_status():** This test function evaluates the correctness of the status method, which queries the database and retrieves a summary of incident data. The test compares the actual result with an expected dataset, asserting that they are equal. If not assertion will fail and eventually test case will fail.

#### test_extraction.py
1. **test_fetchincidents:** This test method simulates the download of a PDF file from a specified URL. It mocks the HTTP response and file handling, ensuring that the fetchincidents function correctly retrieves the PDF content and saves it to a local file. The test uses the patch decorator to replace the actual urllib.request.urlopen and open functions with mock implementations.

## Bugs and Assumptions
#### Bugs
1. **Fixed Column Coordinates:** The code uses fixed x-coordinates for each column. If the PDF layout changes or if the columns are not precisely aligned, this might lead to incorrect extraction. 
2. **Data Concatenation:** The code concatenates text data using + for each column. If the data is split across multiple lines or if there are formatting issues, this may lead to incorrect extraction

#### Assumptions
1. **Assumption about Column Order:** The code assumes a specific order for the columns based on their x-coordinates. As I fetch the data using the co-ordinates of blocks.
2. **Assumption about Grouping:** The code assumes that data with the same group number should be grouped together.

