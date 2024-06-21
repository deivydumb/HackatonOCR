const app = require('./build/app').default;
const isInLambda = !!process.env.LAMBDA_TASK_ROOT;

console.log(`Ejecutando en Lambda: ${isInLambda}`);
console.log(`LAMBDA_TASK_ROOT: ${process.env.LAMBDA_TASK_ROOT}`);

if (isInLambda) {
    const serverlessExpress = require('aws-serverless-express');
    const server = serverlessExpress.createServer(app);
    console.log(`Log1`);
    exports.handler = (event, context) => {
        console.log('Evento de Lambda:', JSON.stringify(event, null, 2));
        console.log('Contexto de Lambda:', JSON.stringify(context, null, 2));
        console.log(server);
        serverlessExpress.proxy(server, event, context);
    }
} else {
    console.error('Error ejecutando como lambda.');
}