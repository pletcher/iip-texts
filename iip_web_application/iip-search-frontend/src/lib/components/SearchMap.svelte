<script lang="ts">
	import type { Inscription } from '$lib/types/inscription.type';
	import type { MapLayerMouseEvent } from 'mapbox-gl';

	import mapboxgl from 'mapbox-gl';
	import { onDestroy, onMount } from 'svelte';
	import MapOverlays from './MapOverlays.svelte';

	const ACCESS_TOKEN =
		'pk.eyJ1IjoiZGs1OCIsImEiOiJjajQ4aHd2MXMwaTE0MndsYzZwaG1sdmszIn0.VFRnx3NR9gUFBKBWNhhdjw';
	const ATTRIBUTION =
		'Map data &copy; <a href="https://openstreetmap.org">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://mapbox.com">Mapbox</a>';
	const MAX_ZOOM = 11;

	mapboxgl.accessToken = ACCESS_TOKEN;

	export let inscriptions: Inscription[] = [];

	let lng: number = 35.3;
	let lat: number = 31.3;
	let map: mapboxgl.Map;
	let mapContainer: HTMLElement;

	function initializeMap() {
		const map = new mapboxgl.Map({
			customAttribution: ATTRIBUTION,
			logoPosition: 'bottom-right',
			container: mapContainer,
			style: 'mapbox://styles/mapbox/satellite-v9',
			center: [lng, lat],
			maxZoom: MAX_ZOOM,
			zoom: 5
		});

		return map;
	}

	function handleUnclusteredClick(e: MapLayerMouseEvent) {
		// @ts-expect-error
		const feature = e.features[0];
		// @ts-expect-error
		const coordinates = feature.geometry.coordinates.slice();

		const properties = feature.properties as Inscription;

		new mapboxgl.Popup()
			.setLngLat(coordinates)
			.setHTML(
				`
					<article class="prose prose-stone prose-sm">
						<h3>${properties.title}</h3>
						<p>
							${properties.description}
						</p>
						<p>
							<a href="/inscriptions/${properties.filename.replace('.xml', '')}">View</a>
						</p>
					</article>
					`
			)
			.addTo(map);
	}

	const SOURCE_NAME = 'inscriptions';

	function addSource(map: mapboxgl.Map, inscriptions: Inscription[]) {
		map.addSource(SOURCE_NAME, {
			type: 'geojson',
			cluster: true,
			clusterMaxZoom: 11,
			clusterRadius: 50,
			// @ts-expect-error
			data: formatData(inscriptions)
		});
	}

	const CLUSTER_LAYER = 'clusters';
	const CLUSTER_COUNT_LAYER = 'cluster-count';
	const UNCLUSTERED_LAYER = 'unclustered-points';

	function addClusterLayers(map: mapboxgl.Map) {
		map.addLayer({
			id: CLUSTER_LAYER,
			type: 'circle',
			source: SOURCE_NAME,
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

		map.addLayer({
			id: CLUSTER_COUNT_LAYER,
			type: 'symbol',
			source: SOURCE_NAME,
			filter: ['has', 'point_count'],
			layout: {
				'text-field': ['get', 'point_count_abbreviated'],
				'text-font': ['Arial Unicode MS Bold'],
				'text-size': 12
			}
		});

		map.addLayer({
			id: UNCLUSTERED_LAYER,
			type: 'circle',
			source: SOURCE_NAME,
			filter: ['!', ['has', 'point_count']],
			paint: {
				'circle-color': '#11b4da',
				'circle-radius': 8,
				'circle-stroke-width': 1,
				'circle-stroke-color': '#fff'
			}
		});

		// When a click event occurs on a feature in
		// the unclustered-point layer, open a popup at
		// the location of the feature, with
		// description HTML from its properties.
		map.on('click', UNCLUSTERED_LAYER, handleUnclusteredClick);

		map.on('mouseenter', CLUSTER_LAYER, () => {
			map.getCanvas().style.cursor = 'pointer';
		});
		map.on('mouseleave', CLUSTER_LAYER, () => {
			map.getCanvas().style.cursor = '';
		});

		map.on('mouseenter', UNCLUSTERED_LAYER, () => {
			map.getCanvas().style.cursor = 'pointer';
		});
		map.on('mouseleave', UNCLUSTERED_LAYER, () => {
			map.getCanvas().style.cursor = '';
		});
	}

	function removeLayers(map: mapboxgl.Map) {
		if (map.getLayer(CLUSTER_LAYER)) {
			map.removeLayer(CLUSTER_LAYER);
		}

		if (map.getLayer(CLUSTER_COUNT_LAYER)) {
			map.removeLayer(CLUSTER_LAYER);
		}

		if (map.getLayer(UNCLUSTERED_LAYER)) {
			map.removeLayer(UNCLUSTERED_LAYER);
		}
	}

	function removeSources(map: mapboxgl.Map) {
		if (map.getSource(SOURCE_NAME)) {
			map.removeSource(SOURCE_NAME);
		}
	}

	function convertToGeoJson(inscriptions: Inscription[]) {
		return inscriptions.filter(hasCoords).map((inscription) => {
			const coordinates = inscription.location_coordinates as number[];
			return {
				type: 'Feature',
				properties: inscription,
				geometry: {
					type: 'Point',
					coordinates: [coordinates[1], coordinates[0]]
				}
			};
		});
	}


	function formatData(inscriptions: Inscription[]) {
		return {
			type: 'FeatureCollection',
			features: convertToGeoJson(inscriptions)
		};
	}

	function hasCoords(inscription: Inscription) {
		return Boolean(inscription.location_coordinates);
	}

	onMount(async () => {
		map = initializeMap();

		map.on('load', () => {
			addSource(map, inscriptions);
			addClusterLayers(map);
			// addOverlays(map);
		});
	});

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});

	$: {
		if (map && map.loaded()) {
			// @ts-expect-error
			map.getSource(SOURCE_NAME).setData(formatData(inscriptions));
		}
	}

	/* borrowed from iip-production/iip_smr_web_app/static/iip_search_app/mapsearch/mapsearch.js
	// OVERLAYS

var roman_provinces;
var roman_roads;
var byzantine_provinces_400CE;
var iip_regions;
var king_herod_boundaries_37BCE;

// ajax call for getting overlay data
$.ajax({
  dataType: "json",
  url: "load_layers",
  success: function (data) {

    var provinces = JSON.parse(data.roman_provinces);
    roman_provinces = new L.geoJSON(provinces, { color: 'olive', weight: 1, onEachFeature: onEachRomanProvince });

    var roads = JSON.parse(data.roman_roads);
    roman_roads = new L.geoJSON(roads, { style: getWeight });

    var byzantine = JSON.parse(data.byzantine_provinces_400CE);
    byzantine_provinces_400CE = new L.geoJSON(byzantine, { color: 'gray', weight: 1, onEachFeature: onEachByzantine });

    var iip = JSON.parse(data.iip_regions);
    iip_regions = new L.geoJSON(iip, { color: 'navy', weight: 1, onEachFeature: onEachIIP });

    var king_herod = JSON.parse(data.king_herod);
    king_herod_boundaries_37BCE = new L.geoJSON(king_herod, { color: 'brown', weight: 1, onEachFeature: onEachKingHerod });
  }
});


// FUNCTION FOR CHANGING ROAD WEIGHTS
var getWeight = function (road) {
  var line_weight;
  var dash_array;
  var color;

  if (road.properties.Major_or_M === "0") {
    line_weight = 1;
  } else {
    line_weight = 2;
  }

  if (road.properties.Known_or_a) {
    dash_array = null;
  } else {
    dash_array = '1 5';
  }

  return { weight: line_weight, dashArray: dash_array, color: 'maroon' }
}
	*/
</script>

<div>
	<div class="fixed bottom-0 right-0 h-full w-full left-96 bg-theme-700 text-white" bind:this={mapContainer} />
	{#if map}
		<MapOverlays map={map} />
	{/if}
</div>
