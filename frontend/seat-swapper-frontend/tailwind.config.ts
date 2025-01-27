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
        primary: '#232323',
        secondary: '#bbbbba',
        background: '#FFFFFF',
        button:'#81f3ff',
        buttonHover: '#3B7FBC',
        navbar: '#202121',  // Add this new color for navbar
      },
    },
  },

  

  plugins: [typography, forms, containerQueries,
    function ({ addUtilities }) {
      addUtilities({
        '.no-scrollbar': {
          /* Hide scrollbar for modern browsers */
          '-ms-overflow-style': 'none', // Internet Explorer 10+
          'scrollbar-width': 'none', // Firefox
        },
        '.no-scrollbar::-webkit-scrollbar': {
          display: 'none', // Safari and Chrome
        },
      });
    },
  ],

} satisfies Config;
