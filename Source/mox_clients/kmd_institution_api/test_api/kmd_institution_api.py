import requests, json


class Kmd_institution_api:

    def get_institutions(self, url, apikey):
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        response = requests.get(url=url, headers=headers)
        print(response.status_code)
        #print(response.text)
        jdata = json.loads(response.text)
        for institution in jdata:
            print(institution['name'], institution['id'])

