from concurrent.futures import ThreadPoolExecutor
import sqlite3
import logging
from typing import List
import requests
from bs4 import BeautifulSoup
from model import Patient

# -------------------------------------------------------
# Logging Configuration
# -------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler("patient_app.log"), logging.StreamHandler()],
)

# -------------------------------------------------------
# Database Connection & Table
# -------------------------------------------------------
def connect():
    """
    Establish connection to SQLite database.

    Returns:
        sqlite3.Connection: SQLite connection object.
    """
    try:
        con = sqlite3.connect("patient_app.db")
        return con
    except sqlite3.Error as e:
        logging.error("DB connection error: %s", e)
        raise


def patient_table_create():
    """
    Create patients table if it does not already exist.
    """
    sql = """CREATE TABLE IF NOT EXISTS patients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age TEXT NOT NULL,
        disease TEXT NOT NULL
    )"""
    try:
        with connect() as con:
            con.execute(sql)
            logging.info("Patients table created or already exists.")
    except Exception as e:
        logging.error("Error creating table: %s", e)


# -------------------------------------------------------
# CRUD Operations
# -------------------------------------------------------
def create_patient(patient: Patient):
    """
    Insert a new patient into the database.

    Args:
        patient (Patient): Patient object to insert.

    Returns:
        int: New patient ID if success, None otherwise.
    """
    sql = """INSERT INTO patients(name, age, disease) VALUES(?, ?, ?)"""
    params = (patient.name, patient.age, patient.disease)
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql, params)
            patient_id = cur.lastrowid
            con.commit()
            logging.info("Patient created: %s", patient)
            return patient_id
    except Exception as e:
        logging.error("Error creating patient: %s", e)
        return None


def read_all_patients() -> List[Patient]:
    """
    Retrieve all patients from the database.

    Returns:
        List[Patient]: List of Patient objects.
    """
    sql = "SELECT * FROM patients"
    try:
        with connect() as con:
            cur = con.cursor()
            rows = cur.execute(sql).fetchall()
            return [Patient(*row) for row in rows]
    except Exception as e:
        logging.error("Error fetching patients: %s", e)
        return []


def read_patient_by_id(patient_id: int):
    """
    Retrieve a patient by ID.

    Args:
        patient_id (int): Patient ID.

    Returns:
        Patient | None: Patient object if found, None otherwise.
    """
    sql = "SELECT * FROM patients WHERE id=?"
    try:
        with connect() as con:
            cur = con.cursor()
            row = cur.execute(sql, (patient_id,)).fetchone()
            return Patient(*row) if row else None
    except Exception as e:
        logging.error("Error fetching patient by id: %s", e)
        return None


def update_patient(patient: Patient):
    """
    Update patient details.

    Args:
        patient (Patient): Patient object with updated details.

    Returns:
        int: Number of rows updated.
    """
    sql = "UPDATE patients SET name=?, age=?, disease=? WHERE id=?"
    params = (patient.name, patient.age, patient.disease, patient.id)
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql, params)
            con.commit()
            return cur.rowcount
    except Exception as e:
        logging.error("Error updating patient: %s", e)
        return 0


def delete_patient(patient_id: int):
    """
    Delete a patient by ID.

    Args:
        patient_id (int): Patient ID.

    Returns:
        int: Number of rows deleted.
    """
    sql = "DELETE FROM patients WHERE id=?"
    try:
        with connect() as con:
            cur = con.cursor()
            cur.execute(sql, (patient_id,))
            con.commit()
            return cur.rowcount
    except Exception as e:
        logging.error("Error deleting patient: %s", e)
        return 0


# -------------------------------------------------------
# Web Scraping Interest Rates
# -------------------------------------------------------
def fetch_interest_rates():
    """
    Scrape interest rates from financial website.

    Returns:
        dict: Dictionary of rate names and values.
    """
    try:
        url = "https://www.investing.com/rates-bonds/"
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        rates = {}
        for row in soup.select("table tbody tr")[:5]:
            cols = row.find_all("td")
            if len(cols) >= 2:
                rates[cols[0].get_text(strip=True)] = cols[1].get_text(strip=True)

        logging.info("Fetched rates: %s", rates)
        return rates
    except Exception as e:
        logging.error("Error scraping rates: %s", e)
        return {}


# -------------------------------------------------------
# Multi-threaded Average Age Calculation
# -------------------------------------------------------
def calculate_batch_average_age(patients: List[Patient]):
    """
    Helper function: calculate average age of a batch.

    Args:
        patients (List[Patient]): Batch of patients.

    Returns:
        tuple: (sum of ages, count of valid ages) for the batch.
    """
    total_age = 0
    valid_count = 0
    for patient in patients:
        try:
            age = int(patient.age)  # Convert age string to integer
            total_age += age
            valid_count += 1
        except (ValueError, TypeError):
            logging.warning(f"Invalid age value for patient {patient.id}: {patient.age}")
    return total_age, valid_count


def calculate_average_age(batch_size=5):
    """
    Calculate average age across all patients using multi-threading.

    Args:
        batch_size (int): Number of patients per batch.

    Returns:
        float: Average age of patients, or None if no valid ages.
    """
    patients = read_all_patients()
    if not patients:
        logging.info("No patients found for average age calculation")
        return None

    total_age = 0
    total_count = 0
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(patients), batch_size):
            batch = patients[i : i + batch_size]
            futures.append(executor.submit(calculate_batch_average_age, batch))
        for f in futures:
            batch_total, batch_count = f.result()
            total_age += batch_total
            total_count += batch_count

    if total_count == 0:
        logging.info("No valid ages found for average calculation")
        return None
    average_age = total_age / total_count
    logging.info(f"Calculated average age: {average_age:.2f} from {total_count} valid patients")
    return average_age


def calculate_average_ages():
    """
    Calculate average age across all patients.

    Returns:
        float: Average age of patients, or None if no valid ages.
    """
    patients = read_all_patients()
    if not patients:
        logging.info("No patients found for average age calculation")
        return None

    total_age = 0
    valid_count = 0
    for patient in patients:
        try:
            age = int(patient.age)  # Convert age string to integer
            total_age += age
            valid_count += 1
        except (ValueError, TypeError):
            logging.warning(f"Invalid age value for patient {patient.id}: {patient.age}")

    if valid_count == 0:
        logging.info("No valid ages found for average calculation")
        return None
    average_age = total_age / valid_count
    logging.info(f"Calculated average age: {average_age:.2f} from {valid_count} valid patients")
    return average_age


# -------------------------------------------------------
# Seed Data
# -------------------------------------------------------
def seed_data():
    """
    Insert sample patients into the database for testing.
    """
    sample_patients = [
        {"name": "John Doe", "age": "45", "disease": "Hypertension"},
        {"name": "Jane Smith", "age": "32", "disease": "Diabetes"},
        {"name": "Alice Johnson", "age": "60", "disease": "Arthritis"},
        {"name": "Bob Brown", "age": "28", "disease": "Asthma"},
        {"name": "Charlie Davis", "age": "50", "disease": "Heart Disease"},
        {"name": "David Evans", "age": "19", "disease": "Allergies"},
        {"name": "Eve Foster", "age": "72", "disease": "Osteoporosis"},
        {"name": "Frank Green", "age": "35", "disease": "Migraine"},
        {"name": "Grace Harris", "age": "41", "disease": "Thyroid Disorder"},
        {"name": "Henry Irving", "age": "55", "disease": "Cancer"},
        {"name": "Ivy Jackson", "age": "29", "disease": "Anemia"},
        {"name": "Jack King", "age": "63", "disease": "COPD"},
    ]
    for patient in sample_patients:
        create_patient(Patient(name=patient["name"], age=patient["age"], disease=patient["disease"]))