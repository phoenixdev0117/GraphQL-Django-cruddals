from utils.client import Client
from graphene_django.utils.testing import GraphQLTestCase
from graphql import get_introspection_query


# class VerifyResponseAssertionMixins:
#     def verify_response(self, response, expected_response):
#         if isinstance(expected_response, dict):
#             self.assertIsInstance(response, dict)
#             iterator = expected_response.items()
#         elif isinstance(expected_response, list):
#             self.assertIsInstance(response, list)
#             self.assertEqual(
#                 len(expected_response), len(response), msg="len(list) didn't match"
#             )
#             iterator = enumerate(expected_response)
#         else:
#             self.assertEqual(
#                 expected_response,
#                 response,
#                 msg=(
#                     "values didn't match :"
#                     + str(expected_response)
#                     + " == "
#                     + str(response)
#                 ),
#             )
#             return

#         for key, value in iterator:
#             if isinstance(value, (dict, list)):
#                 self.verify_response(response[key], value)
#             else:
#                 self.assertEqual(
#                     value,
#                     response[key],
#                     msg=(
#                         "values didn't match :"
#                         + str(value)
#                         + " == "
#                         + str(response[key])
#                     ),
#                 )


class SchemaTestCase(GraphQLTestCase):

    QUERY_GET_TYPE = """
        fragment ofType on __Type {
            kind
            name
            ofType {
                kind
                name
            }
        }

        fragment type on __Type {
            kind
            name
            ofType {
                ...ofType
            }
        }

        fragment inputValue on __InputValue {
            name
            description
            defaultValue
            type {
                ...type
            }
        }

        fragment field on __Field {
            name
            description
            type {
                ...type
            }
            args {
                ...inputValue
            }
        }

        query ($name: String!) {
            __type(name: $name) {
                name
                fields {
                ...field
                }
                inputFields {
                ...inputValue
                }
            }
        }
    """

    INTROSPECTION_QUERY = get_introspection_query()

    def get_schema(self):
        client = Client()
        return client.query(self.INTROSPECTION_QUERY).json()

    def get_type(self, name):
        client = Client()
        response = client.query(self.QUERY_GET_TYPE, variables={"name": name}).json()
        return response["data"]["__type"]

    def get_field(self, name):
        client = Client()
        response = client.query(self.QUERY_GET_TYPE, variables={"name": name}).json()
        return response["data"]["__type"]

    def get_field_by_name(self, type, name, input_field=False):
        fields_key = "inputFields" if input_field else "fields"
        return next(filter(lambda field: field["name"] == name, type[fields_key]))

    def assertFieldEqual(self, type_name, field_name, field_meta, input_type=False):
        gql_type = self.get_type(type_name)
        field = self.get_field_by_name(gql_type, field_name, input_field=input_type)
        self.assertDictEqual(field, field_meta)

    def run_test_graphql_type(self, type_name, fields_to_test, input_type=False):
        gql_type = self.get_type(type_name)
        for ref_field in fields_to_test:
            with self.subTest(field=ref_field):
                field = self.get_field_by_name(
                    gql_type, ref_field["name"], input_field=input_type
                )
                self.assertDictEqual(field, ref_field)

    def run_test_graphql_field(self, field_name:str, target_type:str, field_meta:dict):
        gql_type = self.get_type(target_type)
        field = self.get_field_by_name(gql_type, field_name)
        self.assertDictEqual(field, field_meta)

    def assertTypeIsComposeOfFields(self, type_name, field_names, input_type=False):
        fields_key = "inputFields" if input_type else "fields"
        gql_type = self.get_type(type_name)
        self.assertEqual(len(field_names), len(gql_type[fields_key]))
        for field in gql_type[fields_key]:
            self.assertIn(field["name"], field_names)

    def verify_response(self, response, expected_response, message=""):
        if isinstance(expected_response, dict):
            self.assertIsInstance(response, dict, msg=f"response is not a dict + {message}")
            self.assertEqual(len(expected_response), len(response), msg=f"len(dict) didn't match + {message}")
            iterator = expected_response.items()
        elif isinstance(expected_response, list):
            self.assertIsInstance(response, list, msg=f"response is not a list + {message}")
            self.assertEqual(len(expected_response), len(response), msg=f"len(list) didn't match + {message}")
            iterator = enumerate(expected_response)
        else:
            self.assertEqual(expected_response, response, msg=(
                "values didn't match :" + str(expected_response) + " == " + str(response) + " + " + message
            ))
            return

        for key, value in iterator:
            if isinstance(value, (dict, list)):
                self.verify_response(response[key], value, message=message)
            else:
                self.assertEqual(value, response[key], msg=(
                    "values didn't match in key:" + str(key) + " :" + str(value) + " == " + str(response[key]) + " + " + message
                ))