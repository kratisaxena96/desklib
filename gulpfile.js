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
	cleanCSS = require('gulp-clean-css'),
	gulpimagemin = require('gulp-imagemin');

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
  return gulp.src(['desklib/static/src/css/*.css',   '!desklib/static/src/css/coming-soon/coming-soon.css'])
    .pipe(sourcemaps.init())
    .pipe(concat('bundle.css'))
    .pipe(cleanCSS())
//    .pipe(sourcemaps.write())
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
   return gulp.src(['desklib/static/src/js/jquery.js','desklib/static/src/js/popper.min.js','desklib/static/src/js/bootstrap.js','desklib/static/src/js/owl.carousel.min.js','desklib/static/src/js/custom-typeahead.bundle.js','desklib/static/src/js/bloodhound.js','desklib/static/src/js/select2.js','desklib/static/src/js/custom.js','desklib/static/src/js/jquery.fileupload.js','desklib/static/src/js/question-search.js','desklib/static/src/js/typeahead.js'])
  .pipe(sourcemaps.init())
       .pipe(concat('bundle.js'))
       .pipe(uglify())
//     .pipe(sourcemaps.write())
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
  gulp.src('bower_components/owl.carousel/dist/assets/owl.carousel.min.css').pipe(gulp.dest('desklib/static/src/css/'));
  gulp.src('bower_components/owl.carousel/dist/assets/owl.theme.default.min.css').pipe(gulp.dest('desklib/static/src/css/'));
  gulp.src('bower_components/components-font-awesome/css/all.css').pipe(gulp.dest('desklib/static/src/css/'));
  gulp.src('bower_components/select2/dist/css/select2.css').pipe(gulp.dest('desklib/static/src/css/'));
  gulp.src('bower_components/jQuery-File-Upload/css/jquery.fileupload.css').pipe(gulp.dest('desklib/static/src/css/'));
  gulp.src('bower_components/jQuery-File-Upload/css/jquery.fileupload-ui.css').pipe(gulp.dest('desklib/static/src/css/'));
});

gulp.task('copy-font', function(){
    gulp.src('bower_components/components-font-awesome/webfonts/*.*').pipe(gulp.dest('desklib/static/dist/webfonts/'));
});

gulp.task('copy-js', function(){
  gulp.src('bower_components/jquery/dist/jquery.js').pipe(gulp.dest('desklib/static/src/js/'));
  gulp.src('bower_components/bootstrap/dist/js/bootstrap.js').pipe(gulp.dest('desklib/static/src/js/'));
  gulp.src('bower_components/owl.carousel/dist/owl.carousel.min.js').pipe(gulp.dest('desklib/static/src/js/'));
//  gulp.src('bower_components/typeahead.js/dist/typeahead.bundle.js').pipe(gulp.dest('desklib/static/src/js/'));
  gulp.src('bower_components/typeahead.js/dist/bloodhound.js').pipe(gulp.dest('desklib/static/src/js/'));
  gulp.src('bower_components/select2/dist/js/select2.js').pipe(gulp.dest('desklib/static/src/js/'));
  gulp.src('bower_components/jQuery-File-Upload/js/vendor/jquery.ui.widget.js').pipe(gulp.dest('desklib/static/src/js/'));
  gulp.src('bower_components/jQuery-File-Upload/js/jquery.fileupload.js').pipe(gulp.dest('desklib/static/src/js/'));
  gulp.src('bower_components/jQuery-File-Upload/js/jquery.fileupload-image.js').pipe(gulp.dest('desklib/static/src/js/'));
  gulp.src('bower_components/jQuery-File-Upload/js/jquery.fileupload-process.js').pipe(gulp.dest('desklib/static/src/js/'));
  gulp.src('bower_components/jQuery-File-Upload/js/jquery.fileupload-validate.js').pipe(gulp.dest('desklib/static/src/js/'));
}); 

//compress images

gulp.task('minify-image', function () {
	gulp.src('desklib/static/src/assets/images/v2/*')
		.pipe(gulpimagemin([
		    gulpimagemin.gifsicle({interlaced: true}),
		    gulpimagemin.jpegtran({progressive: true}),
		    gulpimagemin.optipng({optimizationLevel: 5}),
		    gulpimagemin.svgo({
		        plugins: [
		            {removeViewBox: true},
		            {cleanupIDs: false}
		        ]
		    })
		]))
		.pipe(gulp.dest('desklib/static/dist/assets/images/v2'))
});


// Static Server + watching scss/html files
gulp.task('serve', ['copy-css', 'copy-font', 'copy-js', 'minify-css', 'build-js', 'minify-image'], function() {

    browserSync.init({
      	injectChanges: true,
        files: ['desklib/static/dist/css/**/*.css', 'desklib/static/dist/js/*.js'],
        // server: "./",
        proxy: "localhost:8000",
//        port: 3001,
        logConnections: true,
        // tunnel: true,
        // xip: true,
    });

    gulp.watch('desklib/static/src/js/**/*.js', ['jshint', 'build-js']);
    gulp.watch('desklib/static/src/scss/**/*.scss', ['minify-css']);
    gulp.watch('desklib/static/src/assets/**', ['minify-image']);
    // gulp.watch('desklib/static/desklib/css/**/*.css', browserSync.reload({stream: true}));
    // gulp.watch("desklib/static/desklib/css/**/*.css").on('change', browserSync.reload),
    gulp.watch("./**/*.html").on('change', browserSync.reload);
});



