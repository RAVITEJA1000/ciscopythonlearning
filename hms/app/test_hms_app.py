import unittest
import sqlite3
from db_services import create_patient, read_all_patients, read_patient_by_id, delete_patient, calculate_average_age
from model import Patient

class TestPatientApp(unittest.TestCase):
    def setUp(self):
        """Set up an in-memory SQLite database for testing."""
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age TEXT NOT NULL,
                disease TEXT NOT NULL
            )
        """)
        self.conn.commit()

        # Patch db_services to use the in-memory database
        def mocked_connect():
            return self.conn
        import db_services
        db_services.connect = mocked_connect

    def tearDown(self):
        """Close the in-memory database connection."""
        self.conn.close()

    def test_read_all_patients_empty(self):
        """Test fetching all patients when database is empty."""
        patients = read_all_patients()
        self.assertEqual(len(patients), 0, "Empty database should return 0 patients")

    def test_create_and_read_patient(self):
        """Test creating and fetching a patient by ID."""
        # Create a patient
        patient = Patient(name="John Doe", age="45", disease="Hypertension")
        patient_id = create_patient(patient)
        self.assertIsNotNone(patient_id, "Patient ID should not be None")

        # Fetch the patient by ID
        retrieved = read_patient_by_id(patient_id)
        self.assertIsNotNone(retrieved, "Patient should be retrieved")
        self.assertEqual(retrieved.id, patient_id, "Patient ID should match")
        self.assertEqual(retrieved.name, "John Doe", "Name should match")
        self.assertEqual(retrieved.age, "45", "Age should match")
        self.assertEqual(retrieved.disease, "Hypertension", "Disease should match")

        # Test non-existent ID
        retrieved_non_existent = read_patient_by_id(999)
        self.assertIsNone(retrieved_non_existent, "Non-existent ID should return None")

    def test_delete_patient(self):
        """Test deleting a patient."""
        patient = Patient(name="Jane Smith", age="32", disease="Diabetes")
        patient_id = create_patient(patient)
        self.assertIsNotNone(patient_id, "Patient ID should not be None")

        rows_deleted = delete_patient(patient_id)
        self.assertEqual(rows_deleted, 1, "One patient should be deleted")
        self.assertIsNone(read_patient_by_id(patient_id), "Deleted patient should not be found")

        # Test deleting non-existent patient
        self.assertEqual(delete_patient(999), 0, "Deleting non-existent patient should affect 0 rows")

    def test_calculate_average_age(self):
        """Test calculating the average age of patients."""
        # Create test patients
        patients = [
            Patient(name="John Doe", age="45", disease="Hypertension"),
            Patient(name="Jane Smith", age="32", disease="Diabetes"),
            Patient(name="Alice Johnson", age="60", disease="Arthritis"),
            Patient(name="Invalid Age", age="invalid", disease="Asthma")
        ]
        for patient in patients:
            create_patient(patient)

        # Calculate average age
        average_age = calculate_average_age()
        expected_average = (45 + 32 + 60) / 3  # Only valid ages are counted
        self.assertAlmostEqual(average_age, expected_average, places=2, msg="Average age should match expected value")

        # Test with empty database
        self.cursor.execute("DELETE FROM patients")
        self.conn.commit()
        self.assertIsNone(calculate_average_age(), "Average age should be None for empty database")

if __name__ == '__main__':
    unittest.main()