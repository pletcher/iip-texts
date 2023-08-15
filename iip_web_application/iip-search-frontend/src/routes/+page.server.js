import { PUBLIC_API_URL } from '$env/static/public'

export async function load() {
    const response = await fetch(`${PUBLIC_API_URL}/facets`);
    const facets = await response.json();


    /*
        cities: list[City]
        genres: list[IIPGenre]
        materials: list[IIPMaterial]
        physical_types: list[IIPForm]
        provenances: list[Provenance]
        regions: list[Region]
        religions: list[IIPReligion]
    */
    return facets;
}