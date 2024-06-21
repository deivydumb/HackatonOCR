const VERSIONS = {
	V1: '/V1/Enterprise',
};
const URI_DEFAULT = 'http://localhost:9001';
export default {
	CLOUD_LOGS: process.env.CLOUD_LOGS || 'false',
	LOG_LEVEL: process.env.LOG_LEVEL || 'silly',
	PORT: process.env.APPLICATION_PORT ?? '8001',
	ENV: process.env.NODE_ENV ?? 'LOCAL',
	AWS_REGION: process.env.REGION ?? 'us-east-1',
	CONTEXT: process.env.CONTEXT ?? '/my-context',
	PATHS: {
		CUSTOMERS: {
			PATH: `${VERSIONS.V1}/customers`,
			OPERATIONS: {
				CUSTOMER: '',
			},
			RESOURCE_URI: process.env.CUSTOMER_URI ?? URI_DEFAULT,
			RESOURCES: {
				GET_CUSTOMER_V2: '/wsptdoapi/customer/v2/personal',
			},
		},
		PRODUCTS: {
			PATH: `${VERSIONS.V1}/customers/products`,
			OPERATIONS: {
				PRODUCTS: '',
			},
			RESOURCE_URI: process.env.CUSTOMER_URI ?? URI_DEFAULT,
			RESOURCES: {
				GET_PRODUCTS_V2: '/wsptdoapi/customer/v2/personal/products',
			},
		},
	},
	RESOURCE: './static',
	OAS: {
		FILE: '/OAS.json',
		PATH: '/api-docs',
	},
	TVS: {
		API_KEY: process.env.TVS_API_KEY ?? '{ "secret_name":"EMPTY_KEY", "secret_key":"TVS_API_KEY"}',
	},
	API_PATH: '/default',
};
