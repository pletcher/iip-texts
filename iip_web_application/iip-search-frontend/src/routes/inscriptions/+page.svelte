<script lang="ts">
	import SearchMap from '$lib/components/SearchMap.svelte';
	import TableResults from '$lib/components/TableResults.svelte';

	export let data;

	let showMapView = false;

	function toggleMapView(_e: Event) {
		showMapView = !showMapView;
	}

	$: inscriptions = data.inscriptions;
</script>

<main class="py-10">
	<div class="px-4 sm:px-6 lg:px-8">
		<div
			class="absolute top-28 right-4 bg-opacity-60 opacity-95 bg-stone-700 p-4 rounded-md z-50 flex"
		>
			<p class="block left-0 relative text-sm text-white mr-2">List</p>
			<button
				type="button"
				class={`${
					showMapView ? 'bg-stone-500' : 'bg-stone-200'
				} relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-md border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-stone-600`}
				role="switch"
				aria-checked={showMapView}
				on:click={toggleMapView}
			>
				<span class="sr-only">Map or List</span>
				<!-- showMapView: "translate-x-5", !showMapView: "translate-x-0" -->
				<span
					class={`${
						showMapView ? 'translate-x-5' : 'translate-x-0'
					} pointer-events-none relative inline-block h-5 w-5 transform rounded-md  shadow ring-0 transition duration-200 ease-in-out`}
				>
					<!-- showMapView: "opacity-0 duration-100 ease-out", !showMapView: "opacity-100 duration-200 ease-in" -->
					<span
						class={`${
							showMapView ? 'opacity-0 duration-100 ease-out' : 'opacity-100 duration-200 ease-in'
						} absolute inset-0 flex h-full w-full items-center justify-center transition-opacity p-1`}
						aria-hidden="true"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="w-6 h-6"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M3.75 12h16.5m-16.5 3.75h16.5M3.75 19.5h16.5M5.625 4.5h12.75a1.875 1.875 0 010 3.75H5.625a1.875 1.875 0 010-3.75z"
							/>
						</svg>
					</span>
					<!-- showMapView: "opacity-100 duration-200 ease-in", !showMapView: "opacity-0 duration-100 ease-out" -->
					<span
						class={`${
							showMapView
								? 'opacity-100 duration-200 ease-in bg-stone-700 text-white rounded-md'
								: 'opacity-0 duration-100 ease-out'
						} absolute inset-0 flex h-full w-full items-center justify-center transition-opacity p-1`}
						aria-hidden="true"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="1.5"
							stroke="currentColor"
							class="w-6 h-6"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M9 6.75V15m6-6v8.25m.503 3.498l4.875-2.437c.381-.19.622-.58.622-1.006V4.82c0-.836-.88-1.38-1.628-1.006l-3.869 1.934c-.317.159-.69.159-1.006 0L9.503 3.252a1.125 1.125 0 00-1.006 0L3.622 5.689C3.24 5.88 3 6.27 3 6.695V19.18c0 .836.88 1.38 1.628 1.006l3.869-1.934c.317-.159.69-.159 1.006 0l4.994 2.497c.317.158.69.158 1.006 0z"
							/>
						</svg>
					</span>
				</span>
			</button>
			<p class="block right-0 relative text-sm text-white ml-2">Map</p>
		</div>
		{#if showMapView}
			<SearchMap {inscriptions} />
		{:else}
			<TableResults {inscriptions} currentPage={data.page} totalPages={data.pages} />
		{/if}
	</div>
</main>
