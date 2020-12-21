import requests, json


class Kmd_institution_api:

    def get_institutions(self, url, apikey):
        headers = {'content-type': 'application/json', 'Ocp-Apim-Subscription-Key': apikey}
        response = requests.get(url=url, headers=headers)
        print(response.status_code)
        #print(response.text)
        jdata = json.loads(response.text)
        print('name;id;shortName;careType;dayCareType')
        for institution in jdata:
            #dagplejere
            if institution['careType'] != 'Childminding':
                print(f"{institution['name']};{institution['id']};{institution['shortName']};{institution['careType']};{institution['dayCareType']}")
