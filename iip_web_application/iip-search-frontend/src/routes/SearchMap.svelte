<script lang="ts">
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	const ACCESS_TOKEN =
		'pk.eyJ1IjoiZGs1OCIsImEiOiJjajQ4aHd2MXMwaTE0MndsYzZwaG1sdmszIn0.VFRnx3NR9gUFBKBWNhhdjw';
	const ATTRIBUTION =
		'Map data &copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://mapbox.com">Mapbox</a>';
	const MAX_ZOOM = 11;
	const TILE_LAYER_ID = 'mapbox.satellite';
	const TILES_URL = `https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=${ACCESS_TOKEN}`;

	async function createMap(container: HTMLElement) {
		const L = await import('leaflet');
		const initialCoordinates = L.latLng(31.3, 35.3);
		const m = L.map(container, { preferCanvas: true }).setView(initialCoordinates, 5);

		L.tileLayer(TILES_URL, {
			attribution: ATTRIBUTION,
			id: TILE_LAYER_ID,
			maxZoom: MAX_ZOOM
		}).addTo(m);

		return m;
	}

	async function mapAction(container: HTMLElement) {
		let destroy = () => {};
		if (browser) {
			const map = await createMap(container);

			return {
				destroy: () => {
					map.remove();
				}
			};
		}

		return { destroy };
	}

	onMount(() => {
		mapAction(document.getElementById('search_map') as HTMLElement);
	});
</script>

<svelte:window />

<link
	rel="stylesheet"
	href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
	integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
	crossorigin=""
/>
<div class="fixed bottom-0 right-0 h-full w-full bg-theme-700 text-white" id="search_map" />
