
PAYLOAD_VALIDATION = ['userId', 'name']

def validate_payload(payload):
    for key in PAYLOAD_VALIDATION:
        if key not in payload:
            return False
    return True

def validate_additional_payload(payload):
    for key in payload:
        if key not in PAYLOAD_VALIDATION:
            return False
    return True

class BodyParamsError(Exception):
    # two types: "too less" or "too many" params
    def __init__(self, type):
        if type == 'too less':
            self.message = 'body params must have the following types: 1. "userId", 2. "name"'
        elif type == 'too many':
            self.message = 'body params only allow the following types: 1. "userId", 2. "name"'