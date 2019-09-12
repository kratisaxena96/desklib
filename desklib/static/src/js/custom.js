$( document ).ready(function() {
   $(function(){
        var stocks = new Bloodhound({
            datumTokenizer: function (datum) {
                return Bloodhound.tokenizers.whitespace(datum.tokens);
            },
            queryTokenizer: Bloodhound.tokenizers.whitespace,
            limit: 5,
            remote: {
                url: "/study/autocomplete/",
                replace: function(url, query) {
                    return url + "?q=" + query;
                },
                filter: function(stocks) {
                    return stocks;
                }
            }
        });
        stocks.initialize();
        $('#remote .typeahead').typeahead({
                hint: true,
                highlight: true,
                minLength: 2,
            },
             {
                name: 'stocks',
                displayKey: 'name',
                async: true,
                minLength: 3, // send AJAX request only after user type in at least X characters
                source: stocks.ttAdapter(),
                templates: {
                    empty: [
                          '<div class="empty-message">',
                            'unable to find any Best Document winners that match the current query',
                          '</div>'
                        ].join('\n'),
                          suggestion: function(data){
//                      var str = '<ul>';
                    	$(data).each(function(index,value){
                    		$(value.slug).each(function(ind,val){
                    			var url = "/document/"+value.slug[ind];
                    			str += '<li><a href="' + url + '">' + value.results[ind] + '</a></li>';
//<!--    							console.log(value.results[ind]+"::::"+value.slug[ind]+">>>>>>>>"+ind);-->
                                $(".tt-menu").append('<li><a href="' + url + '">' + value.results[ind] + '</a></li>');
							});
						});
//						str += '</ul>';
//<!--                    suggestion: function(data){-->
//<!--                      var str = '<ul class="list-group">'-->
//<!--                    	$(data).each(function(index,value){-->
//<!--                    		$(value.slug).each(function(ind,val){-->
//<!--                    			var url = "/document/"+value.slug[ind]-->
//<!--                    			str += '<li  class="list-group-item"><img src="' + value.cover_image[ind] + '" width="20%" height="20%"	 class="float-right""/><a href="' + url + '">' + value.results[ind] + '</a></li>'-->
//<!--&lt;!&ndash;    							console.log(value.results[ind]+"::::"+value.slug[ind]+">>>>>>>>"+ind);&ndash;&gt;-->
//<!--							});-->
//<!--						});-->
//<!--						str += '</ul>'-->
//                        return  str ;
                    }
                }
        });
        });
});
