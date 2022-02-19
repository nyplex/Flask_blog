module.exports = {
  plugins: {
    'postcss-preset-env': {
      browsers: 'last 7 versions',
      stage: 0,
    },
    //'cssnano': {}, //uncomment on production
    tailwindcss: {},
    autoprefixer: {},
  },
};