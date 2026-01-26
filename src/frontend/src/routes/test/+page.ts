export async function load({ fetch }) {
	const res = await fetch('http://localhost:8000/test/');

	return {
		test: await res.json()
	};
}
