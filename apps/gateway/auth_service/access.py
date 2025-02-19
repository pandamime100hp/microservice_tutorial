import os, requests

def login(request):
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return None, ("missing credentials", 401)
    
    basic_auth = (auth.username, auth.password)
    
    res = requests.post(f"http://{os.environ.get('AUTH_SERVICE_HOST')}/login", auth=basic_auth)

    if res.status_code == 200:
        return res.text, None
    
    return None, (res.text, res.status_code)