import datetime
from datetime import timedelta
import logging
import pandas as pd
import datetime
from datetime import timedelta
import logging
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
from datetime import timedelta
import logging
import pandas as pd
import requests
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

global start_date
global end_date

logger = logging.getLogger(__name__)

def extract_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for non-2xx status codes
        extracted_data = response.text  # Extract the data from the response as JSON
        return extracted_data
    except requests.exceptions.HTTPError as e:
        logger.error(f"Error: {e}")
        return None

"""Transforms raw data into a format that can be used for analysis."""
def transform_data(df, years, station, min_frozen):
 
    # Calculate date x years ago from the first day of the previous month
    global start_date
    global end_date

    logger = logging.getLogger(__name__)

    end_date = (datetime.datetime.now().replace(day=1) - timedelta(days=1)).replace(day=1)

    # Assuming 365.25 days per year to account for leap years
    start_date = end_date - timedelta(days=int(365.25 * years))

    # Filter DataFrame on YEARS
    df['DATE'] = pd.to_datetime(df['DATE'], format='%Y-%m-%d')  # Transform DATE series to datetime using a string format
    df = df[(df.DATE >= start_date) & (df.DATE < end_date)]

    # Calculate missing data
    init_len = df.size
    df = df.dropna()
    missing_rows = init_len - df.size
    logger.info(f'Total Rows Missing Data :( : {missing_rows}')

    # Calculate wet and frozen conditions based on precipitation and temperature
    df.loc[:, 'WET']  = (df['PRCP'] > 0).astype(int)
    df.loc[:, 'FRZN'] = (df['TMIN'] <= min_frozen) \
    .astype(int)

    # Calculate snow logit based on wet and frozen conditions
    df.loc[:, 'SNOW'] = (df['WET'] * df['FRZN']).astype(int)

    report = {}
    report['Total Snow Days'] = round(df['SNOW'].sum(), 1)
    report['Average Snow Days per Year'] = round(df['SNOW'].sum() / (df.size / 365.25), 1)
    report['Human on Factor'] = 1.5
    report['Average Heating Hours'] = round(report['Human on Factor'] * 24 * report['Average Snow Days per Year'], 1)
    report['Years'] = years
    report['Missing Rows'] = missing_rows

    return report

"""Loads climate report and puts it in a pdf format"""
def load_data(filename, report):
    # Create a canvas for PDF generation
    c = canvas.Canvas(filename, pagesize=letter)

    # Set the title for the report
    title = f"Climate Report NOAA {start_date.month}-{start_date.year}:{end_date.month}-{end_date.year}"  
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 750, title)
    
    # Set the data points
    c.setFont("Helvetica", 12)
    y_position = 700

    for k, v in report.items():
        c.drawString(50, y_position, f"{k}:")
        y_position -= 40  # Adjust vertical position for the next data point
        
        if isinstance(v, dict):
            for sub_k, sub_v in v.items():
                c.drawString(70, y_position, f"  {sub_k}: {sub_v}")
                y_position -= 20  # Adjust vertical position for the next sub-data point
        y_position -= 20  # Adjust vertical position for the next data point
    # Save the PDF file
    c.save()