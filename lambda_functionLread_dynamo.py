import json
import boto3


table_name = 'scantalentdb'


dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    try:
        response = dynamodb.scan(
            TableName=table_name
        )
        items = response.get('Items', [])
        
        # Itera sobre los items encontrados
        for item in items:
            print(f"Item encontrado: {item}")
    
        # Si la respuesta tiene más items, se pueden recuperar usando paginación
        while 'LastEvaluatedKey' in response:
            response = dynamodb.scan(
                TableName=table_name,
                ExclusiveStartKey=response['LastEvaluatedKey']
            )
            items = response.get('Items', [])
            for item in items:
                print(f"Item encontrado (página siguiente): {item}")
        return items
        
    except dynamodb.exceptions.DynamoDBError as e:
        print(f"Error al escanear la tabla DynamoDB: {e}")
