//
// var search = new Bloodhound({
//  datumTokenizer: Bloodhound.tokenizers.obj.whitespace('title'),
//  queryTokenizer: Bloodhound.tokenizers.whitespace,
//  // `states` is an array of state names defined in "The Basics"
////  prefetch: '/study/autocomplete/?q=ass',
//
//  question: {
//    url: '/homework-help/autocomplete/?q=%QUERY',
//    wildcard: '%QUERY'
//  }
//});
//
//$('#question .typeahead').typeahead(null,{
//
//  name: 'search',
//  display: 'title',
//  source: search,
//  templates: {
//    empty: [
//      '<div class="empty-message">',
//        'No results found',
//      '</div>'
//    ].join('\n'),
//		suggestion: Handlebars.compile('<a href="/homework-help/question/{{slug}}">{{title}}</a>')
//  }
//});
