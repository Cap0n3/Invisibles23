const { src, dest, watch, series } = require('gulp')
const gulp = require('gulp');
const sass = require('gulp-sass')(require('sass'));

function buildStyles() {
  return src('./src/sass/**/*.scss')
    .pipe(sass())
    .pipe(dest('./website/static/website/css'))
}

function watchTask() {
  watch(['./src/sass/**/*.scss'], buildStyles)
}

exports.default = series(buildStyles, watchTask)