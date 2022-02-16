module.exports = {
  content: ["./flask_blog/templates/**/*.{html,js}", "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {
      fontFamily: {
        IBM: ["IBM Plex Sans", "sans-serif"],
      },
      colors: {
        primary: "#1D3557",
      }
    },
    screens: {
      "mobile": "445px",
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
}
