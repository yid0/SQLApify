class JsonObject:
    def __init__(cls, dictionary: dict):
        if isinstance(dictionary, dict):
            for key, value in dictionary.items():
                if isinstance(value, dict):
                    value = JsonObject(value)
                setattr(cls, key, value)
        else:
            raise TypeError("Input object is not type of dict.")
