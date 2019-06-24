import requests
import json, re, time
from datetime import datetime
import pandas as pd

API_ENDPOINT = 'https://kong.speedcheckerapi.com:8443/ProbeAPIv2/'

with open('api-ri.key','r') as f:
    APIKEY = f.read()

ccs = [
'EG', 'BJ', 'CI', 'CV', 'GH', 'GM', 'GN', 'GW', 'AO', 'CF', 'CG', 'CM', 'GA', 'GQ', 'TD', 'BI', 'DJ', 'ER', 'ET', 'KM', 'BW', 'MA', 'SD', 'TN', 'LR', 'ML', 'MR', 'NE', 'NG', 'SL', 'SN', 'TG', 'ST', 'KE', 'MG', 'MU', 'MW', 'MZ', 'RE', 'RW', 'SC', 'SO', 'UG', 'LS', 'NA', 'SZ', 'ZA', 'DZ', 'EH', 'LY', 'BF', 'SH', 'CD', 'TZ', 'YT', 'ZM', 'ZW']

HEADERS = {'apikey': APIKEY,
            'accept': 'application/json',
            'content-type': 'application/json'
          }

probeInfoProperties = [
        "ASN",
        "CityName",
        "ConnectionType",
        "CountryCode",
        "DNSResolver",
        "GeolocationAccuracy",
        "IPAddress",
        "Latitude",
        "Longitude",
        "Network",
        "NetworkID",
        "Platform",
        "ProbeID",
        "Version",
        "Screensize"
    ]


def startPingTest(cc, destination, pingType, ipv4Only, ipv6Only, resolve):
    
    test_url = API_ENDPOINT + "StartPingTest"
        
    json_test = {
        "testSettings": {
        "PingType": pingType,
        "BufferSize": 32,
        "Count": 3,
        "Fragment": 1,
        "Ipv4only": ipv4Only,
        "Ipv6only": ipv6Only,
        "Resolve": resolve,
        "Sleep": 1000,
        "Ttl": 128,
        "Timeout": 1000,
        "TestCount": 10,
        "Sources": [
          {
            "CountryCode": cc
          }
        ],
        "Destinations": [
          destination
        ],
        "ProbeInfoProperties": probeInfoProperties
      }
    }
    
    data = json.dumps(json_test)
    
    try:
        r = requests.post(test_url, data=data, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        return "Request FAILED"
    
    res = json.loads(r.text)
                
    if ("OK" == res['StartPingTestResult']['Status']['StatusText']):
        return res['StartPingTestResult']['TestID']
    else:
        return "FAILED"

    

#function to launch a traceroute
def startTracertTest(cc, destination):
    
    test_url = API_ENDPOINT + "StartTracertTest"
    
    json_test = {
      "testSettings": {
        "BufferSize": 32,
        "Count": 3,
        "Fragment": 1,
        "Ipv4only": 0,
        "Ipv6only": 0,
        "MaxFailedHops": 0,
        "Resolve": 1,
        "Sleep": 300,
        "Ttl": 128,
        "TtlStart": 1,
        "Timeout": 80000,
        "HopTimeout": 3000,
        "TestCount": 10,
        "Sources": [
          {
            "CountryCode": cc
          }
        ],
        "Destinations": [
          destination
        ],
        "ProbeInfoProperties": probeInfoProperties
      }
    }
    
    
    data = json.dumps(json_test)
    
    try:
        r = requests.post(test_url, data=data, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        return "Request FAILED"
    
    res = json.loads(r.text)
                
    if ("OK" == res['StartTracertTestResult']['Status']['StatusText']):
        return res['StartTracertTestResult']['TestID']
    else:
        return "FAILED"
    

def startDigTest(cc, domain, cache, qclass, qtype, recurse, retries, dnsresolver, tcp):
    
    test_url = API_ENDPOINT + "StartDigTest"
    
    dig_test = {
          "testSettings": {
            "Cache": cache,
            "QClass": qclass,
            "QType": qtype,
            "Recurse": recurse,
            "Retries": retries,
            "Server": dnsresolver,
            "Tcp": tcp,
            "Time": 2000,
            "TestCount": 10,
            "Sources": [
              {
                "CountryCode": cc
              }
            ],
            "Destinations": [
              domain
            ],
            "ProbeInfoProperties": probeInfoProperties
          }
        }
        
    data = json.dumps(dig_test)
    
    try:
        r = requests.post(test_url, data=data, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        return "Request FAILED"
    
    try:
        res = json.loads(r.text)
    except JSONDecodeError as e:
        return "FAILED"
        
    if ("OK" == res['StartDigTestResult']['Status']['StatusText']):
        return res['StartDigTestResult']['TestID']
    else:
        return "FAILED"
    
def retrieveDigTestResult(testID):
        
    url = API_ENDPOINT + "GetDigResults?apikey=" + APIKEY + "&testID=" + testID
    
    try:    
        r = requests.get(url, headers=HEADERS)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return []
    
    res = json.loads(r.text)
    return res['DigTestResults']

def retrievePingTestResult(testID):
        
    url = API_ENDPOINT + "GetPingResults?apikey=" + APIKEY + "&testID=" + testID
    
    try:    
        r = requests.get(url, headers=HEADERS)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return []
    
    res = json.loads(r.text)
    return res['PingTestResults']

def retrieveTracertTestResult(testID):
        
    url = API_ENDPOINT + "GetTracertResults?apikey=" + APIKEY + "&testID=" + testID
    
    try:    
        r = requests.get(url, headers=HEADERS)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return []
    
    res = json.loads(r.text)
    return res['TracerouteTestResults']

def getAvailablePCProbesCC():
    
    json_test = {
                  "criteria": {
                    "Sources": [
                      { 
                        "Platform":"PC",
                        "BoundingBox": {
                          "MinLatitude": -47.131349,
                          "MaxLatitude": 37.5359,
                          "MinLongitude": -25.383911,
                          "MaxLongitude": 63.808594
                        }
                      }
                    ],
                    "ProbeInfoProperties": probeInfoProperties
                  }
                }
    
    url = API_ENDPOINT + "GetProbes?apikey=" + APIKEY
    
    data = json.dumps(json_test)
    
    try:
        r = requests.post(url, data=data, headers=HEADERS)
    except requests.exceptions.RequestException as e:
        return "Request FAILED"
       
    j = r.json()

    df = pd.DataFrame.from_dict(j)
    
    df = pd.DataFrame(df['GetProbesResult']['Probes'])
    
    return df
