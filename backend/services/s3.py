import boto3
import uuid
from typing import Optional, Dict, Any
from fastapi import UploadFile, HTTPException
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET_NAME
from botocore.exceptions import ClientError
import mimetypes
from PIL import Image
import io

class S3Service:
    """AWS S3 service for file uploads and management."""
    
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            region_name=AWS_REGION
        )
        self.bucket_name = S3_BUCKET_NAME
    
    def upload_file(self, file: UploadFile, folder: str = "media") -> Dict[str, Any]:
        """Upload a file to S3 and return metadata."""
        try:
            # Generate unique filename
            file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            s3_key = f"{folder}/{unique_filename}"
            
            # Get file content
            file_content = file.file.read()
            file.file.seek(0)  # Reset file pointer
            
            # Determine content type
            content_type = file.content_type or mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=content_type,
                ACL='private'  # Private by default for security
            )
            
            # Generate presigned URL for access
            presigned_url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=3600  # 1 hour
            )
            
            # Get file metadata
            file_size = len(file_content)
            
            # If it's an image, get dimensions
            width, height = None, None
            if content_type.startswith('image/'):
                try:
                    image = Image.open(io.BytesIO(file_content))
                    width, height = image.size
                except Exception:
                    pass  # If we can't get dimensions, that's okay
            
            return {
                "s3_key": s3_key,
                "filename": file.filename,
                "content_type": content_type,
                "size": file_size,
                "width": width,
                "height": height,
                "url": presigned_url
            }
            
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file to S3: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error during file upload: {str(e)}"
            )
    
    def delete_file(self, s3_key: str) -> bool:
        """Delete a file from S3."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except ClientError as e:
            print(f"Error deleting file {s3_key}: {str(e)}")
            return False
    
    def get_presigned_url(self, s3_key: str, expiration: int = 3600) -> str:
        """Generate a presigned URL for accessing a file."""
        try:
            response = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=expiration
            )
            return response
        except ClientError as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate presigned URL: {str(e)}"
            )
    
    def get_file_metadata(self, s3_key: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a file in S3."""
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return {
                "size": response['ContentLength'],
                "content_type": response['ContentType'],
                "last_modified": response['LastModified'],
                "etag": response['ETag']
            }
        except ClientError:
            return None

# Global S3 service instance
s3_service = S3Service()
