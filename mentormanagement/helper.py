def sen_message(email, message):
    return f"Send the email in {email} Id. and message is {message}"

import boto3
from botocore.exceptions import ClientError

def main_send_email(subject, body, to_address, from_address):
    aws_access_key = 'your-access-key'
    aws_secret_key = 'your-secret-key'
    region = 'us-east-1'
    ses = boto3.client('ses', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=region)
    sender = from_address
    recipient = to_address
    email_subject = subject
    email_body = body
    message = {
        'Subject': {
            'Data': email_subject
        },
        'Body': {
            'Text': {
                'Data': email_body
            }
        }
    }

    try:
        # Send the email
        response = ses.send_email(
            Source=sender,
            Destination={
                'ToAddresses': [recipient],
            },
            Message=message
        )
        print(f"Email sent! Message ID: {response['MessageId']}")

    except ClientError as e:
        print(f"Error sending email: {e.response['Error']['Message']}")

# Example usage
main_send_email(
    subject='Test Email',
    body='This is a test email sent from Amazon SES using Python.',
    to_address='recipient@example.com',
    from_address='sender@example.com'
)