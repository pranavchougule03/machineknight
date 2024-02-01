from flask import Flask, render_template, request, send_file
import pandas as pd
from io import BytesIO
import base64
import flsk

app = Flask(__name__)

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

    low_risk_data = uploaded_data[uploaded_data['dropout_probability'] == 'low-risk']
    neutral_data = uploaded_data[uploaded_data['dropout_probability'] == 'neutral']
    high_risk_data = uploaded_data[uploaded_data['dropout_probability'] == 'high-risk']

    low_risk_html = low_risk_data.to_html(classes='table table-striped', index=False)
    neutral_html = neutral_data.to_html(classes='table table-striped', index=False)
    high_risk_html = high_risk_data.to_html(classes='table table-striped', index=False)

    low_risk_csv = BytesIO()
    low_risk_data.to_csv(low_risk_csv, index=False)
    low_risk_csv.seek(0)

    neutral_csv = BytesIO()
    neutral_data.to_csv(neutral_csv, index=False)
    neutral_csv.seek(0)

    high_risk_csv = BytesIO()
    high_risk_data.to_csv(high_risk_csv, index=False)
    high_risk_csv.seek(0)

    return render_template('results.html', 
                           low_risk_html=low_risk_html, 
                           neutral_html=neutral_html, 
                           high_risk_html=high_risk_html,
                           low_risk_csv=base64.b64encode(low_risk_csv.read()).decode('utf-8'),
                           neutral_csv=base64.b64encode(neutral_csv.read()).decode('utf-8'),
                           high_risk_csv=base64.b64encode(high_risk_csv.read()).decode('utf-8'))

@app.route('/upload', methods=['POST'])
def upload():
    global uploaded_data

    file = request.files['file']
    if file and file.filename.endswith('.csv'):
        uploaded_data = pd.read_csv(file,sep=';')
    uploaded_data = flsk.pred(uploaded_data)
    return render_template('File_uploaded.html')

@app.route('/fields_info')
def fields_info():
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
    }

    return render_template('fields_info.html', field_info=field_info)

if __name__ == '__main__':
 
    # run() method of Flask class runs the application 
    # on the local development server.
    app.run()
