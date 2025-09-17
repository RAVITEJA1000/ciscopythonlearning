from db_services import create_patient, read_all_patients, read_patient_by_id, update_patient, delete_patient, calculate_average_age
from emailer import send_gmail
from model import Patient
from datetime import datetime
import json

def menu():
    message = '''
The menu choices are:
1 - Create Patient
2 - Read All Patients
3 - Read Patient by ID
4 - Update Patient
5 - Delete Patient
6 - View Scraped Disease Information
7 - Calculate Average Patient Age
8 - Exit / Logout
Your choice: '''
    try:
        choice = int(input(message))
        print(choice)
        if choice == 1:
            name = input('Name: ')
            age = input('Age: ')
            disease = input('Disease: ')
            patient_dict = {'name': name, 'age': age, 'disease': disease}
            patient_id = create_patient(Patient(name=name, age=age, disease=disease))
            if patient_id is None:
                print('Failed to create patient.')
            else:
                # Email notification
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                subject = f"Patient Record Created at {now_str}"
                body = f"A new patient record has been created:\nName: {name}\nAge: {age}\nDisease: {disease}"
                try:
                    send_gmail("inahpm7@gmail.com", subject, body)
                    print('Email notification sent successfully.')
                except Exception as e:
                    print(f'Failed to send email notification: {e}')
                print('Patient created successfully.', patient_dict)
        elif choice == 2:
            patients = read_all_patients()
            if not patients:
                print('No patients found.')
            else:
                print('Patients:')
                for patient in patients:
                    print(f"ID: {patient.id}, Name: {patient.name}, Age: {patient.age}, Disease: {patient.disease}")
        elif choice == 3:
            patient_id = int(input('Patient ID: '))
            patient = read_patient_by_id(patient_id)
            if patient is None:
                print('Patient not found.')
            else:
                print(f"ID: {patient.id}, Name: {patient.name}, Age: {patient.age}, Disease: {patient.disease}")
        elif choice == 4:
            patient_id = int(input('Patient ID: '))
            old_patient = read_patient_by_id(patient_id)
            if old_patient is None:
                print('Patient not found.')
            else:
                print(f"Current: ID: {old_patient.id}, Name: {old_patient.name}, Age: {old_patient.age}, Disease: {old_patient.disease}")
                user_input = input(f"Want to update the Name ({old_patient.name}): (T|F) ").strip().lower()
                new_name = input("Name: ") if user_input != "f" else old_patient.name
                user_input = input(f"Want to update the Age ({old_patient.age}): (T|F) ").strip().lower()
                new_age = input("Age: ") if user_input != "f" else old_patient.age
                user_input = input(f"Want to update the Disease ({old_patient.disease}): (T|F) ").strip().lower()
                new_disease = input("Disease: ") if user_input != "f" else old_patient.disease
                updated_patient = Patient(id=old_patient.id, name=new_name, age=new_age, disease=new_disease)
                rows_updated = update_patient(updated_patient)
                if rows_updated == 0:
                    print('Patient update failed.')
                else:
                    print('Patient updated successfully.')
        elif choice == 5:
            patient_id = int(input('Patient ID: '))
            old_patient = read_patient_by_id(patient_id)
            if old_patient is None:
                print('Patient not found.')
            else:
                print(f"Patient: ID: {old_patient.id}, Name: {old_patient.name}, Age: {old_patient.age}, Disease: {old_patient.disease}")
                if input('Are you sure to delete (y/n)? ').lower() == 'y':
                    rows_deleted = delete_patient(patient_id)
                    if rows_deleted == 0:
                        print('Patient deletion failed.')
                    else:
                        print('Patient deleted successfully.')
        elif choice == 6:
            try:
                with open("./patient_app/scraped_diseases.json", 'r', encoding='utf-8') as file:
                    diseases = json.load(file)
                if not diseases:
                    print("No disease information found in the file.")
                else:
                    print('Disease Information (JSON Contents):')
                    print(json.dumps(diseases, indent=2))
            except FileNotFoundError:
                print("Scraped disease file not found. Please scrape disease information first.")
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in scraped disease file.")
            except Exception as e:
                print(f"Error reading disease information: {e}")
        elif choice == 7:
            average_age = calculate_average_age()
            if average_age is None:
                print("No valid ages found for average calculation.")
            else:
                print(f"Average Patient Age: {average_age:.2f}")
        return choice
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 8.")
        return None

def menus():
    print('***************Patient Management App***************')
    choice = menu()
    while choice != 8:
        choice = menu()
    print('Thank you for using the app')

