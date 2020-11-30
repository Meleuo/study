import json


d1 = {
    'name': 'Jerry',
    'age': 20,
    'is18': True,
    'marry': None
}

print('-' * 10)
print(d1)
print(type(d1))


print('-' * 10)
j1 = json.dumps(d1)
print(j1)
print(type(j1))

print('-' * 10)
d2 = json.loads(j1)
print(d2)
print(type(d2))
