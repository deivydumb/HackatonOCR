import json
import urllib.parse
import boto3
import os
import logging

role_arn = os.environ['RoleArn']
sns_arn = os.environ['SNSTopicArn']
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        s3BucketName = event['Records'][0]['s3']['bucket']['name']
        documentName = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        
        # Amazon Textract client
        textract = boto3.client('textract')
        
        # Call Amazon Textract
        try:
            response = textract.start_document_analysis(
                DocumentLocation={
                    'S3Object': {
                        'Bucket': s3BucketName,
                        'Name': documentName
                    }
                },
                FeatureTypes=['LAYOUT'],
                NotificationChannel={
                    'RoleArn': 'arn:aws:iam::267693165925:role/policyTextTrack',
                    'SNSTopicArn': 'arn:aws:sns:us-east-1:267693165925:TEXTRACK'
                }
            )
            print(response)
            logger.info('Proceso de Extraccion del Documento: ' + documentName + ' Iniciado')
            return 'Triggered PDF Processing for ' + documentName
        except Exception as e:
            logger.warning('Fallo en proceso, verificar estructura del archivo PDF cargado: ' + documentName)
            logger.error("Error al iniciar la extracción del documento: " + str(e))
            return 'Error al iniciar la extracción del documento: ' + documentName
        
    except Exception as e:
        logger.error("Error al procesar el evento: " + str(e))
        return 'Error al procesar el evento'
