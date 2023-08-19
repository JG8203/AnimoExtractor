import requests

# Define the URL you want to make a request to
url = 'https://enroll.dlsu.edu.ph/dlsu/view_course_offerings'

# Define the list of cookies you have
cookies = [
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU1",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": "enroll.dlsu.edu.ph",
        "expirationDate": 1692028014,
        "hostOnly": True,
        "httpOnly": False,
        "name": "cf_chl_2",
        "path": "/",
        "secure": False,
        "session": False,
        "value": "e554e9dec31df91"
    },
    {
        "domain": "enroll.dlsu.edu.ph",
        "expirationDate": 1692024535.501973,
        "hostOnly": True,
        "httpOnly": True,
        "name": "NSC_Fospmm_TTM",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "ffffffffc3a017b045525d5f4f58455e445a4a423660"
    },
    {
        "domain": ".dlsu.edu.ph",
        "expirationDate": 1707576416.501912,
        "hostOnly": False,
        "httpOnly": True,
        "name": "cf_clearance",
        "path": "/",
        "secure": True,
        "session": False,
        "value": "bTHyHsDEwuXTOLX9QkSFwhJWoUFtCj2_rOzVZH4M3_w-1692024414-0-1-d42cf0a5.10aa7120.832daf45-160.0.0"
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU10",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU11",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU12",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU13",
        "path": "/",
        "secure": False,
        "session": True,
        "value": "Y"
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU14",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU2",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU3",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU4",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU5",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU6",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU7",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU8",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    },
    {
        "domain": ".dlsu.edu.ph",
        "hostOnly": False,
        "httpOnly": False,
        "name": "DLSU9",
        "path": "/",
        "secure": False,
        "session": True,
        "value": ""
    }
]

# Convert the cookies list into the correct format
formatted_cookies = '; '.join([f'{cookie["name"]}={cookie["value"]}' for cookie in cookies if cookie["value"]])

# Create headers with the cookies
headers = {
    'Cookie': formatted_cookies,
}

# Make the request
response = requests.get(url, headers=headers)

# Print the response content
print(response.text)
