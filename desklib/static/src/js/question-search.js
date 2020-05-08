// $(document).ready(function(){
//        var results = new Bloodhound({
//            datumTokenizer: Bloodhound.tokenizers.obj.whitespace('question'),
//            queryTokenizer: Bloodhound.tokenizers.whitespace,
//            remote: {
//                url: '/homework-help/autocomplete/?q=%QUERY',
//                 wildcard: '{query}'
//            }
//        });
//        results.initialize();
//
//        $('#question .typeahead').typeahead({
//            hint: true,
//            highlight: true,
//            minLength: 2,
//            maxItem: 5,
//          },
//          {
//            name: 'question',
//            displayKey: 'question',
//            source: results.ttAdapter(),
//            templates: {
//                empty: function(){
//                    return [
//                        '<div class="empty-message">',
//                            'No results found',
//                        '</div>'].join('\n')
//                },
//                suggestion: function(question){
//                    var string = '<a class="tt-suggestion-link" href="/homework-help/question/'+ question.slug +'">'+ question.question +'</a>'
//                    return string;
//                }
//            }
//           }
//        );
//    });