import json
from datetime import datetime

import boto3

# Initialize AWS resources
dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")
tasks_table = dynamodb.Table("Tasks")


def lambda_handler(event, context):
    """
    AWS Lambda handler for updating a task in the database and sending notifications.
    """
    try:
        if isinstance(event, str):
            event = json.loads(event)
        elif "body" in event and isinstance(event["body"], str):
            event = json.loads(event["body"])
        task_id = event.get("id")
        status = event.get("status")
        timestamp = datetime.utcnow().isoformat()

        # Update the DynamoDB table
        response = tasks_table.update_item(
            Key={"TaskID": task_id},
            UpdateExpression="SET #status = :status, updated_at = :timestamp",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":status": status,
                ":timestamp": timestamp,
            },
            ReturnValues="ALL_NEW",
        )

        updated_task = response["Attributes"]

        # Notify about the status change via SNS
        sns.publish(
            TopicArn="arn:aws:sns:eu-west-1:195275667627:taskTopic",
            Message=json.dumps({"type": "TASK_UPDATED", "task": updated_task}),
        )

        # Return success response
        return {"statusCode": 200, "body": json.dumps(updated_task)}

    except Exception as e:
        # Return error response
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
