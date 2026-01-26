import { error } from '@sveltejs/kit';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
	const page = Number(url.searchParams.get('page') ?? 1);
	const limit = Number(url.searchParams.get('limit') ?? 5);

	const res = await fetch(`http://localhost:8000/users?page=${page}&limit=${limit}`);

	if (!res.ok) {
		throw error(res.status, await res.text());
	}

	const data = await res.json();

	return {
		users: data.users ?? [],
		total: data.total ?? 0,
		page,
		limit
	};
};
