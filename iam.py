import boto3
import json

class IAMRoleManager:
    def __init__(self, role_name, account_id, assume_role_policy_document):
        self.role_name = role_name
        self.account_id = account_id
        self.assume_role_policy_document = assume_role_policy_document
        self.client = boto3.client('iam')

    def create_role(self):
        try:
            response = self.client.create_role(
                RoleName=self.role_name,
                AssumeRolePolicyDocument=self.assume_role_policy_document
            )
            return response['Role']['Arn']
        except Exception as e:
            print(f"Failed to create IAM role: {e}")
            return None

    def attach_policy(self, policy_arn):
        try:
            response = self.client.attach_role_policy(
                RoleName=self.role_name,
                PolicyArn=policy_arn
            )
            print(f"Policy attached to IAM role {self.role_name}")
        except Exception as e:
            print(f"Failed to attach policy to IAM role: {e}")

class S3BucketPolicyManager:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client('s3')

    def create_bucket_policy(self, role_arn):
        try:
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "AllowCrossAccountAccess",
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": role_arn
                        },
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{self.bucket_name}/*",
                        "Condition": {
                            "StringEquals": {
                                "aws:RequestTag/SUPPORTED": "true"
                            }
                        }
                    }
                ]
            }

            response = self.client.put_bucket_policy(
                Bucket=self.bucket_name,
                Policy=json.dumps(policy)
            )
            print(f"Bucket policy updated for bucket {self.bucket_name}")
        except Exception as e:
            print(f"Failed to update bucket policy: {e}")

# Example usage
if __name__ == "__main__":
    # IAM role parameters
    role_name = "CrossAccountRole"
    account_id = "123456789012"  # Replace with the account ID
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},  # or "eks.amazonaws.com"
                "Action": "sts:AssumeRole",
                "Condition": {"StringEquals": {"sts:ExternalId": "some-external-id"}}
            }
        ]
    }

    # Create IAM role
    iam_manager = IAMRoleManager(role_name, account_id, json.dumps(assume_role_policy_document))
    role_arn = iam_manager.create_role()

    # Attach policies to IAM role
    if role_arn:
        policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"  # or any other policy ARN
        iam_manager.attach_policy(policy_arn)

        # Update S3 bucket policy
        bucket_name = "your-s3-bucket"
        s3_policy_manager = S3BucketPolicyManager(bucket_name)
        s3_policy_manager.create_bucket_policy(role_arn)
