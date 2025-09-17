from flask import Flask, request, jsonify
from emailer import send_gmail
import db_services
import logging
from datetime import datetime
import os
import json
import random
from model import Patient

# Create with mail <Done>, Fetch all <Done>, Fetch by id <Done>, Update by id <Done>, Delete by id <Done>, Fetch scraper data <Done> 

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('patient_app.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
# db_services.patient_table_create()

'''
Retrieve all patients from the database.

This endpoint returns a list of all patients in the database.

Returns:
    Response: A JSON array of patient objects, each containing:
        - id (int): The unique identifier of the patient.
        - name (str): The name of the patient.
        - age (str): The age of the patient.
        - disease (str): The disease of the patient.
'''
@app.route("/patients", methods=['GET'])
def read_all_patients():
    patient_objects = db_services.read_all_patients()
    patients = []
    for patient_obj in patient_objects:
        patient = {
            'id': patient_obj.id,
            'name': patient_obj.name,
            'age': patient_obj.age,
            'disease': patient_obj.disease
        }
        patients.append(patient)
    return jsonify(patients)

"""
Create a new patient in the database.

This endpoint accepts a JSON object containing the details of the patient to be created,
adds it to the database, and sends a notification email.

Request Body:
    JSON object containing:
        - name (str): The name of the patient.
        - age (str): The age of the patient.
        - disease (str): The disease of the patient.

Returns:
    Response: A JSON object representing the created patient, containing:
        - id (int): The unique identifier of the created patient.
        - name (str): The name of the patient.
        - age (str): The age of the patient.
        - disease (str): The disease of the patient.
"""
@app.route("/patients", methods=['POST'])
def create_patient_endpoint():
    patient_data = request.get_json()
    patient_id = db_services.create_patient(Patient(
        name=patient_data['name'],
        age=patient_data['age'],
        disease=patient_data['disease']
    ))
    if patient_id is None:
        return jsonify({"error": "Failed to create patient"}), 500
    
    created_patient = db_services.read_patient_by_id(patient_id)
    saved_patient = {
        'id': created_patient.id,
        'name': created_patient.name,
        'age': created_patient.age,
        'disease': created_patient.disease
    }
    
    # Send email notification
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    subject = f"Patient Record Created at {now_str}"
    body = f"A new patient record has been created:\nName: {patient_data['name']}\nAge: {patient_data['age']}\nDisease: {patient_data['disease']}"
    send_gmail("inahpm7@gmail.com", subject, body)
    
    return jsonify(saved_patient), 201

"""
Retrieve a patient by their ID.

This endpoint returns the details of a specific patient identified by their ID.

Args:
    id (int): The unique identifier of the patient to be retrieved.

Returns:
    Response: A JSON object representing the patient, containing:
        - id (int): The unique identifier of the patient.
        - name (str): The name of the patient.
        - age (str): The age of the patient.
        - disease (str): The disease of the patient.
"""
@app.route("/patients/<int:patient_id>", methods=['GET'])
def read_patient_by_id_endpoint(patient_id):
    patient_obj = db_services.read_patient_by_id(patient_id)
    if patient_obj is None:
        return jsonify({"error": "Patient not found"}), 404
    patient = {
        'id': patient_obj.id,
        'name': patient_obj.name,
        'age': patient_obj.age,
        'disease': patient_obj.disease
    }
    return jsonify(patient)

"""
Update the details of an existing patient.

This endpoint updates the details of a patient identified by their ID.

Args:
    id (int): The unique identifier of the patient to be updated.
    Request Body:
        JSON object containing:
            - name (str): The new name of the patient.
            - age (str): The new age of the patient.
            - disease (str): The new disease of the patient.

Returns:
    Response: A JSON object representing the updated patient, containing:
        - id (int): The unique identifier of the patient.
        - name (str): The name of the patient.
        - age (str): The age of the patient.
        - disease (str): The disease of the patient.
"""
@app.route("/patients/<int:patient_id>", methods=['PUT'])
def update_patient_endpoint(patient_id):
    patient_data = request.get_json()
    updated_patient = Patient(
        id=patient_id,
        name=patient_data['name'],
        age=patient_data['age'],
        disease=patient_data['disease']
    )
    rows_updated = db_services.update_patient(updated_patient)
    if rows_updated == 0:
        return jsonify({"error": "Patient not found or update failed"}), 404
    
    updated_obj = db_services.read_patient_by_id(patient_id)
    saved_patient = {
        'id': updated_obj.id,
        'name': updated_obj.name,
        'age': updated_obj.age,
        'disease': updated_obj.disease
    }
    return jsonify(saved_patient)

"""
Delete a patient by their ID.

This endpoint removes a patient from the database identified by their ID.

Args:
    id (int): The unique identifier of the patient to be deleted.

Returns:
    Response: A JSON object containing a message indicating the result of the deletion.
        Example:
            {"message": "Patient with ID 5 has been deleted."}
"""
@app.route("/patients/<int:patient_id>", methods=['DELETE'])
def delete_patient_endpoint(patient_id):
    rows_deleted = db_services.delete_patient(patient_id)
    if rows_deleted == 0:
        return jsonify({"error": "Patient not found"}), 404
    return jsonify({"message": f"Patient with ID {patient_id} has been deleted."}), 200

"""
Endpoint to fetch interest rates.

Returns:
    Response: A JSON object containing the fetched interest rates.
"""
@app.route("/patients/scraped", methods=['GET'])
def get_scraped_data():
    try:
        json_file_path = "./patient_app/scraped_diseases.json"
        if not os.path.exists(json_file_path):
            logging.error(f"Scraped JSON file not found: {json_file_path}")
            return jsonify({'error': 'Scraped JSON file not found'}), 404
        
        with open(json_file_path, 'r', encoding='utf-8') as file:
            rates = json.load(file)
        
        logging.info("Successfully retrieved scraped interest rates")
        return jsonify(rates), 200
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON format in {json_file_path}: {str(e)}")
        return jsonify({'error': 'Invalid JSON format'}), 500
    except Exception as e:
        logging.error(f"Error fetching interest rates: {str(e)}")
        return jsonify({'error': str(e)}), 500
    

'''
Endpoint to get the average age of all patients.
'''
@app.route("/patients/average-age", methods=['GET'])
def get_average_age():
    try:
        average_age = db_services.calculate_average_ages()
        if average_age is None:
            logging.error("No valid ages found for average calculation")
            return jsonify({'error': 'No valid ages found', 'patient_count': 0}), 404
        
        # Fetch patient count for additional context
        patients = db_services.read_all_patients()
        valid_count = sum(1 for patient in patients if is_valid_age(patient.age))
        response = {
            'average_age': round(average_age, 2),
            'patient_count': valid_count,
            'total_patients': len(patients)
        }
        logging.info(f"Calculated average age: {average_age:.2f} for {valid_count}/{len(patients)} patients")
        return jsonify(response), 200
    except Exception as e:
        logging.error(f"Error calculating average age: {str(e)}")
        return jsonify({'error': str(e), 'patient_count': 0}), 500

def is_valid_age(age):
    """Helper function to check if age is valid for calculation."""
    try:
        int(age)
        return True
    except (ValueError, TypeError):
        return False

def crud_operations():
    app.run(debug=True)