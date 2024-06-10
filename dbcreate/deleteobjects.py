import boto3



bucket = "www.digitalsteve.net"
filename = "asset-manifest.json"

client = boto3.client('s3')
paginator = client.get_paginator('list_object_versions')
response_iterator = paginator.paginate(Bucket=bucket)
for response in response_iterator:
    versions = response.get('Versions', [])
    versions.extend(response.get('DeleteMarkers', []))
    for version_id in [x['VersionId'] for x in versions
                       if x['Key'] == filename and x['VersionId'] != 'null']:
        print('Deleting {} version {}'.format(filename, version_id))
        client.delete_object(Bucket=bucket, Key=filename, VersionId=version_id)