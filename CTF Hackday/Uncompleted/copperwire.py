import requests

url = "http://h4ckd4y.external:8000"
headers = {
    "User-Agent": "python-requests/2.32.3",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept": "*/*",
    "Connection": "keep-alive"
}
cookies = {
    "cookie_name": "=PL9Gs9lsFgAAAAAE6mj3AAAAAADwdolbAAAAAMQStwAAAACIJW4BAAAAEEvcAgAAACCWuAUAAABALHELAAAAgA=="
}

response = requests.get(url, headers=headers, cookies=cookies)

print(response.status_code)
print(response.text)
