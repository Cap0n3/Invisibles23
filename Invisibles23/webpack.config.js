const NodePolyfillPlugin = require('node-polyfill-webpack-plugin');
const Dotenv = require('dotenv-webpack');

module.exports = {
    mode: 'development',
    watch: true, // To watch for changes in main.js
    entry: './src/js/main.js',
    output: {
        filename: 'bundle.js',
        path: __dirname + '/website/static/website/js/dist',
    },
    plugins: [
		new NodePolyfillPlugin(),
        // see https://www.npmjs.com/package/dotenv-webpack
        new Dotenv({
            path: './.env', // To make sure that the .env file is used
            ignoreStub: true // To avoid issues with the dotenv-webpack (process.env not defined)
        }),
	],
    resolve: {
        fallback: {
            // To partially fix Polyfill issue with Node.js core modules
            "fs": false,
        } 
    },
};