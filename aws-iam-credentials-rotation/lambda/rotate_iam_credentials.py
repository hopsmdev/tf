"""
Lambda function to generate IAM User Access Key Id and Secret Access Key and store
user credentials in AWS Secrets Manager.

WARNING: A valid IAM User name has to be specified via IAM_USER_NAME environment variable

How does it work?

1) Create IAM User with user credentials - Access Key Id and Secret Access Key.
2) Update lambda function environment variable `IAM_USER_NAME` with your IAM User name.
3) Create new secret in AWS Secret Manager, configure automatic rotation and choose this lambda function
to rotate your secret.

https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html

"""

import boto3
import logging
import os
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

iam_client = boto3.client('iam')
service_client = boto3.client('secretsmanager')


def lambda_handler(event, context):
    """Secrets Manager Rotation Template

    This is a template for creating an AWS Secrets Manager rotation lambda

    Args:
        event (dict): Lambda dictionary of event parameters. These keys must include the following:
            - SecretId: The secret ARN or identifier
            - ClientRequestToken: The ClientRequestToken of the secret version
            - Step: The rotation step (one of createSecret, setSecret, testSecret, or finishSecret)

        context (LambdaContext): The Lambda runtime information

    Raises:
        ResourceNotFoundException: If the secret with the specified arn and stage does not exist

        ValueError: If the secret is not properly configured for rotation

        KeyError: If the event parameters do not contain the expected keys

    """
    
    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']


    # Make sure the version is staged correctly
    metadata = service_client.describe_secret(SecretId=arn)
    if not metadata['RotationEnabled']:
        logger.error("Secret %s is not enabled for rotation" % arn)
        raise ValueError("Secret %s is not enabled for rotation" % arn)
    versions = metadata['VersionIdsToStages']
    if token not in versions:
        logger.error("Secret version %s has no stage for rotation of secret %s." % (token, arn))
        raise ValueError("Secret version %s has no stage for rotation of secret %s." % (token, arn))
    if "AWSCURRENT" in versions[token]:
        logger.info("Secret version %s already set as AWSCURRENT for secret %s." % (token, arn))
        return
    elif "AWSPENDING" not in versions[token]:
        logger.error("Secret version %s not set as AWSPENDING for rotation of secret %s." % (token, arn))
        raise ValueError("Secret version %s not set as AWSPENDING for rotation of secret %s." % (token, arn))

    if step == "createSecret":
        create_secret(service_client, arn, token)

    elif step == "setSecret":
        set_secret(service_client, arn, token)

    elif step == "testSecret":
        test_secret(service_client, arn, token)

    elif step == "finishSecret":
        finish_secret(service_client, arn, token)

    else:
        raise ValueError("Invalid step parameter")


def create_secret(service_client, arn, token):
    """Create the secret

    This method first checks for the existence of a secret for the passed in token. If one does not exist, it will generate a
    new secret and put it with the passed in token.

    Args:
        service_client (client): The secrets manager service client

        arn (string): The secret ARN or other identifier

        token (string): The ClientRequestToken associated with the secret version

    Raises:
        ResourceNotFoundException: If the secret with the specified arn and stage does not exist

    """
    # Make sure the current secret exists
    service_client.get_secret_value(SecretId=arn, VersionStage="AWSCURRENT")

    # Now try to get the secret version, if that fails, put a new secret
    
    try:
        service_client.get_secret_value(SecretId=arn, VersionId=token, VersionStage="AWSPENDING")
        logger.info("createSecret: Successfully retrieved secret for %s." % arn)
    except service_client.exceptions.ResourceNotFoundException:
        # Get exclude characters from environment variable
        exclude_characters = os.environ['EXCLUDE_CHARACTERS'] if 'EXCLUDE_CHARACTERS' in os.environ else '/@"\'\\'
        
        key = rotate_iam_keys()
        secret_string = {
            "access_key_id": key["access_key"],
            "secret_access_key": key["secret_key"]
        }
        
        service_client.put_secret_value(SecretId=arn, ClientRequestToken=token, SecretString=json.dumps(secret_string), VersionStages=['AWSPENDING'])
        logger.info("createSecret: Successfully put secret for ARN %s and version %s." % (arn, token))
    
    
def set_secret(service_client, arn, token):
    """Set the secret

    This method should set the AWSPENDING secret in the service that the secret belongs to. For example, if the secret is a database
    credential, this method should take the value of the AWSPENDING secret and set the user's password to this value in the database.

    Args:
        service_client (client): The secrets manager service client

        arn (string): The secret ARN or other identifier

        token (string): The ClientRequestToken associated with the secret version

    """
    # This is where the secret should be set in the service
    logger.info("Nothing to do")


def test_secret(service_client, arn, token):
    """Test the secret

    This method should validate that the AWSPENDING secret works in the service that the secret belongs to. For example, if the secret
    is a database credential, this method should validate that the user can login with the password in AWSPENDING and that the user has
    all of the expected permissions against the database.

    Args:
        service_client (client): The secrets manager service client

        arn (string): The secret ARN or other identifier

        token (string): The ClientRequestToken associated with the secret version

    """
    # This is where the secret should be tested against the service
    pass


def finish_secret(service_client, arn, token):
    """Finish the secret

    This method finalizes the rotation process by marking the secret version passed in as the AWSCURRENT secret.

    Args:
        service_client (client): The secrets manager service client

        arn (string): The secret ARN or other identifier

        token (string): The ClientRequestToken associated with the secret version

    Raises:
        ResourceNotFoundException: If the secret with the specified arn does not exist

    """
    # First describe the secret to get the current version
    metadata = service_client.describe_secret(SecretId=arn)
    current_version = None
    for version in metadata["VersionIdsToStages"]:
        if "AWSCURRENT" in metadata["VersionIdsToStages"][version]:
            if version == token:
                # The correct version is already marked as current, return
                logger.info("finishSecret: Version %s already marked as AWSCURRENT for %s" % (version, arn))
                return
            current_version = version
            break

    # Finalize by staging the secret version current
    service_client.update_secret_version_stage(SecretId=arn, VersionStage="AWSCURRENT", MoveToVersionId=token, RemoveFromVersionId=current_version)
    logger.info("finishSecret: Successfully set AWSCURRENT stage to version %s for secret %s." % (token, arn))
    
    
def create_key(username):
  access_key_metadata = iam_client.create_access_key(UserName = username)
  access_key = access_key_metadata['AccessKey']['AccessKeyId']
  secret_key = access_key_metadata['AccessKey']['SecretAccessKey']
  return {
      "access_key": access_key, 
      "secret_key": secret_key
   }
  
  
def disable_key(access_key, username):
    try:
        iam_client.update_access_key(
            UserName=username, AccessKeyId=access_key, Status="Inactive")
        print(access_key + " has been disabled.")
    except ClientError as e:
        print("The access key with id %s cannot be found" % access_key)
      
      
def delete_key(access_key, username):
    try:
        iam_client.delete_access_key(UserName=username, AccessKeyId=access_key)
        print(access_key + " has been deleted.")
    except ClientError as e:
        print("The access key with id %s cannot be found" % access_key)
      

def list_access_key(user, status_filter):
    keydetails = iam_client.list_access_keys(UserName=user)
    key_details = {}
    user_iam_details = []

    # Some users may have 2 access keys.
    for keys in keydetails['AccessKeyMetadata']:
        key_details['UserName'] = keys['UserName']
        key_details['AccessKeyId'] = keys['AccessKeyId']
        key_details['status'] = keys['Status']
        user_iam_details.append(key_details)
        key_details = {}

    return user_iam_details


def rotate_iam_keys():
    user = os.environ.get('IAM_USER_NAME')
    if (not user): 
        err_msg = 'A valid username not specified via IAM_USER_NAME environment variable'
        logger.error(err_msg)
        return {
          'statusCode': 500,
          'body': err_msg
        }
    logger.info(user)
    
    user_iam_details = list_access_key(user=user, status_filter='Active')
    keys = []
    
    for _ in user_iam_details:
        disable_key(access_key=_['AccessKeyId'], username=_['UserName'])
        delete_key(access_key=_['AccessKeyId'], username=_['UserName'])
        keys.append(create_key(username=_['UserName']))
    
    return keys[0] # return only 1 Active key
    