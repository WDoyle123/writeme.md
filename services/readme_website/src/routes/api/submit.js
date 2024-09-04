import { connectToDatabase } from '$lib/mongo';

export async function post({ request }) {
	const data = await request.json();
	const db = await connectToDatabase();
	const collection = db.collection('submissions');

	try {
		const result = await collection.insertOne(data);
		return {
			status: 200,
			body: { success: true }
		};
	} catch (error) {
		return {
			status: 500, 
			body: { success: false, error: error.message }
		};
	}
]
