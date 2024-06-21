import http from 'http';
import express from 'express';
import S3read from './controller/s3read.controller'; // Asegúrate de que la ruta sea correcta
import LoggerGen from './utilities/LoggerGen';

const log = LoggerGen.getLoggingInstance('bdb:app');

const app = express();
const port = process.env.PORT || '3000';
console.log(`Log2`);

app.set('port', port);

app.use(express.json());

app.use(S3read);

console.log(`Log3`);

const server = http.createServer(app);

server.listen(port, () => {
  log.info(`Server running on port ${port}`);
});

export default app;