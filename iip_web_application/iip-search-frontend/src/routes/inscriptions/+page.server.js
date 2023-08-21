import { PUBLIC_API_URL } from '$env/static/public'

export async function load({ url }) {
    const inscriptionResponse = await fetch(`${PUBLIC_API_URL}/inscriptions${url.search}`);
    const json = await inscriptionResponse.json();
    const { items: inscriptions, page, pages } = json;

    return { inscriptions, page, pages };
}