import requests

def mayaMovies(username, password):    
    url = "https://demo.credy.in/api/v1/maya/movies/"

    payload = {}
    headers = {
        'Authorization': f'Basic {username}:{password}'
    }
    print("\n", headers, "\n")
    response = requests.get(url, headers=headers, data=payload, verify=False)
    print("\n", response.content, "\n")
    
    if response.status_code == 200:
        return response.json()
    else:
        return None  # Handle error cases as per your requirement