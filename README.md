## Name: Manikumar Honnenahalli Lakshminarayana Swamy

## Project Description 
In this project, we aim to retrieve incident PDF reports from the Norman Police Department API. Subsequently,
we will extract relevant data from the PDF files and organize it in a structured format within the normanpd database. 
The next phase involves printing a list of incident natures along with their respective occurrence frequencies in the console. 
The resulting list will be sorted based on the total number of incidents, followed by alphabetical sorting of incident natures.

## How to install and run
1. Install pyenv to manage Python versions using the command: **'curl https://pyenv.run | bash'**.
2. Install a specific Python version with the command: **'pyenv install {PYTHON_VERSION}'**.
3. Set the global Python version using: **'pyenv global {PYTHON_VERSION}'**.
4. Install pipenv, a dependency manager, with the command: **'pip install pipenv'**.
5. Install SQLite3 for database management using: **'sudo apt install sqlite3'**.
6. Create a virtual environment with pipenv using: **'pipenv shell'**.
7. Install all dependencies specified in the Pipfile by running: **'pipenv install'**. This command downloads all required dependencies.
8. Run the application using: **'pipenv run python assignment0/main.py --incidents <url>'**. Replace <url> with the actual incidents URL.
9. To execute test cases and verify functionality, use the command: **'pipenv run python -m pytest'**.

## Functions
#### main.py
1. **'fetchincidents(url)'** - Takes a URL as a parameter, downloads incident data from the specified URL, creates a 'docs' directory if needed, and saves the data as 'downloaded_file.pdf'.
2. **'extractincidents(path)'** - Takes a path where the incident file downloaded, And it parses the 'downloaded_file.pdf,' stored in the 'docs' folder using PdfReader, extracts text data from its pages with a layout-based mode, processes the lines, and filters out those containing "Incident Number". It splits the remaining lines based on multiple whitespaces and appends tuples with five elements to the 'incidents' list. The function returns a list of incident tuples.
3. **'createdb()'** - The 'createdb' method employs the sqlite3 library to create an SQLite database. It uses the os library to check for the existence of a 'resources' directory and creates one if not present. The SQLite database, named 'normanpd.db', is then established within the 'resources' directory. The method returns the connection to the created database. In the event of any exceptions during the connection process, an error message is printed.
4. **'populatedb(db, incidents)'** - The 'populatedb' method takes a database connection ('db') and incident data as parameters. It utilizes the connection to instantiate a cursor, which is then used to execute queries. Initially, the method creates a table named 'incidents' in the database with columns 'incident_time', 'incident_number', 'incident_location', 'nature', and 'incident_ori'. Subsequently, the provided incident data is stored in this table, and the changes are committed to the database.
5. **'status(db)'** - the 'status' method accepts a database connection ('db') and executes an SQL query on the 'incidents' table. It calculates the occurrence count for each unique nature of incidents, orders the results in descending order by count and then alphabetically by nature. The method prints the nature and occurrence count in the format "nature|occurrence". After processing, it ensures the closure of the database connection for proper resource management 

## Database Development
For effective management and analysis of incident data, the application relies on SQLite3 for database operations. Ensure that SQLite3 is installed on your system using the command sudo apt-get install sqlite3. The main code includes robust database development functionality, initializing with the creation of an SQLite database connection. This connection is established and configured within the 'resources' directory, ensuring proper isolation. Subsequently, the application creates the 'incidents' table within the database to structure the data. The populatedb function facilitates the insertion of incident information into this table, enabling efficient storage and retrieval. The status function retrieves and analyzes data from the 'incidents' table, generating insightful reports on incident occurrences.

## Bugs and Assumptions
#### Bugs
1. **Hardcoded File Paths:** The paths to files and directories (e.g., 'docs/downloaded_file.pdf', 'resources/normanpd.db') are hardcoded. This might lead to issues if the directory structure changes.
2. **Exception Handling:** The except Exception as e in the fetchincidents and createdb functions prints an error message but doesn't log or handle the exception further. A more robust exception handling mechanism can be implemented.

#### Assumptions1
1. **Location in Incident report** - I am assuming the characters in the Location column will always be capitalized.
2. **PDF Structure and Layout Mode:** - The extractincidents function assumes a specific structure in the PDF content, particularly relying on the layout mode ("layout" specified in extraction_mode="layout"). The regular expression used to split lines assumes a minimum of three spaces (\s{3,}) between elements. This assumes that the layout mode ensures sufficient space between words for accurate splitting. Any changes in the PDF structure or layout mode may necessitate adjustments to the regex for proper extraction.