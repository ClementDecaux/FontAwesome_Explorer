import requests
from python_graphql_client import GraphqlClient

client = GraphqlClient(endpoint="https://api.fontawesome.com")

def get_version():
    query = "query { release (version: \"6.x\") { version } }"
    return client.execute(query)['data']['release']['version']

def search_icon(searched_terms: str, limit: int, free_only=True):

    free_block = 'free { family style }'
    pro_block = 'pro { family style }'

    if free_only:
        family_style_block = 'familyStylesByLicense {%s}' % (free_block)
    else:
        family_style_block = 'familyStylesByLicense {%s %s}' % (free_block, pro_block)

    query = """query search_icon($version: String!, $query: String!, $limit: Int)
    {
        search (version: $version, query: $query, first: $limit) 
        {
            id unicode label %s
        }
    }""" % (family_style_block)

    variables = {'version': "6.x", "query": searched_terms, "limit": limit}
    return client.execute(query, variables)['data']['search']

def get_ids(result: list):
    return [icon['id'] for icon in result]