jQuery(document).ready(function (){


    function ajaprod(query){
        var data = {};
        data.query = query
        data.subject = 'productlistbyname'
        $.ajax({
            type: "GET",
            url: "/trading/ajax",
            data: data,
            cache: false,
            success: function(data){
                    if (data.len || data.len == 0){
                        $('#itemname').html("");
                    if(data.len == 0){
                        $('#itemname').append('Не найдено по запросу.');
                    }else{
                        $.each(data.items, function(k, v){
                            $('#itemname').append('<p><a class = "add_to_basket" href="" data-product-id="'+v.id+'" data-user-id="'+v.userid+'" data-amount="1">[+]</a> <a href="view?object=product&id='+v.id+'">'+v.name+'</a></p>');
                        });
                    }                    
                    }

            },
            error: function(){
                console.log("error")
            }
        });
        console.log('got to func');
    };

    
$(document).on('keyup', '.m2m', function(e){
    e.preventDefault();
    var query = $(this).val();
    ajaprod(query)
    
});
});

