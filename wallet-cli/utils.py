def urljoin(*args):
    """
    Joins given arguments into an url.
    """
    return "/".join(map(lambda x: str(x).strip('/'), args))
