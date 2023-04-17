export async function load({ url }) {
  return {
    limit: parseInt(url.searchParams.get('limit')) || 24,
    unique: (url.searchParams.get('unique') || '').toLowerCase() !== 'false',
  };
}
