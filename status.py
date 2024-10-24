import boto3
import csv

# Initialize clients
ses_client = boto3.client('ses', region_name='ap-south-1')
sns_client = boto3.client('sns', region_name='ap-south-1')
cloudwatch_client = boto3.client('logs', region_name='ap-south-1')

# File path for email_aws_sent.csv in the project root folder
file_path = './email_aws_sent.csv'

# Function to fetch message IDs from CSV file
def get_message_ids_from_csv(file_path):
    message_ids = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            message_id = row[2]  # Assuming the third column contains the message ID
            message_ids.append(message_id)
    return message_ids

# Function to query CloudWatch logs for SES event logs (you need CloudWatch log setup for this)
def check_email_status_cloudwatch(message_id):
    log_group_name = '/aws/ses/email_delivery'  # Adjust if needed for your setup
    log_stream_name_prefix = f'{message_id}/'

    # Fetch logs from CloudWatch for the message
    response = cloudwatch_client.filter_log_events(
        logGroupName=log_group_name,
        logStreamNamePrefix=log_stream_name_prefix,
    )

    for event in response.get('events', []):
        print(f"Message ID: {message_id}, Log: {event['message']}")

# Main function to process each message ID and check status
def main():
    message_ids = get_message_ids_from_csv(file_path)

    for message_id in message_ids:
        print(f"Checking status for Message ID: {message_id}")

        # Check status from CloudWatch logs
        check_email_status_cloudwatch(message_id)

if __name__ == "__main__":
    main()
