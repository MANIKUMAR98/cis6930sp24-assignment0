from assignment0.main import extractincidents, check_and_remove_resource_folder, createdb, populatedb, status
import os

con = None
incident_data = None


def test_extract():
    expected_data = ('12/17/2023 0:01', '2023-00025122', '901 N PORTER AVE', 'Transfer/Interfacility', 'EMSSTAT')
    global incident_data
    incident_data = extractincidents("tests/test_file.pdf")
    actual_data = incident_data[0]
    if expected_data == actual_data:
        assert True
    else:
        assert False


def test_create_db_and_populate_data():
    check_and_remove_resource_folder()
    global con
    con = createdb()
    if os.path.exists("resources/normanpd.db"):
        assert True
    else:
        assert False


def test_populate_data():
    populatedb(con, incident_data)
    cursor = con.cursor()
    cursor.execute(
        "SELECT * FROM incidents LIMIT 1")
    results = cursor.fetchall()
    if results is not None:
        assert True
    else:
        assert False


def test_status():
    results = status(con)
    if results is not None:
        assert True
    else:
        assert False
