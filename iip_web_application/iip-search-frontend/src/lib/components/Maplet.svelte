<script lang="ts">
	import type { Inscription } from '$lib/types/inscription.type';
	import type { LngLatLike, MapLayerMouseEvent } from 'mapbox-gl';

	import { PUBLIC_MAPBOX_ACCESS_TOKEN } from '$env/static/public';
	import mapboxgl from 'mapbox-gl';
	import { onDestroy, onMount } from 'svelte';

	const ATTRIBUTION =
		'Map data &copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://mapbox.com">Mapbox</a>';

	mapboxgl.accessToken = PUBLIC_MAPBOX_ACCESS_TOKEN;

	export let inscription: Inscription;

	let map: mapboxgl.Map;
	let mapContainer: HTMLElement;

	function initializeMap() {
		const map = new mapboxgl.Map({
			customAttribution: ATTRIBUTION,
			logoPosition: 'bottom-right',
			container: mapContainer,
			style: 'mapbox://styles/mapbox/satellite-v9',
			center: inscription.location_coordinates as LngLatLike,
			zoom: 5
		});

		return map;
	}

    onMount(async () => {
		map = initializeMap();

		map.on('load', () => {
			addSource(map, inscriptions);
			addClusterLayers(map);
		});
	});

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});
</script>
