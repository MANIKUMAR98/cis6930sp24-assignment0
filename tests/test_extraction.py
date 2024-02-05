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
    expected_data = [('Traffic Stop', 79), ('Transfer/Interfacility', 24), ('Contact a Subject', 18), ('Alarm', 15), ('Sick Person', 14), ('Disturbance/Domestic', 12), ('Larceny', 12), ('Welfare Check', 12), ('Falls', 11), ('Check Area', 8), ('MVA With Injuries', 8), ('Runaway or Lost Child', 7), ('Suspicious', 7), ('Breathing Problems', 6), ('Chest Pain', 6), ('Convulsion/Seizure', 6), ('Motorist Assist', 5), ('Public Assist', 5), ('Stolen Vehicle', 5), ('Stroke', 5), ('911 Call Nature Unknown', 4), ('Diabetic Problems', 4), ('Follow Up', 4), ('Trespassing', 4), ('Unconscious/Fainting', 4), ('Assist Police', 3), ('Barking Dog', 3), ('Burglary', 3), ('Harassment / Threats Report', 3), ('Medical Call Pd Requested', 3), ('Noise Complaint', 3), ('Assault', 2), ('Back Pain', 2), ('COP Problem Solving', 2), ('Drunk Driver', 2), ('Escort/Transport', 2), ('Fire Residential', 2), ('Found Item', 2), ('Heart Problems/AICD', 2), ('Hemorrhage/Lacerations', 2), ('Hit and Run', 2), ('Open Door/Premises Check', 2), ('Overdose/Poisoning', 2), ('Reckless Driving', 2), ('Supplement Report', 2), ('Animal Injured', 1), ('COP Relationships', 1), ('Civil Standby', 1), ('Extra Patrol', 1), ('Fire Alarm', 1), ('Fire Gas Leak', 1), ('Fire Smoke Investigation', 1), ('Foot Patrol', 1), ('Loud Party', 1), ('MVA Non Injury', 1), ('Pick Up Items', 1), ('Public Intoxication', 1), ('Stake Out', 1)]
    actual = status(con)
    if expected_data == actual:
        assert True
    else:
        assert False
