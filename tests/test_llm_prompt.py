import pytest
from src.process_answers import process_user_inputs

# test_process_answers.py


def test_process_user_inputs():
    form_data = {
        'price_range': '$1000-$1500',
        'charger_type': 'USB-C',
        'color': 'Black',
        'graphics_card': 'High',
        'battery_lifetime': 'Long',
        'usage_description': 'Gaming and Development'
    }

    expected_output = "Expected output based on the LLM model's response"

    output = process_user_inputs(form_data)
    
    assert output == expected_output