import unittest
from source.server import main 


# this is a sample for unittest
class TestServer(unittest.TestCase):

    def test_server(self):
        input_json = '{"field1": "value1", "field2": "value2", "field3": "value3"}'
        expected_output = {
            "field1": "value1",
            "field2": "value2",
            "field3": "value3"
        }

        json_to_dict = JsonToDict()
        result = list(json_to_dict.process(input_json))

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], expected_output)

if __name__ == '__main__':
    unittest.main()
