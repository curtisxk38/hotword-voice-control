import json
import sys
import os
import requests
import test

def load_credentials(name):
    if os.path.isfile(name):
        with open(name, "r") as f:
            return json.load(f)
    else:
        return None
    
def api_call(audio_name, url, auth, params, headers):
    with open(audio_name, "rb") as audio:
        http_response = requests.post(url,
                                      auth=auth,
                                      data=audio,
                                      params=params,
                                      headers=headers,
                                      stream=False)
        return http_response

def parse(response):
    result = []
    data = response.json()
    for x in data["results"]:
        best_alt = x["alternatives"][0]
        print(best_alt)
        result.append(best_alt["transcript"])
    return result
    
def main(file_name):
    cred = load_credentials("credentials")
    #url = cred["url"]
    url = "https://stream.watsonplatform.net/speech-to-text/api/v1/recognize"
    auth = (cred["username"], cred["password"])
    params = {"continuous":True, "word_confidence":True}
    headers = {"content-type": "audio/wav"}

    r = api_call(file_name, url, auth, params, headers)
    result = parse(r)
    for i in result:
        print(i)
      
if __name__ == "__main__":
    main(sys.argv[1])
