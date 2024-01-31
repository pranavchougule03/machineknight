from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO
import base64
import flsk

app = Flask(__name__)

# Set up a simple in-memory database to store uploaded data
uploaded_data = None
result_data = None
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/results')
def results():
    global uploaded_data

    if uploaded_data is None:
        return 'No data uploaded. Please go to the home page to upload a CSV file.'

    # Assuming the CSV file has columns 'Name', 'Roll Number', 'Grade'
    # You can modify this based on your actual CSV file structure
    columns = ['id', 'dropout_probability']
    
    # Display results
    results_html = uploaded_data.to_html(classes='table table-striped', index=False)

    # Generate downloadable CSV file
    csv_output = BytesIO()
    uploaded_data.to_csv(csv_output, index=False)
    csv_output.seek(0)

    return render_template('results.html', results_html=results_html, columns=columns, csv_data=base64.b64encode(csv_output.read()).decode('utf-8'))

@app.route('/upload', methods=['POST'])
def upload():
    global uploaded_data

    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        # Read CSV file into a Pandas DataFrame
        uploaded_data = pd.read_csv(file,sep=';')
        # uploaded_data['id'] = range(1, len(uploaded_data) + 1)
    uploaded_data = flsk.pred(uploaded_data)
    return render_template('File_uploaded.html')

@app.route('/fields_info')
def fields_info():
    # Define a dictionary with updated field names
    field_info = {
        'id':'Roll no of student',
        'Marital Status': 'Whether the student is married or not',
        'Application mode': 'Mode of application',
        'Application order': 'Order of application',
        'Course': 'Selected course',
        'Daytime/evening attendance': 'Attendance preference (Daytime/evening)',
        'Previous qualification': 'Previous academic qualification',
        'Previous qualification (grade)': 'Grade of previous qualification',
        'Nationality': 'Nationality',
        'Mother\'s qualification': 'Mother\'s highest qualification',
        'Father\'s qualification': 'Father\'s highest qualification',
        'Mother\'s occupation': 'Mother\'s occupation',
        'Father\'s occupation': 'Father\'s occupation',
        'Admission grade': 'Grade at the time of admission',
        'Displaced': 'Whether the student is displaced',
        'Educational special needs': 'Special educational needs',
        'Debtor': 'Whether the student is a debtor',
        'Tuition fees up to date': 'Payment status of tuition fees',
        'Gender': 'Gender of the student',
        'Scholarship holder': 'Whether the student holds a scholarship',
        'Age at enrollment': 'Age of the student at the time of enrollment',
        'International': 'Whether the student is international',
        'Curricular units 1st sem (credited)': 'Credits for 1st semester curricular units',
        'Curricular units 1st sem (enrolled)': 'Enrollment status for 1st semester curricular units',
        'Curricular units 1st sem (evaluations)': 'Number of evaluations for 1st semester curricular units',
        'Curricular units 1st sem (approved)': 'Number of approved 1st semester curricular units',
        'Curricular units 1st sem (grade)': 'Grade for 1st semester curricular units',
        'Curricular units 1st sem (without evaluations)': 'Curricular units without evaluations in 1st semester',
        'Curricular units 2nd sem (credited)': 'Credits for 2nd semester curricular units',
        'Curricular units 2nd sem (enrolled)': 'Enrollment status for 2nd semester curricular units',
        'Curricular units 2nd sem (evaluations)': 'Number of evaluations for 2nd semester curricular units',
        'Curricular units 2nd sem (approved)': 'Number of approved 2nd semester curricular units',
        'Curricular units 2nd sem (grade)': 'Grade for 2nd semester curricular units',
        'Curricular units 2nd sem (without evaluations)': 'Curricular units without evaluations in 2nd semester',
        'Unemployment rate': 'Unemployment rate',
        'Inflation rate': 'Inflation rate',
        'GDP': 'Gross Domestic Product',
        # Add more fields as needed
    }

    return render_template('fields_info.html', field_info=field_info)



