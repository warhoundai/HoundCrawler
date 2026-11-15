"""Real S3 contract check using a narrowly scoped ephemeral OIDC role."""
import hashlib,json,os,secrets
from houndcrawler.storage_backends import S3Backend
from botocore.exceptions import ClientError
bucket=os.environ['HOUNDCRAWLER_TEST_BUCKET'];prefix='test/houndcrawler/'+os.environ['GITHUB_RUN_ID']+'/'+secrets.token_hex(8)
backend=S3Backend('s3://'+bucket+'/'+prefix);key='tenant/object';data=b'Controlled HoundCrawler S3 contract evidence'
try:
    backend.put(key,data,'text/plain');assert backend.get(key,len(data))==data
    try:
        backend.client.get_object(Bucket=bucket,Key='outside-test-prefix/'+secrets.token_hex(16))
    except ClientError as e:assert e.response['Error']['Code'] in ('AccessDenied','403')
    else:raise RuntimeError('Qualification role can read outside its permitted prefix')
    print(json.dumps({'s3_roundtrip_verified':True,'sha256':hashlib.sha256(data).hexdigest(),'outside_prefix_denied':True}))
finally:backend.delete(key)
