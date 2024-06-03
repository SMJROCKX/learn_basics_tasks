import pandas as pd 
import sys
import csv

def read_csv_to_list_of_rows(file_path):
  with open(file_path,'r',newline='') as file:
    reader = csv.reader(file)
    list_of_rows=[]
    for row in reader:
      list_of_rows.append(row)
  return(list_of_rows)

def read_any_number_of_csv_to_list_of_rows():
  list_of_rows=[]
  for i in range (1,len(sys.argv)):
    file_path = sys.argv[i]
    with open(file_path,'r',newline='') as file:
      reader = csv.reader(file)
      for row in reader:
        list_of_rows.append(row)
  del list_of_rows[0]
  return(list_of_rows)

def get_test_list(list_of_columns):
  list_test  = []
  list_test_data = list_of_columns[0]
  for i in range(3,len(list_test_data)):
    list1 = list_test_data[i].split("-")
    name  = list1[0].rstrip()
    if name not in list_test:
      list_test.append(name)
  return list_test

def convert_to_output(list_of_rows,test_list):
  column_names = list_of_rows[0]
  len1 = len(list_of_rows)
  len2  =len(list_of_rows[0])
  number_of_tests = int((len1-3)/6)
  list_of_output = []
  for i in range(1,len1):
    for j in range(len(test_list)):
      list_of_output_per_test = []
      list_of_output_per_test.extend(list_of_rows[i][0:3])
      list_of_output_per_test.append(test_list[j])
      list_of_output_per_test.extend(list_of_rows[i][(6*j)+3:(6*j)+9])
      list_of_output.append(list_of_output_per_test)
  return list_of_output

def main(file_path):
  file1 = read_csv_to_list_of_rows(file_path)
  file2 = get_test_list(file1)
  file3 = convert_to_output(file1,file2)
  column_names = ['Name', 'Username', 'Chapter Tag','Test_Name','Score','Time-taken (seconds)','Answered','Correct','Wrong','Skipped']
  df = pd.DataFrame(file3, columns=column_names)
  df= df.replace('-', pd.NA, inplace=True)
  df= df.dropna(axis=0, how='any', inplace=True)
  desired_columns = ['Name', 'Username', 'Chapter Tag','Test_Name','Answered','Correct','Score','Skipped','Time-taken (seconds)','Wrong']
  df = df[desired_columns]
  df.to_csv('output.csv', index=False)
  
  

file_path = input("Enter ytour file path")
main(file_path)
