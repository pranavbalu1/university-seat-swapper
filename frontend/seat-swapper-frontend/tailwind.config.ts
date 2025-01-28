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
        background: '#f2f2f2',
        button:'#81f3ff',
        buttonHover: '#3B7FBC',
        navbar: '#202121',

      },
      backgroundImage: {
        'stacked-waves': "url('/stacked_waves.svg')",
        'stacked-waves-2': "url('/stacked-waves-1.svg')",
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
