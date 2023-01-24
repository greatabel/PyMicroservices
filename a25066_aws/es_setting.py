# coding = utf-8
# es 调用建立index demo例子

import requests
from os import environ
import json
import simplejson
import subprocess

import requests

# Making a PUT request
r = requests.put(
    "http://localhost:9200/twitter/tweet/1",
    headers={"Content-Type": "application/json"},
    json={"message": "今天天气不错，风和日丽的."},
)

# check status code for response received
# success code - 200
print(r)

# print content of request
print(r.content)

r = requests.put(
    "http://localhost:9200/twitter/tweet/2",
    headers={"Content-Type": "application/json"},
    json={"message": "今天心情很好. I am doing test today."},
)

# check status code for response received
# success code - 200
print(r)

# print content of request
print(r.content)
