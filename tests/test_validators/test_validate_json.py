import pytest
from Validators.validate_json import validate_json_string_value, validate_json_numeric_value

def test_validate_json_string_value():
    value1=validate_json_string_value('Logitech Keyboard')
    value2=validate_json_string_value(200)
    assert value1==True
    assert value2==False

def test_validate_json_numeric_value():
    value1=validate_json_numeric_value('Iphone 7')
    value2=validate_json_numeric_value(400)
    value3=validate_json_numeric_value(-1)
    assert value1==False
    assert value2==True
    assert value3==False