from os import name
import boto3
import csv
from botocore.exceptions import ClientError
import time

# AWS Region
AWS_REGION = "ap-south-1"

# Create a new SES resource and specify a region
ses_client = boto3.client('ses', region_name=AWS_REGION)

# Email parameters
SENDER = "admin@credcheck.pro"  # Replace with your verified sender email
SUBJECT = "Diwali Offer: 15% Off to Secure Your Hiring with CredCheck.Pro"

# External logo URL
LOGO_URL = "https://credcheckpro.s3.ap-south-1.amazonaws.com/CredCheck.Pro%20logo-5.png"

# Limit parameters
MAX_EMAILS_PER_SECOND = 10

# Email content
def create_email_body(name):  
    return f"""
    <html>
<head>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background: linear-gradient(to bottom, #000000, #6A0DAD); /* Purple to black gradient */
      color: #ffffff;
    }}
    .container {{
      background-color: rgba(30, 30, 30, 0.9);
      margin: 20px auto;
      padding: 20px;
      max-width: 600px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }}
    h2 {{
      color: #8952e0; /* Light purple */
      text-align: center;
    }}
    p {{
      line-height: 1.6;
      color: #ffffff; /* White text for better visibility */
    }}
    .logo {{
      display: block;
      margin: 0 auto;
      width: 220px;
      height: auto;
    }}
    .key-features {{
      color: #ffffff; /* White text for key features */
      font-weight: bold;
    }}
    .price {{
      text-decoration: line-through;
      color: #bbb;
    }}
    .current-price {{
      color: #FFD700; /* Gold */
      font-weight: bold;
    }}
    .offer {{
      background-color: #6A0DAD;
      padding: 10px;
      border-radius: 5px;
      color: #fff;
      text-align: center;
      margin: 20px 0;
      font-weight: bold;
    }}
    .link {{
      color: #FFD700; /* Gold for link */
      text-decoration: none;
    }}
    .link:hover {{
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  <div class="container">
    <img src="{LOGO_URL}" alt="CredCheck.Pro Logo" class="logo" style="display:block; margin:0 auto; width:220px; height:auto;" />

    <h2>Diwali Offer: 15% Off to Secure Your Hiring with CREDCHECK.PRO</h2>
    
    <p>Dear {name},</p>
    
    <p>Hiring the right employees is critical for your company’s success. But how do you ensure that each candidate is fully qualified and trustworthy? That’s where CREDCHECK.PRO comes in—and right now, we’re offering 15% off on all services during our Diwali special.</p>
    
    <p>Our AI-driven platform is trusted by leading companies to provide accurate, compliant, and fast employee background checks, making your hiring process more secure and efficient.</p>
    
    <p><strong>Can your current verification process guarantee this?</strong></p>

    <div class="offer">
      <h3>Limited-Time Offer:</h3>
      <p>Starter Plan: <span class="price">₹799/-</span> <span class="current-price">₹599/-</span></p>
      <p>Growth Plan: <span class="price">₹1499/-</span> <span class="current-price">₹1199/-</span></p>
      <p>Enterprise Plan: <span class="price">₹1999/-</span> <span class="current-price">₹1499/-</span></p>
    </div>
    
    <p class="key-features">Accuracy That Protects Your Business: Our AI ensures every detail is verified, reducing hiring risks.</p>
    <p class="key-features">Speed You Need: Fast results, so you can focus on growing your team.</p>
    <p class="key-features">Customizable to Your Needs: Choose only the checks you need with easy API integrations.</p>
    
    <p>Can your company afford to make a hiring mistake? With the competitive market, ensuring you’re bringing on the best candidates is more important than ever. Let us show you how CredCheck.Pro can transform your hiring process.</p>
    
    <p>Are you available for a quick chat, or would you prefer to <a href="https://credcheck.pro/" class="link">schedule a demo here?</a></p>
    
    <p>Act now and take advantage of our Diwali offer before it’s too late!</p>
    
    <p>Best regards,<br>Dr. Ishit Karoli<br>CEO<br>CREDCHECK.PRO<br>admin@credcheck.pro</p>
    </div>
</body>
</html>
"""

# Text fallback
def create_email_text(name):
    return f"""
    Diwali Offer: 15% Off to Secure Your Hiring with CredCheck.Pro
    <img src="{LOGO_URL}" alt="CredCheck.Pro Logo" class="logo" style="display:block; margin:0 auto; width:220px; height:auto;" />
    Dear {name},
    Hiring the right employees is critical for your company’s success. But how do you ensure that each candidate is fully qualified and trustworthy? That’s where CredCheck.Pro comes in—and right now, we’re offering 15% off on all services during our Diwali special.
    Our AI-driven platform is trusted by leading companies to provide accurate, compliant, and fast employee background checks, making your hiring process more secure and efficient.
    Can your current verification process guarantee this?
    Limited-Time Offer:
    Starter Plan: ₹599/- (was ₹799/-)
    Growth Plan: ₹1199/- (was ₹1499/-)
    Enterprise Plan: ₹1499/- (was ₹1999/-)
    
    Accuracy That Protects Your Business: Our AI ensures every detail is verified, reducing hiring risks.
    Speed You Need: Fast results, so you can focus on growing your team.
    Customizable to Your Needs: Choose only the checks you need with easy API integrations.
    Can your company afford to make a hiring mistake? With the competitive market, ensuring you’re bringing on the best candidates is more important than ever. Let us show you how CredCheck.Pro can transform your hiring process.
    Are you available for a quick chat or would you prefer to schedule a demo here? Act now and take advantage of our Diwali offer before it’s too late!
    Best regards,
    Dr. Ishit Karoli
    CEO
    CREDCHECK.PRO
    admin@credcheck.pro
"""

# Send email to each recipient with a limit
def send_bulk_emails():
    with open('output_data.csv', mode='r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header if it exists

        with open('email_aws_sent.csv', mode='a', newline='') as log_file:
            log_writer = csv.writer(log_file)
            log_writer.writerow(['Recipient Name', 'Email', 'Message ID', 'Status'])

            batch_count = 0

            for row in reader:
                recipient_name = row[0]
                recipient_email = row[1]
                
                # Create the email body
                BODY_HTML = create_email_body(recipient_name)
                BODY_TEXT = create_email_text(recipient_name)

                try:
                    response = ses_client.send_email(
                        Destination={
                            'ToAddresses': [recipient_email],
                        },
                        Message={
                            'Body': {
                                'Html': {
                                    'Charset': 'UTF-8',
                                    'Data': BODY_HTML,
                                },
                                'Text': {
                                    'Charset': 'UTF-8',
                                    'Data': BODY_TEXT,
                                },
                            },
                            'Subject': {
                                'Charset': 'UTF-8',
                                'Data': SUBJECT,
                            },
                        },
                        Source=SENDER,
                    )
                    # Log success
                    log_writer.writerow([recipient_name, recipient_email, response['MessageId'], 'Sent'])
                    print(f"Email sent to {recipient_name} ({recipient_email})! Message ID: {response['MessageId']}")
                
                except ClientError as e:
                    # Log failure
                    log_writer.writerow([recipient_name, recipient_email, '', f"Failed: {e.response['Error']['Message']}"])
                    print(f"Error sending to {recipient_name} ({recipient_email}): {e.response['Error']['Message']}")

                # Increment batch counter and sleep if limit is reached
                batch_count += 1
                if batch_count == MAX_EMAILS_PER_SECOND:
                    print(f"Reached the limit of {MAX_EMAILS_PER_SECOND} emails per second. Sleeping for 1 second...")
                    time.sleep(1)
                    batch_count = 0  # Reset counter after sleep

# Execute email sending
send_bulk_emails()