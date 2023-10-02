/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
      "./templates/**/*.html",
      "./templates/**/**/*.html",
      "./static/**/js/*.js"
  ],
  theme: {
    extend: {
        colors: {
            'dashboard-blue': "#4759E4",
            'dashboard-item-active': "#95A1FF",
            'dashboard-gray': "#F8FAFF"
        },
        gridTemplateColumns: {
            'dashboard-template': '300px 1fr'
        }
    },
  },
  plugins: [],
}

