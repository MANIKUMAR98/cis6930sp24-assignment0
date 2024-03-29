import argparse
import urllib.request
import shutil
import sqlite3
import os
import ssl
import fitz
import re

first_column = 52.560001373291016
second_column = 150.86000061035156
third_column = 229.82000732421875
fourth_column = 423.19000244140625
fifth_column = 623.8599853515625


def main(url):
    # it cleans the resource folder to avoid exception
    check_and_remove_resource_folder()

    path = "docs/downloaded_file.pdf"

    # Download data
    fetchincidents(url)

    # Extract data
    incidents = extractincidents(path)

    # Create new database
    db = createdb()

    # Insert data
    populatedb(db, incidents)

    # Print incident counts
    status(db)


def check_and_remove_resource_folder():
    if os.path.exists("resources"):
        shutil.rmtree("resources")
    if os.path.exists("docs"):
        shutil.rmtree("docs")


def fetchincidents(url):
    try:
        incident_data = urllib.request.urlopen(url)
        docs_dir = 'docs'
        if not os.path.exists(docs_dir):
            os.makedirs(docs_dir)
        path = os.path.join(docs_dir, "downloaded_file.pdf")
        with open(path, 'wb') as local_file:
            local_file.write(incident_data.read())
    except Exception as e:
        print(f"An error occurred while calling normanpd URL: {e}")


def extractincidents(path):
    try:
        doc = fitz.open(path)
        incidents = []
        incident = [''] * 5
        group_number = 0
        for page in doc:
            tuples = page.get_text('words')
            for data in tuples:
                current_number = data[5]
                if current_number == group_number:
                    add_data(incident, data)
                else:
                    text = incident[2]
                    if text.find("NORMAN POLICE DEPARTMENT") == -1 and text.find("Daily Incident Summary") == -1 and incident[0].find("Date / Time") == -1:
                        incidents.append(tuple(incident))
                    incident = [''] * 5
                    add_data(incident, data)
                    group_number = current_number

        date_pattern = re.compile(r'\b\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}\b')
        if not date_pattern.search(incident[2]):
            incidents.append(incident)
        return incidents
    except Exception as e:
        print(f"An error occurred while parsing PDF: {e}")


def add_data(incident, data):
    coordinate = data[0]
    text = data[4]
    if coordinate == first_column or coordinate < second_column:
        incident[0] = incident[0] + " " + text if incident[0] else text
    elif coordinate == second_column or coordinate < third_column:
        incident[1] = incident[1] + " " + text if incident[1] else text
    elif coordinate == third_column or coordinate < fourth_column:
        incident[2] = incident[2] + " " + text if incident[2] else text
    elif coordinate == fourth_column or coordinate < fifth_column:
        incident[3] = incident[3] + " " + text if incident[3] else text
    else:
        incident[4] = incident[4] + " " + text if incident[4] else text


def createdb():
    try:
        resources_dir = 'resources'
        if not os.path.exists(resources_dir):
            os.makedirs(resources_dir)
        con = sqlite3.connect(os.path.join(resources_dir, "normanpd.db"))
        return con
    except Exception as e:
        print("Exception Occurred while connecting to SQLLite ", e)


def populatedb(db, incident_data):
    cur = db.cursor()
    db.execute(
        "CREATE TABLE incidents (incident_time TEXT, incident_number TEXT, incident_location TEXT, nature TEXT, incident_ori TEXT);")
    cur.executemany("INSERT INTO incidents VALUES(?, ?, ?, ?, ?)", incident_data)
    db.commit()
    return


def status(db):
    cursor = db.cursor()
    cursor.execute(
        "SELECT nature, COUNT(*) as occurrence FROM incidents GROUP BY nature ORDER BY occurrence DESC, nature;")
    results = cursor.fetchall()
    for nature, occurrence in results:
        print(f"{nature}|{occurrence}")
    db.close()
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--incidents", type=str, required=True,
                        help="Incident summary url.")

    args = parser.parse_args()
    if args.incidents:
        main(args.incidents)
