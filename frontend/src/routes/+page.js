export async function load({ url }) {
  return {
    limit: parseInt(url.searchParams.get('limit')) || 10,
    unique: (url.searchParams.get('unique') || '').toLowerCase() === 'true',
  };
}
