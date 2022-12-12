import requests
from python_graphql_client import GraphqlClient

client = GraphqlClient(endpoint="https://api.fontawesome.com")

def get_version():
    query = "query { release (version: \"6.x\") { version } }"
    return client.execute(query)['data']['release']['version']

def get_icon_info(icon_query: str, limit: int = 15, free_only: bool = True, full_info: bool = False):

    free_block = 'free { family style }'
    pro_block = 'pro { family style }'

    if free_only:
        family_style_block = 'familyStylesByLicense {%s}' % (free_block)
    else:
        family_style_block = 'familyStylesByLicense {%s %s}' % (free_block, pro_block)

    if full_info:
        full_info_block = 'unicode label %s' % (family_style_block)
    else:
        full_info_block = ''

    query = """query search_icon($version: String!, $query: String!, $limit: Int)
    {
        search (version: $version, query: $query, first: $limit) 
        {
            id %s
        }
    }""" % (full_info_block)

    variables = {'version': "6.x", "query": icon_query, "limit": limit}
    return client.execute(query, variables)['data']['search']

def get_icon_id(icon_info: list):
    return [icon['id'] for icon in icon_info]

