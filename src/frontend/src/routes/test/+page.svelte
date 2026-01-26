<script>
	export let data;
</script>

<main class="min-h-screen bg-gray-100 p-6">
	<div class="mx-auto max-w-xl rounded-xl bg-white p-6 shadow">
		<h1 class="mb-6 text-center text-5xl font-bold text-red-500 text-shadow-2xs">api test</h1>

		<ul class="space-y-2">
			<li class="rounded border p-3">
				{data.test.message}
			</li>
			<li class="rounded border p-3">
				users count: {data.test.users_count}
			</li>
		</ul>
	</div>
</main>
