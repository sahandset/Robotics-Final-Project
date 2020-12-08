import requests


x = requests.post('http://127.0.0.1:5000/post_target',
                  data={'target': '[(1, 2)]'})


x = requests.post('http://127.0.0.1:5000/post_coordinates',
                  data={'coordinates': '(1, 1)'})

x = requests.get('http://127.0.0.1:5000/get_target', cookies=x.cookies)

print(eval(x.text))
