import json
import boto3
import rest_interface


# TODO: Set the name of the bucket to use. If this isn't set then this Lambda Function will not store data in S3 or retrieve data from S3.
rest_interface.bucket = None


def handle_get(event):
    # Usually a GET method is intended to retrieve the content of one or more files in S3.
    # If obtain the content of a single file then use s3_get_object.
    # If obtaining content from multiple files then use s3_get_multiple_objects.
    # You may need to use the path parameter or value of a query parameter as the key of the object or the folder name.

    # param_name = "product"
    # query_param_val = rest_interface.get_query_parm(event, param_name)

    # path_param_val = rest_interface.get_path_param(event)

    response_body = {}
    ###### BEGIN - Get the content of a single object/file #####
    # TODO: provide code to create the correct key.
    # key = """

    # Get a single file
    # response_body = rest_interface.s3_get_object(key)
    ##### END - Get the content of a single object/file

    ###### BEGIN - Get the content of a multiple objects/files. #####

    # TODO: assign folder to the folder's name.  This could be constant or obtained from the query or path parameter.
    folder = None
    # response_body = rest_interface.s3_get_multiple_objects(bucket_name, folder)
    ##### END - Get the content of a multiple objects/files.

    return response_body


def handle_post(event):

    input_obj = rest_interface.get_body(event)

    # TODO: Create a unique name of the JSON to store in the folder. You may have to use an attribute in the JSON object to determine the name.
    key = None

    # TODO: You may have to make some changes to the json_obj or create a new object to store in S3.
    transformed_obj = input_obj

    rest_interface.s3_write_obj(key, transformed_obj)


def lambda_handler(event, context):
    httpMethod = event["httpMethod"]
    if httpMethod == "POST":
        return rest_interface.response(handle_post(event))
    elif httpMethod == "GET":
        return rest_interface.response(handle_get(event))
    return rest_interface.response(
        dict(msg="Unsupported method", method=httpMethod), statusCode=405
    )
