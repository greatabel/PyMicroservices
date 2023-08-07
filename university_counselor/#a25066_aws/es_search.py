# coding = utf-8
# es 调用搜索封装

import requests
from os import environ
import json

import subprocess

import requests


def mysearch(keyword):
    # Making a PUT request
    r = requests.get(
        "http://localhost:9200/twitter/_search?q=message:" + keyword,
        headers={"Content-Type": "application/json"},
    )

    # check status code for response received
    # success code - 200
    print(r)

    # print content of request
    result = r.json()["hits"]["hits"][0]["_source"]["message"]
    print(result, "\n" * 3)
    return result


if __name__ == "__main__":
    mysearch("天气")
    mysearch("test")
