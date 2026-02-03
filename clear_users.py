from app import create_app, db
from app.models import User, Doctor, Patient, Consultation, LabReport, Prescription, MedicalRecord, LabRequest

app = create_app()

def clear_users():
    with app.app_context():
        print("Starting cleanup...")
        
        # 1. Clear dependent tables first
        print("Clearing Lab Requests...")
        try:
            db.session.query(LabRequest).delete()
            db.session.commit()
        except:
            db.session.rollback()

        print("Clearing Medical Records...")
        try:
            db.session.query(MedicalRecord).delete()
            db.session.commit()
        except:
            db.session.rollback()

        print("Clearing Prescriptions...")
        try:
            db.session.query(Prescription).delete()
            db.session.commit()
        except:
            db.session.rollback()

        print("Clearing Lab Reports...")
        try:
             # LabReports might reference Consultations, so we clear them before Consultations if needed, or after?
             # Foreign keys: LabReport -> Consultation (nullable). Consultation -> LabRequests? No.
             # LabRequest -> LabReport (nullable).
             # We deleted LabRequest first. Now LabReport.
            db.session.query(LabReport).delete()
            db.session.commit()
        except:
            db.session.rollback()

        print("Clearing Consultations...")
        try:
            db.session.query(Consultation).delete()
            db.session.commit()
        except:
            db.session.rollback()

        # 2. Clear Profiles
        print("Clearing Patients...")
        try:
            db.session.query(Patient).delete()
            db.session.commit()
        except:
            db.session.rollback()

        print("Clearing Doctors...")
        try:
            db.session.query(Doctor).delete()
            db.session.commit()
        except:
            db.session.rollback()

        # 3. Clear Users (only patients and doctors)
        print("Clearing Users (Patients and Doctors)...")
        try:
            deleted_users = db.session.query(User).filter(User.role.in_(['patient', 'doctor'])).delete(synchronize_session=False)
            db.session.commit()
            print(f"Deleted {deleted_users} users.")
        except Exception as e:
            print(f"Error deleting users: {e}")
            db.session.rollback()
            
        print("Cleanup complete!")

if __name__ == "__main__":
    clear_users()
