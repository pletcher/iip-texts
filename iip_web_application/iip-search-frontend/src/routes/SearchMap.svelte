<script lang="ts">
	import type { Inscription } from '$lib/types/inscription.type';

	// @ts-expect-error
	import mapboxgl from 'mapbox-gl';
	import { onMount } from 'svelte';

	// importing the CSS breaks the map display
	// import 'mapbox-gl/dist/mapbox-gl.css';

	const ACCESS_TOKEN =
		'pk.eyJ1IjoiZGs1OCIsImEiOiJjajQ4aHd2MXMwaTE0MndsYzZwaG1sdmszIn0.VFRnx3NR9gUFBKBWNhhdjw';
	const ATTRIBUTION =
		'Map data &copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://mapbox.com">Mapbox</a>';
	const MAX_ZOOM = 11;

	mapboxgl.accessToken = ACCESS_TOKEN;

	function initializeMap() {
		const map = new mapboxgl.Map({
			container: 'search_map', // container ID
			style: 'mapbox://styles/mapbox/satellite-v9', // style URL
			center: [35.3, 31.3], // starting position [lng, lat]
			zoom: 5 // starting zoom
		});

		return map;
	}

	function convertToGeoJson(inscriptions: Inscription[]) {
		return inscriptions.map((inscription) => {
			const coordinates = inscription.location_coordinates as number[]
			return {
				type: 'Feature',
				properties: {},
				geometry: {
					type: 'Point',
					coordinates: [coordinates[1], coordinates[0]],
				}
			};
		});
	}

	onMount(async () => {
		const map = initializeMap();

		const response = await fetch('/inscriptions');
		const inscriptions = await response.json();

		const withCoords = inscriptions.filter((inscription: Inscription) =>
			Boolean(inscription.location_coordinates)
		);

		map.addSource('inscription_locations', {
			type: 'geojson',
			cluster: true,
			clusterMaxZoom: 11,
			clusterRadius: 50,
			data: {
				type: 'FeatureCollection',
				features: convertToGeoJson(withCoords)
			}
		});

		map.addLayer({
			id: 'clusters',
			type: 'circle',
			source: 'inscription_locations',
			filter: ['has', 'point_count'],
			paint: {
				// Use step expressions (https://docs.mapbox.com/mapbox-gl-js/style-spec/#expressions-step)
				// with three steps to implement three types of circles:
				//   * Blue, 20px circles when point count is less than 100
				//   * Yellow, 30px circles when point count is between 100 and 750
				//   * Pink, 40px circles when point count is greater than or equal to 750
				'circle-color': ['step', ['get', 'point_count'], '#51bbd6', 100, '#f1f075', 750, '#f28cb1'],
				'circle-radius': ['step', ['get', 'point_count'], 20, 100, 30, 750, 40]
			}
		});
	});
</script>

<div class="fixed bottom-0 right-0 h-full w-full bg-theme-700 text-white" id="search_map" />
