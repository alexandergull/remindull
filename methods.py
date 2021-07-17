import requests

API_URL = "https://api.cleantalk.org/"
METHOD_NAMES_AVAILABLE = ["notice_paid_till", "spam_check", "ip_info"]
METHOD_TYPES = {"cms": ['notice_paid_till', 'ip_info'], "bl_api": ['spam_check']}


def spam_check(spam_check_data):
    """
    Fetches CleanTalk spam_check.
    -> Requires collection [api_key, email, ip]
    <- Returns obj [response, url]
    """

    api_key = spam_check_data['api_key']
    email = spam_check_data['email']
    ip = spam_check_data['ip']
    url = (F"{API_URL}"
           F"?method_name=spam_check"
           F"&auth_key={api_key}"
           F"&email={email}"
           F"&ip={ip}"
           F"&validate_email_existence=1"
           F"")
    print('Fetching spam_check...')
    print("Method URL:[" + url + "]")
    response = requests.get(url)
    return {"api_response": response.json(), "url": url}


def notice_paid_till(auth_key):
    """
    Fetches CleanTalk notice_paid_till.
    -> Requires api_key:text
    <- Returns obj [response, url]
    """
    url = (F"{API_URL}"
           F"?method_name=notice_paid_till"
           F"&auth_key={auth_key}"
           F"")
    print('Fetching notice_paid_till...')
    print("Method URL:[" + url + "]")
    response = requests.get(url)
    return {"api_response": response.json(), "url": url}


def ip_info(ip_info_data):
    """
    Fetches CleanTalk ip_info.
    -> Requires collection [api_key, ip]
    <- Returns obj [response, url]
    """
    api_key = ip_info_data['api_key']
    ip = ip_info_data['ip']
    url = (F'{API_URL}'
           F'?method_name=ip_info'
           F'&auth_key={api_key}'
           F'&ip={ip}'
           F'')
    print('Fetching ip_info...')
    print('Method URL:[' + url + ']')
    print()
    response = requests.get(url)
    return {"api_response": response.text + "]\n", "url": url}



