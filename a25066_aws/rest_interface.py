import json
import boto3

s3 = boto3.resource("s3")

# TODO: Set the name of the bucket to use. If this isn't set then this Lambda Function will not store data in S3 or retrieve data from S3.
bucket = None


def response(json_obj=None, statusCode=200, event=None):
    """
    Return the dictionary as the body of the response message.
    """
    if json_obj is None:
        json_obj = dict()

    if "headers" in event:
        json_obj = json.dumps(json_obj)

    return {"statusCode": statusCode, "body": json_obj}


def get_query_parm(event, query_parm_name):
    """
    Get the value of the query parameter with the name stored in query_parm_name.
    """
    try:
        params = event["queryStringParameters"]
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
    vals = event["products"]
    return None if vals is None else vals[0]


def get_body(event):
    """
    Get the body of the request.
    """
    # When API Gateway sends a request the body is serialized.
    if "headers" in event:
        return json.loads(event["body"])
    return event["body"]


def s3_get_object(key):
    print("bucket =", bucket, "key =", key)
    if bucket is None:
        return {}
    object = s3.Object(bucket, key)
    print("object with key", key, "is", object)
    stream = object.get()
    if stream is None:
        return {}
    data = str(stream["Body"].read(), "utf-8")
    data = json.loads(data)
    return data


def s3_get_multiple_objects(folder):
    """
    Return the contents of all of the objects/files from a folder in a specific S3 bucket.
    It is assumed that the files are JSON objects.
    The returned value will be a list of dictionaries.
    """
    print("bucket =", bucket, "folder =", folder)
    if bucket is None:
        return {}
    s3_bucket = s3.Bucket(bucket)
    if len(folder) > 0 and folder[-1] != "/":
        prefix = f"{folder}/"
    else:
        prefix = folder

    print("prefix =", prefix)
    contents = []
    for object_summary in s3_bucket.objects.filter(Prefix=prefix):
        key = object_summary.key
        object = s3.Object(bucket, key)
        contents.append(json.loads(object.get()["Body"].read().decode("utf-8")))
    return contents


def s3_write_obj(key, json_obj):
    print("key=", key, json_obj)
    if bucket is None:
        return
    object = s3.Object(bucket, key)
    data = bytes(json.dumps(json_obj), "utf-8")
    object.put(Body=data, ContentType="application/json")
    return
