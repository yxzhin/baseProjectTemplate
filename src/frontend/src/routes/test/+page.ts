export async function load({ fetch }) {
	const res = await fetch('http://localhost:8000/api/test/');

	return {
		test: await res.json()
	};
}
