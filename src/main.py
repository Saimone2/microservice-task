from fastapi import FastAPI, HTTPException
import boto3, os

app = FastAPI()

s3 = boto3.client(
    "s3",
    endpoint_url="http://minio-service:9000",
    aws_access_key_id=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
    aws_secret_access_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
)

@app.get("/api/bucket/{uuid}")
def get_bucket_info(uuid: str):
    try:
        response = s3.list_objects_v2(Bucket=uuid)
        total_size = sum(obj["Size"] for obj in response.get("Contents", []))
        total_count = response.get("KeyCount", 0)
        return {"bucket": uuid, "objects": total_count, "size": total_size}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/bucket/{uuid}")
def create_bucket(uuid: str):
    try:
        s3.create_bucket(Bucket=uuid)
        return {"status": "created", "bucket": uuid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/bucket/{uuid}")
def delete_bucket(uuid: str):
    try:
        s3.delete_bucket(Bucket=uuid)
        return {"status": "deleted", "bucket": uuid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
