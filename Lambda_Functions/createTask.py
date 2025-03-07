import json
import uuid
from datetime import datetime

import boto3

dynamodb = boto3.resource("dynamodb")
sns = boto3.client("sns")
tasks_table = dynamodb.Table("Tasks")


def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))

        if not all(
            key in body for key in ["title", "description", "assignee", "deadline"]
        ):
            return {
                "statusCode": 400,
                "body": json.dumps(
                    {"error": "Missing required fields in the request body."}
                ),
            }

        task_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        task = {
            "TaskID": task_id,
            "title": body["title"],
            "description": body["description"],
            "assignee": body["assignee"],
            "deadline": body["deadline"],
            "status": "PENDING",
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        # Save task to DynamoDB
        tasks_table.put_item(Item=task)

        # Notify the assignee via SNS
        sns.publish(
            TopicArn="arn:aws:sns:eu-west-1:195275667627:taskTopic",
            Message=json.dumps({"type": "TASK_ASSIGNED", "task": task}),
        )

        return {"statusCode": 201, "body": json.dumps(task)}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
