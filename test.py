
required_dict = {"language_localizer": {
    "responses": {
            "escape": "escape",
            "attention_check": "space"
    },
    "stimuli": {
            "text_color": [-1, -1, -1],
            "fix_color": [-1, -1, -1]
    },
    "mri": {"sync": "t"}
}}

settings = {"language_localizer": "test"}

def validate_dict(required_dict, check_dict):
    for key, value in required_dict.items():
        print(key, value)
        if isinstance(value, dict):
            # If the value is a dictionary, recurse into it
            if not validate_dict(value, check_dict.get(key, {})):
                return False
        else:
            # If the value is not a dictionary, check if the key and value exist in check_dict
            if key not in check_dict or check_dict[key] != value:
                return False
    return True

print(validate_dict(settings, required_dict))