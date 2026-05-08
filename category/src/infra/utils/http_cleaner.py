
def clean_outbound_request[T](
    obj: T,
) -> dict:
    """Remove None values before sending HTTP requests."""
    if isinstance(obj, str):
        try:
            return int(obj)
        except:
            try:
                return float(obj)
            except: ...
    elif isinstance(obj, bool):
        return 1 if obj else 0
    elif isinstance(obj, dict):
        _dict = dict()
        for k, v in obj.items():
            k = str(k)
            if v is not None:
                _dict.update({k: clean_outbound_request(v)})
        return _dict
    elif isinstance(obj, list):
        _list = list()
        for i in obj:
            if i is not None:
                _list.append(clean_outbound_request(i))
        return _list
    
    return obj