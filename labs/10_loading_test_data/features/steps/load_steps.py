# pylint: disable=function-redefined, missing-function-docstring
# flake8: noqa
"""
Pet Steps
Steps file for Pet.feature
For information on Waiting until elements are present in the HTML see:
    https://selenium-python.readthedocs.io/waits.html
"""
import requests
from behave import given

# Load data here
@given('the following pets')
def step_impl(context):
    """Refresh all Pets in the database"""
    responese = requests.get(f"{context.base_url}/pets")
    assert responese.status_code == 200
    for pet in responese.json():
        responese = requests.delete(f"{context.base_url}/pets/{pet['id']}")
        assert responese.status_code == 204

    for row in context.table:
        payload  = {
            "name" : row['name'],
            "category" : row['category'],
            "available" : row['available'] in ['True', 'true', '1'],
            "gender" : row['gender'],
            "birthday" : row['birthday']
        }
        responese = requests.post(f"{context.base_url}/pets", json=payload)
        assert responese.status_code == 201 