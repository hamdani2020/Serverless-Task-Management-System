import json

import boto3
from botocore.exceptions import ClientError

# Initialize DynamoDB client
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Tasks")


def lambda_handler(event, context):
    try:
        if isinstance(event, str):
            event = json.loads(event)
        elif "body" in event and isinstance(event["body"], str):
            event = json.loads(event["body"])
        task_id = event.get("TaskID")
        if not task_id:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                    "Access-Control-Allow-Methods": "GET, POST, DELETE, PUT, OPTIONS",
                },
                "body": json.dumps({"message": "Task ID is required"}),
            }

        # Check if user has admin role
        # if user_role.upper() != 'ADMIN':
        #     return {
        #         'statusCode': 403,
        #         'headers': {
        #             'Access-Control-Allow-Origin': '*',
        #             'Access-Control-Allow-Credentials': True
        #         },
        #         'body': json.dumps({'message': 'Unauthorized. Admin access required.'})
        #     }

        # Delete the task
        response = table.delete_item(
            Key={"TaskID": task_id},
            ReturnValues="ALL_OLD",  # This will return the deleted item
        )

        # Check if the item was found and deleted
        if "Attributes" not in response:
            return {
                "statusCode": 404,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Credentials": True,
                },
                "body": json.dumps({"message": "Task not found"}),
            }

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps(
                {
                    "message": "Task deleted successfully",
                    "deletedTask": response["Attributes"],
                }
            ),
        }

    except ClientError as e:
        print(f"ClientError: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
            },
            "body": json.dumps({"message": "Internal server error"}),
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal server error", "error": str(e)}),
        }
