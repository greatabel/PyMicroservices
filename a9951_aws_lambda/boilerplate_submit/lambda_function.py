import json
import boto3
import rest_interface

s3 = boto3.resource('s3')

#TODO: Set the name of the bucket to use. If this isn't set then this Lambda Function will not store data in S3 or retrieve data from S3.
bucket = 'desu-jiaruizhong-shopping-list-app'

def response(json_obj=None, statusCode=200, event=None):
    """
    Return the dictionary as the body of the response message.
    """
    if json_obj is None:
        json_obj = dict()

    if 'headers' in event:
        json_obj = json.dumps(json_obj)

    return {
        'statusCode': statusCode,
        'body': json_obj
    }


def get_query_parm(event, query_parm_name):
    """
    Get the value of the query parameter with the name stored in query_parm_name.
    """
    try:
        params = event['queryStringParameters']
        if params is not None:
            return params[query_parm_name]
        return None
    except KeyError:
        return None

def get_path_param(event):
    """
    Get the path parameter that is at the end of the URL.
    There should only be at most one.
    """
    vals = event['pathParameters']
    return None if vals is None else vals[0]

def get_body(event):
    """
    Get the body of the request.
    """
    # When API Gateway sends a request the body is serialized.
    if 'headers' in event:
        return json.loads(event['body'])
    return event['body']


def s3_get_object(key):
    print("bucket =", bucket, "key =", key)
    if bucket is None:
        return {}
    object = s3.Object(bucket, key)
    print("object with key", key, "is", object)
    stream = object.get()
    if stream is None:
        return {}
    data = str(stream['Body'].read(), "utf-8")
    data = json.loads(data)
    return data





def s3_write_obj(key, json_obj):
    print("key=",key, json_obj)
    if bucket is None:
        return
    object = s3.Object(bucket, key)
    data = bytes(json.dumps(json_obj), "utf-8")
    object.put(Body=data, ContentType="application/json")
    return

def myself_s3_get_multiple_objects(bucket, name_param, category_param):
    """
    Return the contents of all of the objects/files from a folder in a specific S3 bucket.
    It is assumed that the files are JSON objects.
    The returned value will be a list of dictionaries.
    """
    # print("bucket =", bucket, "folder =", folder)
    if bucket is None:
        return {}
    s3_bucket = s3.Bucket(bucket)

    contents = []
    for object_summary in s3_bucket.objects.all():
        key = object_summary.key
        object = s3.Object(bucket, key)
        value = json.loads(object.get()['Body'].read().decode('utf-8'))['product']['category']
        print('#key=', key, 'value=',value)
        if name_param != '':
            if key == name_param:
                contents.append(json.loads(object.get()['Body'].read().decode('utf-8')))
        if category_param != '':
            if value== category_param:
                contents.append(json.loads(object.get()['Body'].read().decode('utf-8')))
        if name_param == '' and category_param == '':
            contents.append(json.loads(object.get()['Body'].read().decode('utf-8')))
    return contents

def handle_get(event):
    # Usually a GET method is intended to retrieve the content of one or more files in S3.
    # If obtain the content of a single file then use s3_get_object.
    # If obtaining content from multiple files then use s3_get_multiple_objects.
    # You may need to use the path parameter or value of a query parameter as the key of the object or the folder name.

    param_name = "name"
    name_param = get_query_parm(event, param_name)
    param_category = 'category'
    category_param = get_query_parm(event, param_category)
    print('name_param=', name_param, category_param)
    # path_param_val = rest_interface.get_path_param(event)

    response_body = {}
    ###### BEGIN - Get the content of a single object/file #####
    # TODO: provide code to create the correct key.
    #key = """

    # Get a single file
    #response_body = rest_interface.s3_get_object(key)
    ##### END - Get the content of a single object/file


    ###### BEGIN - Get the content of a multiple objects/files. #####

    # TODO: assign folder to the folder's name.  This could be constant or obtained from the query or path parameter.
    folder = "/"
    response_body = myself_s3_get_multiple_objects(bucket, name_param, category_param)
    return response_body
    ##### END - Get the content of a multiple objects/files.

    return response_body

def handle_post(event):

    input_obj = rest_interface.get_body(event)

    #TODO: Create a unique name of the JSON to store in the folder. You may have to use an attribute in the JSON object to determine the name.
    key = input_obj['product']['name']
    category = input_obj['product']['category']
    print('key=', key)
    # TODO: You may have to make some changes to the json_obj or create a new object to store in S3.
    transformed_obj = input_obj
    if key != '' and category != '':
        rest_interface.s3_write_obj(key, transformed_obj)
    return event['body']


def lambda_handler(event, context):
    print('event=', event)
    httpMethod = event["httpMethod"]
    if httpMethod == "POST":
        return rest_interface.response(handle_post(event))
    elif httpMethod == "GET":
        return rest_interface.response(handle_get(event))
    return rest_interface.response(dict(msg="Unsupported method", method=httpMethod), statusCode=405)
