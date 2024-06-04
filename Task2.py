import requests

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
