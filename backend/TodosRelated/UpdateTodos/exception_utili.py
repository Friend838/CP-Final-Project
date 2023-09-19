
PAYLOAD_VALIDATION = ['userId', 'timestamp', 'name', 'attributes']
ATTRIBUTE_VALIDATION = ['todo_timestamp', 'todo_name', 'todo_description', 'todo_finished']

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

def validate_addional_attribute(attribute):
    for key in attribute:
        if key['type'] not in ATTRIBUTE_VALIDATION:
            return False
    return True

class BodyParamsError(Exception):
    # two types: "too less" or "too many" params
    def __init__(self, type):
        if type == 'too less':
            self.message = 'body params must have the following types: 1. "userId", 2. "timestamp" 3. "name" 4. "attributes"'
        elif type == 'too many':
            self.message = 'body params only allow the following types: 1. "userId", 2. "timestamp" 3. "name" 4. "attributes"'
        elif type == 'attributes error':
            self.message = 'attributes only allow the following types: 1. "todo_timestamp" 2. "todo_name" 3. "todo_description" 4. "todo_finished"'
        
class NoTargetItemError(Exception):
    def __init__(self):
        self.message = 'Find no item with the given userId and timestamp'