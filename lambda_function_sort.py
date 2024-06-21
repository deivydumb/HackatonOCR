import os 
from ast import Try
from io import StringIO
import boto3
import json 
import time
import json 
import random
import csv
import logging
from boto3.dynamodb.conditions import Key, Attr
from datetime import datetime , timedelta

s3_resources = boto3.resource("s3")
s3_client = boto3.client('s3')
textract = boto3.client('textract')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
dynamodb = boto3.resource("dynamodb")
dynamo_banco_MAESTRA_table = dynamodb.Table('scantalentdb')


def lambda_handler(event, context):
    print(event)
    notification_message = event['Records'][0]['Sns']['Message']
    data_document = json.loads(notification_message)
    data = json.loads(data_document['requestPayload']['Records'][0]['Sns']['Message'])
    pdf_text_extraction_document_location = data['DocumentLocation']
    pdf_text_extraction_job_id = data['JobId']
    pdf_text_extraction_s3_object_name = pdf_text_extraction_document_location['S3ObjectName']
    pdf_text_extraction_s3_bucket = pdf_text_extraction_document_location['S3Bucket']
    s3_client = boto3.client('s3')
    content_object = s3_client.get_object(Bucket=pdf_text_extraction_s3_bucket, Key=pdf_text_extraction_s3_object_name)
    file_content = content_object['Body'].read().decode('utf-8')

    blocks_data = json.loads(file_content)
    blocks = blocks_data['Blocks']
    

    datos = process_textract_response(blocks)
    datos3= process_resume_data(datos)
    
    
    response = dynamo_banco_MAESTRA_table.put_item(
            Item={
                'scantalentdb': pdf_text_extraction_s3_object_name,  
                'info': {
                    'data': datos3
                }
            }
        )
    return {
        'statusCode': 200,
        'body':(datos3)
    }
    

def process_textract_response(blocks):
    document_content = {}
    perfil =[]

    # Crear un diccionario para almacenar las líneas asociadas a cada página
    page_lines = {}
    for data in blocks:
        if data['BlockType'] == 'LINE':
            perfil.append(data['Text'])
    return information(perfil)

def information(data):
    posicion_perfil = None
    posicion_experiencia = None
    posicion_educacion = None
    posicion_otras =None
    data2 = {}
    for i, linea in enumerate(data):
        if linea.strip() == "Perfil Profesional":
            posicion_perfil = i
            break
    for i, linea in enumerate(data):
        if linea.strip() == "Experiencia Laboral":
            posicion_experiencia = i
            break
    for i, linea in enumerate(data):
        if linea.strip() == "Educación":
            posicion_educacion = i
            break
    for i, linea in enumerate(data):
        if linea.strip() == "Habilidades Técnicas":
            posicion_otras = i
            break
            

        
    data2['informacion'] = data[:posicion_perfil]
    data2['perfil'] = data[posicion_perfil:posicion_experiencia]
    data2['experiencia'] = data[posicion_experiencia:posicion_educacion]
    data2['educacion']= data[posicion_educacion:posicion_otras]
    data2['habilidades'] = data[posicion_otras:]
    return(data2)
    
def process_resume_data(json_data):
    try:
        # Extraer la información del currículum del JSON
        informacion = json_data.get('informacion', [])
        perfil = json_data.get('perfil', [])
        experiencia = json_data.get('experiencia', [])
        educacion = json_data.get('educacion', [])
        habilidades = json_data.get('habilidades', [])

        # Extraer nombre del candidato, teléfono y correo electrónico
        nombre = informacion[1].split(': ')[1]
        telefono = informacion[2].split(': ')[1]
        correo = informacion[3].split(': ')[1]

        # Extraer perfil profesional
        perfil_profesional = perfil[1]

        # Extraer experiencia laboral
        experiencia_laboral = []
        i = 1
        while i < len(experiencia):
            empresa = experiencia[i]
            cargo = experiencia[i + 1]
            periodo_trabajo = experiencia[i + 2]
            responsabilidades = experiencia[i + 3:i + 7]  # Tomamos las siguientes 4 líneas como responsabilidades
            experiencia_laboral.append({
                'empresa': empresa,
                'cargo': cargo,
                'periodo_trabajo': periodo_trabajo,
                'responsabilidades': responsabilidades
            })
            i += 7

        # Extraer educación
        educacion_info = []
        i = 1
        while i < len(educacion):
            grado_academico = educacion[i]
            institucion = educacion[i + 1]
            periodo_estudio = educacion[i + 2]
            educacion_info.append({
                'grado_academico': grado_academico,
                'institucion': institucion,
                'periodo_estudio': periodo_estudio
            })
            i += 3

        # Extraer habilidades técnicas y blandas
        habilidades_info = habilidades[1:8]  # Tomamos las primeras 7 líneas de habilidades técnicas

        # Extraer certificaciones
        certificaciones = habilidades[9:]  # Tomamos las certificaciones si están presentes

        # Construir el objeto de respuesta
        extracted_info = {
            'nombre_del_candidato': nombre,
            'contacto': {
                'telefono': telefono,
                'correo_electronico': correo
            },
            'perfil_profesional': perfil_profesional,
            'experiencia_laboral': experiencia_laboral,
            'educacion': educacion_info,
            'habilidades': habilidades_info
        }

        # Agregar certificaciones si están presentes
        if certificaciones:
            extracted_info['certificaciones'] = certificaciones

        return extracted_info

    except ValueError as ve:
        raise ValueError("No se encontró un cuerpo de solicitud válido.")

    except Exception as e:
        raise e