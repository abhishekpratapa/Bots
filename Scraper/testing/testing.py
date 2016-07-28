import requests

r = requests.get('http://127.0.0.1:5000/hello', auth=('admin', 'secret'))

print(r.status_code)
#print(r.headers['get-info'])
print(r.headers['content-type'])
print(r.text)