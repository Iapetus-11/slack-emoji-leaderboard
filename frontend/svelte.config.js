import adapterNode from '@sveltejs/adapter-node';
import preprocess from 'svelte-preprocess';

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapterNode(),
  },
  preprocess: [
    preprocess({
      postcss: true,
    }),
  ],
};

export default config;
