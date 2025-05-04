 
import boto3 
from datetime import datetime, timedelta 
 
#    Configuration 
SENDER_EMAIL = '228r1a1278@gmail.com'           # Replace with SES sender 
RECEIVER_EMAIL = '228r1a1299@cmrec.ac.in'                    # Replace with verified receiver 
SNS_TOPIC_ARN = 'arn:aws:sns:ap-south-1:879381285442:s3-file-upload-topic'  # Replace with SNS ARN 
 
def lambda_handler(event, context): 
    try: 
        # 1 Get S3 file details 
        record = event['Records'][0] 
        bucket = record['s3']['bucket']['name'] 
        key = record['s3']['object']['key'] 
        timestamp = record['eventTime'] 
 
        # 2️ Convert UTC to IST 
        utc_time = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ") 
        ist_time = utc_time + timedelta(hours=5, minutes=30) 
        formatted_time = ist_time.strftime("%Y-%m-%d %I:%M:%S %p IST") 
 
        # 3️ Create Email content 
        subject = '   New File Uploaded to S3' 
        body_text = f""" 
        A new file has been uploaded. 
 
        File Name: {key} 
        Bucket: {bucket} 
        Uploaded At (IST): {formatted_time} 
        """ 
 
        body_html = f""" 
        <html> 
        <body> 
          <h2>   New File Uploaded to S3</h2> 
          <p><strong>File:</strong> {key}</p> 
          <p><strong>Bucket:</strong> {bucket}</p> 
          <p><strong>Uploaded At (IST):</strong> {formatted_time}</p> 
        </body> 
        </html> 
        """ 
 
        # 4️ Send SES Email 
        ses = boto3.client('ses', region_name='ap-south-1') 
        ses.send_email( 
            Source=SENDER_EMAIL, 
            Destination={'ToAddresses': [RECEIVER_EMAIL]}, 
            Message={ 
'Subject': {'Data': subject}, 
'Body': { 
'Text': {'Data': body_text}, 
'Html': {'Data': body_html} 
} 
} 
) 
# 5 Send SNS Notification 
sns = boto3.client('sns', region_name='ap-south-1') 
sns.publish( 
TopicArn=SNS_TOPIC_ARN, 
Subject='       
S3 Upload Notification', 
Message=f'File "{key}" uploaded to S3 bucket "{bucket}" at {formatted_time}.' 
) 
print("   
Email & SNS notification sent with IST time.") 
return {'statusCode': 200, 'body': 'Notifications sent with IST time'} 
except Exception as e: 
print("  
Error:", str(e)) 
return {'statusCode': 500, 'body': str(e)}