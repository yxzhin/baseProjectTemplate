<script lang="ts">
	import { goto } from '$app/navigation';

	export let data;

	let { users, total, page, limit } = data;

	$: totalPages = Math.max(1, Math.ceil(total / limit));

	$: pages = (() => {
		const maxShow = 7;
		let start = Math.max(1, page - Math.floor(maxShow / 2));
		let end = Math.min(totalPages, start + maxShow - 1);
		if (end - start + 1 < maxShow) {
			start = Math.max(1, end - maxShow + 1);
		}
		return Array.from({ length: end - start + 1 }, (_, i) => start + i);
	})();

	function gotoPage(p: number) {
		if (p < 1 || p > totalPages || p === page) return;
		goto(`?page=${p}&limit=${limit}`); // eslint-disable-line
	}

	function changeLimit(e: Event) {
		const newLimit = Number((e.target as HTMLSelectElement).value);
		goto(`?page=1&limit=${newLimit}`); // eslint-disable-line
	}

	function avatarFallback(e: Event) {
		(e.target as HTMLImageElement).src = 'https://placehold.co/120x120?text=No+Avatar';
	}
</script>

<main class="mx-auto max-w-6xl p-4">
	<header class="mb-4 flex items-center justify-between">
		<h1 class="text-2xl font-semibold">users</h1>

		<select class="rounded border px-2 py-1" bind:value={limit} on:change={changeLimit}>
			<option value="5">5</option>
			<option value="10">10</option>
			<option value="20">20</option>
		</select>
	</header>

	<div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
		{#each users as u (u.id)}
			<article class="rounded-lg border bg-white p-4 shadow transition hover:shadow-md">
				<a href={u.avatar_url} target="_blank" rel="noopener external">
					<!-- svelte-ignore a11y_missing_attribute -->
					<img
						src={u.avatar_url}
						class="mb-3 h-28 w-full rounded object-cover"
						loading="lazy"
						on:error={avatarFallback}
					/>
				</a>

				<h2 class="text-lg font-medium">{u.username ?? '—'}</h2>

				<div class="mt-2 space-y-1 text-sm text-gray-600">
					<div class="flex justify-between">
						<span>id</span>
						<span>{u.id}</span>
					</div>
					<div class="flex justify-between">
						<span>discord_id</span>
						<span>{u.discord_id}</span>
					</div>
				</div>
			</article>
		{/each}
	</div>

	{#if users.length === 0}
		<p class="mt-6 text-gray-600">no users</p>
	{/if}

	<nav class="mt-6 flex items-center justify-between">
		<span class="text-sm text-gray-600">
			{(page - 1) * limit + 1}–{Math.min(page * limit, total)} of {total}
		</span>

		<div class="flex gap-1">
			<button
				class="rounded border px-3 py-1 disabled:opacity-50"
				disabled={page === 1}
				on:click={() => gotoPage(page - 1)}
			>
				←
			</button>

			<!-- eslint-disable-next-line no-undef -->
			{#each pages as p (p)}
				<button
					class="rounded border px-3 py-1"
					class:bg-red-600={p === page}
					class:text-white={p === page}
					on:click={() => gotoPage(p)}
				>
					{p}
				</button>
			{/each}

			<button
				class="rounded border px-3 py-1 disabled:opacity-50"
				disabled={page === totalPages}
				on:click={() => gotoPage(page + 1)}
			>
				→
			</button>
		</div>
	</nav>
</main>
