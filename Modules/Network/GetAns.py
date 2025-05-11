import requests

AnswerApi = 'serverURL'

def GiveDescription(prompt):
    response = requests.get(f'{AnswerApi}/{prompt}')
    if response.status_code == 200:
        return response.text
    else:
        return "Error"
    
#print(DiscApi("hello"))