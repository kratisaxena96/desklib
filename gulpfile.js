/* File: gulpfile.js */

// grab our packages
var gulp   = require('gulp'),
    jshint = require('gulp-jshint'),
	sass   = require('gulp-sass'),
	sourcemaps = require('gulp-sourcemaps'),
	concat   = require('gulp-concat'),
	gutil = require('gulp-util'),
	uglify = require('gulp-uglify'),
	browserSync = require('browser-sync').create(),
	reload = browserSync.reload,
	cleanCSS = require('gulp-clean-css');

// define the default task and add the watch task to it
gulp.task('default', ['watch']);

gulp.task('build-css', () => {
  return gulp.src(['desklib/static/src/scss/**/*.scss','!node_modules/**/*.scss'])
    .pipe(sourcemaps.init())  // Process the original sources
    .pipe(sass())
    .pipe(sourcemaps.write()) // Add the map to modified source.
    .pipe(gulp.dest('desklib/static/src/css'))
});

gulp.task('minify-css', ['build-css'], () => {
  return gulp.src('desklib/static/src/css/**/*.css')
    .pipe(sourcemaps.init())
    .pipe(concat('bundle.css'))
    .pipe(cleanCSS())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest('desklib/static/dist/css'));
});

gulp.task('reload-css', function() {
  return gulp.src('desklib/static/desklib/css/**/*.css')
  // .pipe(sourcemaps.init())  // Process the original sources
    .pipe(browserSync.reload({stream: true}));
});

// configure the jshint task
gulp.task('jshint', function() {
  return gulp.src(['desklib/static/src/js/custom.js'])
    .pipe(jshint())
    .pipe(jshint.reporter('jshint-stylish'));
});

 gulp.task('build-js', function() {
   return gulp.src(['desklib/static/src/js/jquery.js','desklib/static/src/js/bootstrap.js','desklib/static/src/js/popper.min.js','desklib/static/src/js/custom.js'])
     .pipe(sourcemaps.init())
       .pipe(concat('bundle.js'))
       .pipe(uglify())
     .pipe(sourcemaps.write())
     .pipe(gulp.dest('desklib/static/dist/js'))
     .pipe(browserSync.reload({stream: true}));
 });

// configure which files to watch and what tasks to use on file changes
gulp.task('watch', function() {
  gulp.watch('desklib/static/src/js/**/*.js', ['jshint']);
  // gulp.watch('scss/**/*.scss', ['build-css']);
  // gulp.watch('javascript/**/*.js', ['build-js']);
});

gulp.task('copy-css', function(){
  gulp.src('bower_components/bootstrap/dist/css/bootstrap.css').pipe(gulp.dest('desklib/static/src/css/'));
});

gulp.task('copy-js', function(){
  gulp.src('bower_components/jquery/dist/jquery.js').pipe(gulp.dest('desklib/static/src/js/'));
  gulp.src('bower_components/bootstrap/dist/js/bootstrap.js').pipe(gulp.dest('desklib/static/src/js/'));
});

// Static Server + watching scss/html files
gulp.task('serve', ['copy-css', 'copy-js', 'minify-css', 'build-js'], function() {

    browserSync.init({
      	injectChanges: true,
        files: ['desklib/static/dist/css/**/*.css', 'desklib/static/dist/js/*.js'],
        // server: "./",
        proxy: "localhost:8004",
        logConnections: true,
        // tunnel: true,
        // xip: true,
    });

    gulp.watch('desklib/static/src/js/**/*.js', ['jshint', 'build-js']);
    gulp.watch('./**/*.scss', ['minify-css']);
    // gulp.watch('desklib/static/desklib/css/**/*.css', browserSync.reload({stream: true}));
    // gulp.watch("desklib/static/desklib/css/**/*.css").on('change', browserSync.reload),
    gulp.watch("./**/*.html").on('change', browserSync.reload);
});



