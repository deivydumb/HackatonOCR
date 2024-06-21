import express from 'express';
import LoggerGen from '../utilities/LoggerGen';
import { Request, Response } from 'express';
import * as AWS from 'aws-sdk';

const S3read = express.Router();

const log = LoggerGen.getLoggingInstance('bdb:DariController');

const tableName = 'scantalentdb';

AWS.config.update({
    region: 'us-east-1',
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
});
  

const dynamoDB = new AWS.DynamoDB.DocumentClient();



S3read.get('/default/health', async (req: Request, res: Response) => {
  try {
    console.log('Health check');
    const response = { data: 'Service is up and running' };

    if (response && response.data) {
      res.setHeader('Access-Control-Allow-Origin', '*');
      res.status(200).send(response.data);
    } else {
      throw new Error('Error while fetching data');
    }
  } catch (error: any) {
    log.error('Error while processing request', error.message);
    res.status(error.status || 500).send({ error: error.message || 'An unexpected error occurred' });
  }
});

S3read.get('/scan-dynamodb', async (req: Request, res: Response) => {
    try {
    AWS.config.update({region: 'us-east-1'});

      let items: AWS.DynamoDB.DocumentClient.ItemList = [];
      let params: AWS.DynamoDB.DocumentClient.ScanInput = {
        TableName: tableName,
      };
  
      let scanResults;
      do {
        scanResults = await dynamoDB.scan(params).promise();
        items = items.concat(scanResults.Items ?? []);
        params.ExclusiveStartKey = scanResults.LastEvaluatedKey;
      } while (scanResults.LastEvaluatedKey);
  
      res.status(200).json(items);
    } catch (error) {
      log.error('Error while scanning DynamoDB', error);
      res.status(500).send({ error: 'An unexpected error occurred' });
    }
  });

export default S3read;