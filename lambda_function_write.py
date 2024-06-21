import os
import json
import time
import boto3
import logging

s3_client = boto3.client('s3')
textract_client = boto3.client('textract')


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    print(event)
    notificationMessage = json.loads(json.dumps(event))['Records'][0]['Sns']['Message']
    pdfTextExtractionDocumentLocation = json.loads(notificationMessage)['DocumentLocation']
    pdfTextExtractionStatus = json.loads(notificationMessage)['Status']
    print()
    pdfTextExtractionJobId = json.loads(notificationMessage)['JobId']
    pdfTextExtractionS3ObjectName = json.loads(json.dumps(pdfTextExtractionDocumentLocation))['S3ObjectName']
    pdfTextExtractionS3Bucket = json.loads(json.dumps(pdfTextExtractionDocumentLocation))['S3Bucket']
    
    job_id = pdfTextExtractionJobId

    #print(job_id)
    results = getJobResults(job_id)
    #event['job_update_timestamp'] = time.time()

    if pdfTextExtractionStatus != "SUCCEEDED":
        # Include the results unless the job is still in progress
        # Useful for investigating failures
        if pdfTextExtractionStatus != "IN_PROGRESS":
            event['results'] = results
        return event

    # Job succeeded - retrieve the results
    input_bucket = pdfTextExtractionS3Bucket
    input_object = pdfTextExtractionS3ObjectName
    output_bucket = input_bucket
    output_prefix = 'output/'

    output_object_base = os.path.join(output_prefix, os.path.basename(input_object))
    page_counter = 0
    blocks = []

    while True:
        page_counter += 1
        #print(len(blocks))

        if 'Blocks' in results:
            blocks.extend(results['Blocks'])

        if 'NextToken' not in results:
            break

        #print(f"NextToken: {results['NextToken']}")
        results = getJobResults(job_id, next_token=results['NextToken'])


    #print(len(blocks))
    # Save merged 'Blocks' into a separate file for ease of use
    output_object = f"{output_object_base}.blocks.json"
    s3_client.put_object(
        Bucket=output_bucket,
        Key=output_object,
        Body=json.dumps({'Blocks': blocks}),
        ServerSideEncryption='AES256',
        ContentType='application/json',
    )

    event['Blocks_raw']={
        "job_update_timestamp": time.time(),
        "output_bucket": output_bucket,
        "raw_results": [],
        "blocks": output_object
    }
    logging.info('JSON Block Mapping Created Correctly : '+output_object)
    return event

def getJobResults(job_id, next_token = None):
    kwargs = {}
    if next_token:
        kwargs['NextToken'] = next_token

    #print("kwargs")
    #print(kwargs)
    response = textract_client.get_document_analysis(JobId=job_id, **kwargs)
    return response