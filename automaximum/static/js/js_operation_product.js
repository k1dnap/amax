$(document).on('click', '.delline', function() {
    $(this).parent().parent().remove();
});

function cloneMore(selector, type) {
    var newElement = $(selector).clone(true);
    var total = $('#id_' + type + '-TOTAL_FORMS').val();
    console.log(total)
    newElement.find(':input').each(function() {
        var name = $(this).attr('name').replace('-' + (total-1) + '-','-' + total + '-');
        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
    });
    total++;
    $('#id_' + type + '-TOTAL_FORMS').val(total);
    $(selector).parent().append(newElement).append('<input type="hidden" name="form-'+(total-1)+'-id" id="id_form-'+(total-1)+'-id">');
}
$(document).on('click', '.addline', function() {
    cloneMore('#menu0 operas:last', 'form');
});

jQuery(document).ready(function (){    
$(document).on('keyup', '.operation_product_list', function(e){
    e.preventDefault();
    var asd = $(this);
    if ($(this).parent().find('.dropdown-menu').is(":hidden")){
        $(this).dropdown('toggle');
      }
    var kias = $(this).parent().find('ul:last');
    var query = $(this).val();
    
    if (query.length > 2){
        
        var data = {};
        data.query = query
        data.subject = 'operation_product_list'
        $.ajax({
            type: "GET",
            url: "/trading/ajax",
            data: data,
            cache: false,
            success: function(data){
                
                console.log(data.len)
                    if (data.len || data.len == 0){
                        kias.html("");
                    if(data.len == 0){
                        kias.append('<li><span>Не найдено по запросу: '+query+'</span></li>');
                    }else{
                        $.each(data.items, function(k, v){
                            kias.append('<li><a data-id="'+v.id+'" class="selecteditem">'+v.name+'</a></li>');
                        });
                    }                    
                    }

            },
            error: function(){
                console.log("error")
            }
        });
        

        
    }
});
});

$(document).on('click', '.selecteditem', function() {
    var dataid = $(this).attr("data-id");
    var name = $(this).text();
    var workplace1 =$(this).parent().parent().parent().parent();
    workplace1.find('input:last').val(dataid);
    workplace1.find('input:first').val(name);
    var price =  $( "#id_price" ).val();
    if (price != null){
        var data = {};
        data.query = dataid
        data.price = price
        data.subject = 'price_val'
        $.ajax({
            type: "GET",
            url: "/trading/ajax",
            data: data,
            cache: false,
            success: function(data){
                console.log(data.len)
                    if (data.len || data.len == 0){
                    if(data.len == 0){
                    }else{
                        var item1 = workplace1.parent().find( "div" )[2];
                        $(item1).find('input:first').val(data.items[0].name);
                    }                    
                    }

            },
            error: function(){
                console.log("error")
            }
        });
    }
});

$(document).on('change', 'select[name=price]', function() {
    var price =  $( "#id_price" ).val();
    var allListElements = $( "operas" );
    $( "#menu0" ).find( "operas" ).each(
        function(){
            var value_to = $($(this).find("input")[3]);
            var product_id = $(this).find("input")[1];
            console.log(value_to);
            console.log($(product_id).val());
            if ($(product_id).val() != ''){
                var data = {};
                data.query = $(product_id).val()
                data.price = price
                data.subject = 'price_val'
                $.ajax({
                    type: "GET",
                    url: "/trading/ajax",
                    data: data,
                    cache: false,
                    success: function(data){
                        console.log(data.items[0].name)
                            if (data.len || data.len == 0){
                            if(data.len != 0){
                                $(value_to).val(data.items[0].name);
                            }                    
                            }
        
                    },
                    error: function(){
                        console.log("error")
                    }
                });
            }

        }
    );
});