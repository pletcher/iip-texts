import { json } from '@sveltejs/kit';
import { PUBLIC_API_URL } from '$env/static/public'

export async function GET() {
    const response = await fetch(`${PUBLIC_API_URL}/inscriptions`);
    const inscriptions = await response.json();

    return json(inscriptions);
}