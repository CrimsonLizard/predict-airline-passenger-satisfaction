import unittest
import pandas as pd
from pandas.testing import assert_frame_equal
import re
from predict import validate_input, preprocess_data, reorder_dict, app

class PredictTest(unittest.TestCase):
    def test_validate_input(self):
        # Test if there are all required keys in the dictionary
        dict_few_required_keys = {
            'customer_type': 'Loyal customer',
            'type_of_travel': 'Business travel',
            'class_of_travel': 'Business'
        }
        
        result_required_keys = validate_input(dict_few_required_keys)
        self.assertFalse(result_required_keys)
        
        # Test if values under customer_type, type_of_travel and class_of_travel have relevant variants
        dict_inrelevant_values = {
            'customer_type': 'Invalid customer type',
            'type_of_travel': 'Personal travel',
            'class_of_travel': 'blah-blah',
            'age': '34'
        }
        
        result_inrelavant_values = validate_input(dict_inrelevant_values)
        self.assertFalse(result_inrelavant_values)

        # Test if required values are empty
        dict_empty_values = {
            'customer_type': '',
            'type_of_travel': 'Personal travel',
            'class_of_travel': 'Eco plus',
            'age': '34'
        }
        
        result_empty_values = validate_input(dict_empty_values)
        self.assertFalse(result_empty_values)


        # Test if age not in range(0, 121)
        dict_age_number = {
            'customer_type': 'Loyal customer',
            'type_of_travel': 'Business travel',
            'class_of_travel': 'Business',
            'age': '350'
        }
        
        result_age_number = validate_input(dict_age_number)
        self.assertFalse(result_age_number)

        # Test if age not an integer
        dict_age_word = {
            'customer_type': 'Loyal customer',
            'type_of_travel': 'Business travel',
            'class_of_travel': 'Business',
            'age': '0.5'
        }
        
        result_age_word = validate_input(dict_age_word)
        self.assertFalse(result_age_word)

        # Test if age is empty value
        dict_age_empty = {
            'customer_type': 'Loyal customer',
            'type_of_travel': 'Business travel',
            'class_of_travel': 'Business',
            'age': ' '
        }
        
        result_age_empty = validate_input(dict_age_empty)
        self.assertFalse(result_age_empty)

        # Test if other numeric values not in range (0, 5)
        dict_numeric_check_wrong_number = {
            'customer_type': 'Loyal customer',
            'type_of_travel': 'Business travel',
            'class_of_travel': 'Business',
            'age': '35',
            'inflight_entertainment': '0',
            'on_board_service': '120',
            'baggage_handling': '0'
        }
           
        result_numeric_worng_number = validate_input(dict_numeric_check_wrong_number)
        self.assertFalse(result_numeric_worng_number)

        # Test if other numeric values not int
        dict_numeric_check_float = {
            'customer_type': 'Loyal customer',
            'type_of_travel': 'Business travel',
            'class_of_travel': 'Business',
            'age': '35',
            'inflight_entertainment': '0',
            'on_board_service': '5',
            'baggage_handling': '1.75'
        }
           
        result_numeric_float = validate_input(dict_numeric_check_float)
        self.assertFalse(result_numeric_float)

        # Test if other numeric values are digits
        dict_numeric_check_wrong_type = {
            'customer_type': 'Loyal customer',
            'type_of_travel': 'Business travel',
            'class_of_travel': 'Business',
            'age': '35',
            'inflight_entertainment': '0',
            'on_board_service': '3',
            'baggage_handling': True
        }
           
        result_numeric_wrong_type = validate_input(dict_numeric_check_wrong_type)
        self.assertFalse(result_numeric_wrong_type)

        # Test proper input
        dict_proper_input = {
            'baggage_handling': '5',
            'customer_type': 'Loyal customer',
            'age': '24',
            'type_of_travel': 'Business travel',
            'gate_location': '3',
            'online_boarding': '4',
            'inflight_entertainment': '5',
            'on_board_service': '2',
            'inflight_wifi_service': '5',
            'checkin_service': '0',
            'inflight_service': '4',
            'cleanliness': '1',
            'class_of_travel': 'Business',
            'seat_comfort': '5'
        }

           
        result_proper_input = validate_input(dict_proper_input)
        self.assertTrue(result_proper_input)


    def test_preprocess_data(self):
        dict_valid_input_ = {
            'baggage_handling': '4',
            'customer_type': 'Loyal customer',
            'age': '35',
            'type_of_travel': 'Business travel',
            'gate_location': '3',
            'online_boarding': '4',
            'inflight_entertainment': '4',
            'on_board_service': '3',
            'inflight_wifi_service': '5',
            'checkin_service': '5',
            'inflight_service': '4',
            'cleanliness': '5',
            'class_of_travel': 'Business',
            'seat_comfort': '5'
        }

        expected_df = pd.DataFrame({
            'customer_type': [0.0],
            'age': [35.0],
            'type_of_travel': [1.0],
            'inflight_wifi_service': [5.0],
            'gate_location': [3.0],
            'online_boarding': [4.0],
            'seat_comfort': [5.0],
            'inflight_entertainment': [4.0],
            'on_board_service': [3.0],
            'baggage_handling': [4.0],
            'checkin_service': [5.0],
            'inflight_service': [4.0],
            'cleanliness': [5.0],
            'class_of_travel': [0.48]
        })

        result_valid_df = preprocess_data(dict_valid_input_)
        assert_frame_equal(result_valid_df, expected_df)

    def test_reorder_dict(self):
        # Test how the function reorders a small dictionary
        dict_unordered_small = {
            'baggage_handling': '4',
            'customer_type': 'Loyal customer',
            'type_of_travel': 'Business travel',
            'class_of_travel': 'Business',
            'seat_comfort': '5'
        }

        dict_expected_ordered = {
            'customer_type': 'Loyal customer',
            'age': '0',
            'type_of_travel': 'Business travel',
            'inflight_wifi_service': '0',
            'gate_location': '0',
            'online_boarding': '0',
            'seat_comfort': '5',
            'inflight_entertainment': '0',
            'on_board_service': '0',
            'baggage_handling': '4',
            'checkin_service': '0',
            'inflight_service': '0',
            'cleanliness': '0',
            'class_of_travel': 'Business'
        }

        result_ordered_dict = reorder_dict(dict_unordered_small)
        self.assertDictEqual(result_ordered_dict, dict_expected_ordered)

        # Test how the function reorders a full dictionary
        dict_unordered_full = {
            'baggage_handling': '2',
            'customer_type': 'Disloyal customer',
            'age': '67',
            'type_of_travel': 'Personal travel',
            'gate_location': '3',
            'online_boarding': '4',
            'inflight_entertainment': '2',
            'on_board_service': '3',
            'inflight_wifi_service': '1',
            'checkin_service': '1',
            'inflight_service': '3',
            'cleanliness': '2',
            'class_of_travel': 'Eco plus',
            'seat_comfort': '4'
        }

        dict_expected_full_ordered = {
            'customer_type': 'Disloyal customer',
            'age': '67',
            'type_of_travel': 'Personal travel',
            'inflight_wifi_service': '1',
            'gate_location': '3',
            'online_boarding': '4',
            'seat_comfort': '4',
            'inflight_entertainment': '2',
            'on_board_service': '3',
            'baggage_handling': '2',
            'checkin_service': '1',
            'inflight_service': '3',
            'cleanliness': '2',
            'class_of_travel': 'Eco plus'
        }

        result_reordered_full_dict = reorder_dict(dict_unordered_full)
        self.assertDictEqual(result_reordered_full_dict, dict_expected_full_ordered)

        # Test how the function reorders a dictionary with unnecessary keys
        dict_additional_keys = {
            'customer_type': 'Loyal customer',
            'age': '35',
            'type_of_travel': 'Business travel',
            'class_of_travel': 'Business',
            'seat_comfort': '5',
            'additional_key1': 'value1',
            'additional_key2': 'value2'
        }

        dict_expected = {
            'customer_type': 'Loyal customer',
            'age': '35',
            'type_of_travel': 'Business travel',
            'inflight_wifi_service': '0',
            'gate_location': '0',
            'online_boarding': '0',
            'seat_comfort': '5',
            'inflight_entertainment': '0',
            'on_board_service': '0',
            'baggage_handling': '0',
            'checkin_service': '0',
            'inflight_service': '0',
            'cleanliness': '0',
            'class_of_travel': 'Business'
        }

        result_additional_keys = reorder_dict(dict_additional_keys)
        self.assertDictEqual(result_additional_keys, dict_expected)

    def test_model_predict(self):
        satisfied_passenger = {
            'baggage_handling': '5',
            'customer_type': 'Loyal customer',
            'age': '60',
            'type_of_travel': 'Business travel',
            'gate_location': '1',
            'online_boarding': '5',
            'inflight_entertainment': '5',
            'on_board_service': '5',
            'inflight_wifi_service': '1',
            'checkin_service': '3',
            'inflight_service': '5',
            'cleanliness': '5',
            'class_of_travel': 'Business',
            'seat_comfort': '4'
        }

        expected_prediction_positive= 'the passenger is satisfied'

        with app.test_client() as client:
            response = client.post('/predict', data=satisfied_passenger)
            self.assertEqual(response.status_code, 200)
            self.assertIn(expected_prediction_positive, response.get_data(as_text=True))
            

        neutral_or_disatisfied_passenger = {
            'gate_location': '3',
            'online_boarding': '5',
            'inflight_entertainment': '2',
            'on_board_service': '3',
            'inflight_wifi_service': '4',
            'checkin_service': '4',
            'inflight_service': '4',
            'cleanliness': '2',
            'baggage_handling': '3',
            'customer_type': 'Disloyal customer',
            'age': '30',
            'type_of_travel': 'Business travel',
            'class_of_travel': 'Eco',
            'seat_comfort': '2'
        }

        expected_prediction_negative = 'the passenger is neutral or dissatisfied'

        with app.test_client() as client:
            response = client.post('/predict', data=neutral_or_disatisfied_passenger)
            self.assertEqual(response.status_code, 200)
            self.assertIn(expected_prediction_negative, response.get_data(as_text=True))

  
if __name__ == '__main__':
    unittest.main()
