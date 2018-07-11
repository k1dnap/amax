jQuery(document).ready(function () {

    function trading_refresh_basket(productid, userid, amount, type){
        var data = {};
        data.type = type;
        data.product_id = productid;
        data.amount = amount;
        data.user_id = userid;
        $.ajax({
            type: "GET",
            url: "/trading/basket",
            data: data,
            cache: false,
            success: function (data) {
                if (data.products_in_basket_count || data.products_in_basket_count == 0){
                   $('#products_in_basket_count').text("("+data.products_in_basket_count+")");
                    $('#basket-list').html("");
                    if (data.products_in_basket_count == 0) {
                        $('#basket-list').append('<li><span>Товары отсутствуют</span></li>');    
                    }else{
                    $('#basket-list').append('<li><span><a id="clearbasket" data-user-id="'+ userid+'" data-amount="1">Очистить товары  </a></span></li><br/>');
                    }
                    $.each(data.products, function(k, v){
                       $('#basket-list').append('<li><span>'+ '<a class="delete-item" data-product-id="'+v.id +'" data-user-id="'+v.userid+  '" data-amount="1"'  +'>[-]</a>'+ v.name+' ' + v.value + 'шт. '+'</span></li>');
                    });
                    $('#basket-list').append('<li><span><a data-toggle="modal" data-target="#formoperation">Сформировать</a></span></li>');
                }

            },
            error: function(){
                console.log("error")
            }
       });
    };

    $(document).on('click', '.add_to_basket', function(e){
        e.preventDefault();
        var productid;
        var userid;
        var amount;
        var type;
        productid = $(this).attr("data-product-id");
        userid = $(this).attr("data-user-id");
        amount= $(this).attr("data-amount");
        type = 'add'
        trading_refresh_basket(productid, userid, amount, type)
    });
        
    $(document).on('click', '.delete-item', function(e){
        e.preventDefault();
        var productid;
        var userid;
        var amount;
        var type;
        productid = $(this).attr("data-product-id");
        userid = $(this).attr("data-user-id");
        amount= $(this).attr("data-amount");
        type = 'delete'
        trading_refresh_basket(productid, userid, amount, type)
    });
    $(document).on('click', '#clearbasket', function(e){
        e.preventDefault();
        var productid;
        var userid;
        var amount;
        var type;
        productid = $(this).attr("data-product-id");
        userid = $(this).attr("data-user-id");
        amount= $(this).attr("data-amount");
        type = 'clear'
        trading_refresh_basket(productid, userid, amount, type)
    });
});