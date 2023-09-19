import json

test = {
    "userId": "8787878787",
    "has_person": True
}
# print(json.dumps(test))
print(json.loads('{"userId": "8787878787", "has_person": true}'))