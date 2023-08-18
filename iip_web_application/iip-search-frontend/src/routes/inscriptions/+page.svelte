<script>
	import SearchMap from '$lib/components/SearchMap.svelte';

	export let data;

	$: inscriptions = data.inscriptions;
</script>


<main class="py-10 ">
	<div class="px-4 sm:px-6 lg:px-8">
		<SearchMap inscriptions={inscriptions} />
	</div>
</main>
