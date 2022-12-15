/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  theme: {
    extend: {
      keyframes: {
        fadeIntro: {
          '0%': {
            opacity: '0.05',
            transform: 'scale(.9)',
          },
          '100%': {
            opacity: '1',
            transform: 'scale(1)',
          },
        },
      },
      animation: {
        fin: 'fadeIntro ease 0.5s',
      },
    },
  },
  plugins: [],
};
