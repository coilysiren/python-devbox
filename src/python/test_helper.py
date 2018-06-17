import sys
import json


def json_body(response):
    return json.loads(response.get_data().decode(sys.getdefaultencoding()))
