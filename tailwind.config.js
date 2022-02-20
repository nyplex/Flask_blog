module.exports = {
  content: ["./flask_blog/templates/**/*.{html,js}", "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {
      fontFamily: {
        IBM: ["IBM Plex Sans", "sans-serif"],
      },
      colors: {
        darkBg: "#111827",
      }
    },
    screens: {
      "mobile": "450px",
      "sm": "640px",
      "md": "768px",
      "lg": "1024px",
      "xl": "1280px",
      "2xl": "1536px",
    }
  },
  plugins: [
    require('flowbite/plugin')
  ],
  darkMode: 'class',
}
