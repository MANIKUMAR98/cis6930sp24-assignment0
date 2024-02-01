import argparse
import urllib.request
import shutil
import sqlite3
import re
import os
import ssl
from pypdf import PdfReader


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
        print(f"An error occurred: {e}")


def extractincidents(path):
    reader = PdfReader(path)
    pages = reader.pages
    incidents = []
    for page in pages:
        data = page.extract_text(extraction_mode="layout")
        for line in data.splitlines():
            line = line.strip()
            if line and line.find("Incident Number") == -1 and line.find("NORMAN POLICE DEPARTMENT") == -1 and line.find("Daily Incident Summary") == -1:
                res = re.split(r'\s{3,}', line)
                if len(res) == 1 and len(incidents) > 0 and res[0].isupper():
                    last_tuple = incidents[-1]
                    new_list = list(last_tuple)
                    new_list[2] = new_list[2] + " " + res[0]
                    incidents.pop()
                    incidents.append(tuple(new_list))
                if len(res) == 5:
                    incidents.append(tuple(res))
    return incidents


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
        "SELECT nature, COUNT(*) as occurrence FROM incidents GROUP BY nature ORDER BY occurrence DESC, nature")
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
