export async function load({ url }) {
  return { limit: parseInt(url.searchParams.get('limit')) || 10 };
}
