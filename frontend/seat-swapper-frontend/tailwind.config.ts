// tailwind.config.ts
import containerQueries from '@tailwindcss/container-queries';
import forms from '@tailwindcss/forms';
import typography from '@tailwindcss/typography';
import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{html,js,svelte,ts}'],
  
  theme: {
    extend: {
      fontFamily: {
        title: ['Belanosima', 'sans-serif'],
        body: ['Open Sans', 'sans-serif'],
        other: ['Quicksand', 'sans-serif'],
      },
      colors: {
        primary: '#4C9AFF',
        secondary: '#2F4F6F',
        background: '#F1F5F9',
        buttonHover: '#3B7FBC',
        navbar: '#2F4F6F',  // Add this new color for navbar
      },
    },
  },

  plugins: [typography, forms, containerQueries],
} satisfies Config;
