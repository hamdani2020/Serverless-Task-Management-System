import json
import logging
from datetime import datetime

import boto3
from botocore.exceptions import ClientError

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize SNS client
sns = boto3.client("sns")
SNS_TOPIC_ARN = "arn:aws:sns:eu-west-1:195275667627:taskTopic"


def lambda_handler(event, context):
    try:
        # Parse the incoming request body
        body = json.loads(event["body"])

        # Extract required fields
        email = body["email"]
        task_title = body["taskTitle"]
        deadline = body["deadline"]
        message = body["message"]

        # Format deadline date
        deadline_date = datetime.strptime(deadline, "%Y-%m-%d").strftime("%B %d, %Y")

        # Create email message
        email_message = f"""
        Task Deadline Reminder
        
        Task: {task_title}
        Deadline: {deadline_date}
        
        {message}
        
        This is an automated reminder. Please ensure to complete the task before the deadline.
        """

        # Set up the SNS message parameters
        sns_params = {
            "TopicArn": SNS_TOPIC_ARN,
            "Message": email_message,
            "Subject": f"Task Deadline Approaching: {task_title}",
            "MessageAttributes": {
                "email": {"DataType": "String", "StringValue": email}
            },
        }

        # Send the SNS notification
        response = sns.publish(**sns_params)

        logger.info(f"Notification sent successfully: {response['MessageId']}")

        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Configure appropriately for production
                "Access-Control-Allow-Credentials": True,
                "Content-Type": "application/json",
            },
            "body": json.dumps(
                {
                    "message": "Notification sent successfully",
                    "messageId": response["MessageId"],
                }
            ),
        }

    except KeyError as e:
        logger.error(f"Missing required field: {str(e)}")
        return {
            "statusCode": 400,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Content-Type": "application/json",
            },
            "body": json.dumps({"error": f"Missing required field: {str(e)}"}),
        }

    except ClientError as e:
        logger.error(f"SNS error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Content-Type": "application/json",
            },
            "body": json.dumps({"error": "Failed to send notification"}),
        }

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Credentials": True,
                "Content-Type": "application/json",
            },
            "body": json.dumps({"error": "Internal server error"}),
        }


def handle_options(event):
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Allow-Methods": "OPTIONS,POST",
            "Access-Control-Allow-Credentials": True,
        },
        "body": json.dumps({}),
    }
