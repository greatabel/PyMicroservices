import json
import boto3
import rest_interface


#TODO: Set the name of the bucket to use. If this isn't set then this Lambda Function will not store data in S3 or retrieve data from S3.
rest_interface.bucket = "desu-rmoten-shopping-list-app"


def handle_get(event):
    # Usually a GET method is intended to retrieve the content of one or more files in S3.
    # If obtain the content of a single file then use s3_get_object.
    # If obtaining content from multiple files then use s3_get_multiple_objects.
    # You may need to use the path parameter or value of a query parameter as the key of the object or the folder name.

    param_name = "uuid"
    query_param_val = rest_interface.get_query_parm(event, param_name)

    # path_param_val = rest_interface.get_path_param(event)

    response_body = {}
    ###### BEGIN - Get the content of a single object/file #####
    # TODO: provide code to create the correct key.
    uuid = query_param_val

    # If the query parameter is present, then get a single member.
    if uuid is not None:
        # Get a single file
        key = f"/members/{uuid}"
        response_body = rest_interface.s3_get_object(key)
        print("response_body = ", response_body)

    else:
        #Get all members
        folder = ""
        response_body = rest_interface.s3_get_multiple_objects(folder)

    return response_body

def handle_post(event):

    member_signup = rest_interface.get_body(event)
    print("member_signup = ", member_signup)

    #TODO: Create a unique name of the JSON to store in the folder. You may have to use an attribute in the JSON object to determine the name.
    import hashlib
    m = hashlib.md5()
    m.update(member_signup['email'].encode())
    uuid = m.hexdigest()
    key = f"/members/{uuid}"

    # TODO: You may have to make some changes to the json_obj or create a new object to store in S3.
    member = dict(key=key, name=member_signup["name"], email=member_signup["email"])

    rest_interface.s3_write_obj(key, member)

    return dict(uuid=uuid)



def lambda_handler(event, context):
    httpMethod = event["httpMethod"]
    if httpMethod == "POST":
        return rest_interface.response(handle_post(event), event=event)
    elif httpMethod == "GET":
        return rest_interface.response(handle_get(event), event=event)
    return rest_interface.response(dict(msg="Unsupported method", method=httpMethod), statusCode=405)
