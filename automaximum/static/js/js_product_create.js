$(document).on('click', '.delline', function() {
    $(this).parent().remove();
});

$(document).on('click', '.addline', function() {
    var newElement = $(this).parent().clone(true);
    var type = newElement.attr("objtype");
    console.log(type)
    newElement.find('input').each(function(){
        var newFor = $(this).attr('name').replace(type+'zx',type);
        $(this).attr('name', newFor);
    });
    newElement.find('a').each(function() {
        var newFor = $(this).attr('class').replace('addline','delline');
        $(this).attr('class', newFor);
        var ars = $(this).text().replace('[+]', '[-]');
        $(this).text(ars);
    });
    $('#'+type+'_listm2m').after(newElement);
});


jQuery(document).ready(function (){


    function m2m(query, type, categoryid, prodid){
        var data = {};
        data.type = type
        if (data.type == 'analogue'){
            data.categoryid = categoryid
            data.prodid = prodid
        }
        console.log(data.type)
        data.query = query
        data.subject = 'productf'
        $.ajax({
            type: "GET",
            url: "/trading/ajax",
            data: data,
            cache: false,
            success: function(data){
                    if (data.len || data.len == 0){
                        $('#'+data.type+'m2m').html("");
                    if(data.len == 0){
                        $('#'+data.type+'m2m').append('<li><span>Не найдено.</span></li>');
                    }else{
                        $.each(data.items, function(k, v){
                            $('#'+data.type+'m2m').append('<p objtype="'+data.type+'"><a class="addline">[+]</a><input type="hidden" name="'+data.type+'zx" value="'+v.id+'">'+v.name+'</p>');
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
    var type = $(this).attr("data-type");
    if (type == 'analogue'){
        var categoryid = $(this).attr("data-categoryid");
        var prodid = $(this).attr("data-prodid");
    }
    m2m(query, type, categoryid, prodid)
    
});
});

