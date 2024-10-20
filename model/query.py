class Query:
    
    """
    Query class for build, validate and excuting queries

    """
    
    query: str

    provider: ("postgres", "mssql")

    def __init__(self, query: str):
        self.query = query


    def __str__(self):
        return f"{self.query}"