imoprt { MongoClient } from 'mongodb';

const client = new MongoClient(process.env.MONGODB_URI);

export async function connectToDatabase() {
	await client.connect();
	return client.db('db_name');
}

export const db = client.db('db_name');
