module.exports = {
    mode: 'development',
    watch: true, // To watch for changes in main.js
    entry: './src/js/main.js',
    output: {
        filename: 'bundle.js',
        path: __dirname + '/website/static/website/js/dist',},
};