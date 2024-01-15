/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './public/**/*.html',
    './src/**/*.{js,jsx,ts,tsx,vue}',
    'node_modules/flowbite-vue/**/*.{js,jsx,ts,tsx,vue}',
    'node_modules/flowbite/**/*.{js,jsx,ts,tsx}'
  ],
  darkMode: 'class',
  theme: {
    extend: {
      gridTemplateColumns: {
        'mine': 'repeat(auto-fit, minmax(100px, 1fr))'
      }
    },
  },
  plugins: [
    require('flowbite/plugin')
  ],
}