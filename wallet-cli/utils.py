def urljoin(*args):
    """
    https://stackoverflow.com/a/11326230/3705710
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return "/".join(map(lambda x: str(x).rstrip('/'), args))
