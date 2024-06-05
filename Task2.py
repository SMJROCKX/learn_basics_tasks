import requests
import pandas as pd 
import numpy as np
pip install reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Table, TableStyle, Frame,Spacer,PageBreak
from reportlab.lib import colors

def get_data(api_url):
  url = api_url
  headers1 = {"Authorization": '1b28274d-1b90-43c3-ad36-dd730905b034'}
  response = requests.get(url, headers=headers1)
  if response.status_code == 200:
    print("got data successfully")
    return response.json()
  else:
     print(f"Request failed with status code: {response.status_code}")


test_details = get_data('https://api.learnbasics.fun/training/test/info/')
student_details= get_data('https://api.learnbasics.fun/training/students/')
test_performance_details=get_data('https://api.learnbasics.fun/training/test/data/')
concept_data_details=get_data('https://api.learnbasics.fun/training/test/concepts/')

def seconds_to_mmss(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes:02}:{remaining_seconds:02}"


def merge_table(student_details,test_performance_details):
  td = pd.DataFrame.from_dict(test_details,orient='index')
  tpd = pd.DataFrame.from_dict(test_performance_details)
  sr = pd.merge(sd,tpd , on='learner_id',how='left')
  return sr 

def marks_table_maker(student_details,test_performance_details):
  merge_table(student_details,test_performance_details)
  nsr = sr.drop(['learner_id','test_id','question_id','response','attempt'], axis=1)
  nsr = nsr.groupby(['student_name']).sum()
  nsr['mark'] = nsr['mark'].astype('int')
  nsr['last_login'] = nsr['last_login']/5
  nsr['last_login'] = nsr['last_login'].astype('int')
  nsr['time_taken'] = nsr['time_taken'].apply(seconds_to_mmss)
  nsr = nsr.reset_index()
  nsr['mark'] = nsr['mark'].astype(str) + "/5"
  return nsr
  
def accuracy_table_maker(merged_student_test_table,concept_data_details):
  correct_responses = correct_responses.dropna(subset=['response'])
  total_responses = correct_responses.groupby('question_id').size()
  right_answers = correct_responses[correct_responses['mark'] == 1.0].groupby('question_id').size()
  percentage_right = (right_answers/ total_responses) * 100
  wpf = pd.DataFrame({'question_id': percentage_right.index, 'percentage_right': percentage_right.values})
  wpf['percentage_right'] = wpf['percentage_right'].round(0)
  merged_table = pd.merge(concept_data_details, wpf, on='question_id')
  merged_table.insert(0, 'Question No.', ['Q' + str(i) for i in range(len(merged_table))])
  merged_table.reset_index(drop=True, inplace=True)
  return merged_table


td = pd.DataFrame.from_dict(test_details,orient='index')
tpd = pd.DataFrame.from_dict(test_performance_details)
cdd = pd.DataFrame.from_dict(concept_data_details)
nsr = marks_table_maker(td,tpd)
mt = accuracy_table_maker(merge_table(td,tpd),cdd)

doc = SimpleDocTemplate("report.pdf", pagesize=A4)
elements = []

logo_path = "/content/Screenshot 2024-06-05 064600.png"
logo = Image(logo_path, 1 * inch, 1 * inch)
elements.append(logo)
elements.append(Spacer(1, 0.5 * inch))

school_info = f"<b>Learn Basics</b> - <b>{td.at['school_name', 0]}</b>"
school_info_paragraph = Paragraph(school_info, getSampleStyleSheet()['Title'])
elements.append(school_info_paragraph)

line = Table([['']], colWidths=[7.5 * inch])
line.setStyle(TableStyle([('LINEBELOW', (0, 0), (-1, 0), 1, colors.black)]))
elements.append(line)

class_subject_chapter = Paragraph(f"Class: {td.at['class',0]}<br/>Subject: {td.at['subject',0]}<br/>Chapter: {td.at['chapter_name',0]}", styles['Normal'])
elements.append(class_subject_chapter)

test_details = Paragraph(f"Test Name: {td.at['test_name',0]}<br/>Start Time: {td.at['start_time',0]}<br/>End Time: {td.at['end_time',0]}", styles['Normal'])
elements.append(test_details)

table_data = [nsr.columns.to_list()] + nsr.values.tolist()
table = Table(table_data, repeatRows=1)
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.white),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.white),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),
]))
elements.append(table)
elements.append(PageBreak())
table_data = [mt.columns.tolist()] + mt.values.tolist()

table = Table(table_data)

table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.white),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black),
                           ]))


elements.append(table)
