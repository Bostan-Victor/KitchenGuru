/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      backgroundColor: {
        '33B249': 'rgba(51, 178, 73, 1)',
        'A5D0A8': 'rgba(165, 208, 168, 0.5)',
        'ECF0F1': 'rgba(236, 240, 241, 1)',
        
      },
      fontFamily: {
        'main-font': ['Rhodium Libre', 'serif'], 
      },
      borderRadius: {
        'custom1': '40px',
      },
    },
  },
  plugins: [],
}
