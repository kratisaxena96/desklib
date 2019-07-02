/* File: gulpfile.js */

// grab our packages
var gulp   = require('gulp'),
  jshint = require('gulp-jshint');
	sass   = require('gulp-sass');
	sourcemaps = require('gulp-sourcemaps');
	concat   = require('gulp-concat');
	gutil = require('gulp-util');
	uglify = require('gulp-uglify');
	browserSync = require('browser-sync').create();
	reload = browserSync.reload;

// define the default task and add the watch task to it
gulp.task('default', ['watch']);

gulp.task('build-css', () => {
  return gulp.src(['./**/*.scss','!node_modules/**/*.scss'])
    .pipe(sourcemaps.init())  // Process the original sources
    .pipe(sass())
    .pipe(sourcemaps.write()) // Add the map to modified source.
    .pipe(gulp.dest('static'))
});

gulp.task('reload-css', function() {
  return gulp.src('desklib/static/desklib/css/**/*.css')
  // .pipe(sourcemaps.init())  // Process the original sources
    .pipe(browserSync.reload({stream: true}));
});

// configure the jshint task
gulp.task('jshint', function() {
  return gulp.src('desklib/static/desklib/js/**/*.js')
    .pipe(jshint())
    .pipe(jshint.reporter('jshint-stylish'));
});

 gulp.task('build-js', function() {
   return gulp.src('javascript/**/*.js')
     .pipe(sourcemaps.init())
       .pipe(concat('bundle.js'))
       .pipe(uglify())
     .pipe(sourcemaps.write())
     .pipe(gulp.dest('static/desklib/js'))
     .pipe(browserSync.reload({stream: true}));
 });

// configure which files to watch and what tasks to use on file changes
gulp.task('watch', function() {
  gulp.watch('desklib/static/desklib/js/**/*.js', ['jshint']);
  // gulp.watch('scss/**/*.scss', ['build-css']);
  // gulp.watch('javascript/**/*.js', ['build-js']);
});

gulp.task('copy', function(){
  gulp.src('desklib/static/desklib/css/**/*.css').pipe(gulp.dest('static/desklib/css/**/*.css'));
  gulp.src('desklib/static/desklib/js/**/*.js').pipe(gulp.dest('static/desklib/js/**/*.js'));
});

// Static Server + watching scss/html files
gulp.task('serve', function() {

    browserSync.init({
      	injectChanges: true,
        files: ['desklib/static/desklib/css/**/*.css', 'desklib/static/desklib/js/*.js'],
        // server: "./",
        proxy: "localhost:8004",
        logConnections: true,
        // tunnel: true,
        // xip: true,
    });

    // gulp.watch('desklib/static/desklib/js/**/*.js', ['jshint']);
    gulp.watch('./**/*.scss', ['build-css']);
    // gulp.watch('desklib/static/desklib/css/**/*.css', browserSync.reload({stream: true}));
    // gulp.watch("desklib/static/desklib/css/**/*.css").on('change', browserSync.reload),
    gulp.watch("./**/*.html").on('change', browserSync.reload);
});



