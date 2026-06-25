# patients.py

# Fake patient database — simulates a real hospital EHR system

PATIENTS = {


"P001": {
    "name": "Ramesh Kumar",
    "age": 70,
    "disease": "Chronic Kidney Disease",
    "doctor": "Dr. Aryant Pratap Singh",
    "history": "Diagnosed with CKD Stage 3 in 2022. On dialysis since 2023. Takes lisinopril and furosemide. Last follow-up March 2026."
},

"P002": {
    "name": "Sunita Devi",
    "age": 63,
    "disease": "Kidney Stone",
    "doctor": "Dr. Aryant Pratap Singh",
    "history": "Recurrent renal calculi since 2024. Underwent ureteroscopic stone removal. Advised hydration and periodic ultrasound."
},

"P003": {
    "name": "Amit Singh",
    "age": 61,
    "disease": "Coronary Artery Disease",
    "doctor": "Dr. Vaibhav Yadav",
    "history": "Underwent angioplasty in 2025. On aspirin, atorvastatin and beta blockers. Stable condition."
},

"P004": {
    "name": "Rajesh Tiwari",
    "age": 58,
    "disease": "Benign Prostatic Hyperplasia",
    "doctor": "Dr. Aryant Pratap Singh",
    "history": "Complaints of frequent urination and nocturia since 2024. Ultrasound showed enlarged prostate. On tamsulosin therapy."
},

"P005": {
    "name": "Vikas Pandey",
    "age": 66,
    "disease": "Heart Failure",
    "doctor": "Dr. Vaibhav Yadav",
    "history": "Diagnosed with reduced ejection fraction heart failure in 2025. On beta blockers and diuretics."
},

"P006": {
    "name": "Anjali Mishra",
    "age": 49,
    "disease": "Hypertension",
    "doctor": "Dr. Rahul Singh",
    "history": "Blood pressure elevated for 5 years. Taking amlodipine and telmisartan."
},

"P007": {
    "name": "Saurabh Singh",
    "age": 42,
    "disease": "Migraine",
    "doctor": "Dr. Tej Pratap",
    "history": "Recurring migraine attacks for 8 years. Triggered by stress and lack of sleep."
},

"P008": {
    "name": "Neha Gupta",
    "age": 55,
    "disease": "Epilepsy",
    "doctor": "Dr. Tej Pratap",
    "history": "Diagnosed in 2021 after recurrent seizure episodes. Controlled on levetiracetam."
},

"P009": {
    "name": "Ashutosh Yadav",
    "age": 61,
    "disease": "Lumbar Disc Herniation",
    "doctor": "Dr. Mansij",
    "history": "MRI confirmed L4-L5 disc prolapse. Conservative treatment ongoing."
},

"P010": {
    "name": "Pooja Verma",
    "age": 47,
    "disease": "Brain Tumor Follow-up",
    "doctor": "Dr. Mansij",
    "history": "Successfully underwent meningioma excision in 2024. MRI monitoring ongoing."
}


}

DOCTOR_SCHEDULE = {


"Dr. Aryant Pratap Singh": {
    "available_slots": ["10:00 AM", "11:00 AM", "2:00 PM", "4:00 PM"],
    "booked_slots": []
},

"Dr. Lincon": {
    "available_slots": ["9:00 AM", "11:00 AM", "1:00 PM", "3:00 PM"],
    "booked_slots": []
},

"Dr. Harshit Mishra": {
    "available_slots": ["10:30 AM", "12:00 PM", "2:30 PM", "5:00 PM"],
    "booked_slots": []
},

"Dr. Himanshu Shekhar Pandey": {
    "available_slots": ["9:00 AM", "11:30 AM", "3:00 PM", "5:00 PM"],
    "booked_slots": []
},

"Dr. Vaibhav Pandey": {
    "available_slots": ["10:00 AM", "12:30 PM", "2:00 PM", "4:30 PM"],
    "booked_slots": []
},

"Dr. Mansij": {
    "available_slots": ["9:30 AM", "12:00 PM", "3:00 PM", "5:30 PM"],
    "booked_slots": []
},

"Dr. Rahul Singh": {
    "available_slots": ["9:00 AM", "10:00 AM", "1:00 PM", "4:00 PM"],
    "booked_slots": []
},

"Dr. Tej Pratap": {
    "available_slots": ["10:00 AM", "12:00 PM", "2:00 PM", "5:00 PM"],
    "booked_slots": []
},

"Dr. Avneesh": {
    "available_slots": ["9:30 AM", "11:30 AM", "2:30 PM", "4:30 PM"],
    "booked_slots": []
},

"Dr. Vaibhav Yadav": {
    "available_slots": ["9:00 AM", "11:00 AM", "1:00 PM", "5:00 PM"],
    "booked_slots": []
}


}

def find_patient(name):
    for pid, data in PATIENTS.items():
        if name.lower() in data["name"].lower():
            return pid, data
    return None, None