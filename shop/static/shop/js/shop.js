


$(document).ready(function(){
    console.log("jquery loaded")
    const csrf_token = $("[name=csrfmiddlewaretoken]").val();
    const cartQuantityContainer = $("#cartQuantityContainer");
    const overlay = $("#overlay");
    const cartContainer = $("#sideCart");
    const cartBody = cartContainer.find(".cartBody");
    const cartTotalContainer = $("#cartTotal");
    const cartItem_template = $("#cartItem_template");


    function showCart(){
        showOverlay();
        cartContainer.addClass("active")
    }

    function removeCart(){
        hideOverlay();
        cartContainer.removeClass("active")
    }

    function showOverlay(){
        $("body").addClass("overflow-hidden");
        overlay.show();
    }

    function hideOverlay() {
        $("body").removeClass("overflow-hidden");
        overlay.hide();
    }


    function addCartItem(response){
        let newCartItem = cartItem_template.clone();
        newCartItem.removeAttr('id');
        newCartItem.attr("data-item", response.product_id);
        newCartItem.find(".cartItem_thumbnail").attr("src", response.product_thumbnail);
        newCartItem.find(".cartItem_title").text(response.product_title);
        newCartItem.find(".cartItem_quantityText").text(response.quantity);
        newCartItem.find(".cartItem_price").text(response.price);
        newCartItem.find(".cartItem_quantityInput").val(response.quantity);
        cartBody.append(newCartItem);
        newCartItem.show();
    }


    function removeCartItem(id){
        let el = cartBody.find(`.cartItem[data-item='${id}']`).remove();
    }
    function updateCartTotals(response){
        cartQuantityContainer.text(response.productCount);
        cartTotalContainer.text(response.total_price);

    }


    function updateCartItem(cartItem_el, quantity){
        cartItem_el.find(".cartItem_quantityText").text(quantity);
        cartItem_el.find(".cartItem_quantityInput").val(quantity);
    }

    $(document).on("click", ".addToCartBtn", function(){
        let button = $(this);
        let product = parseInt(button.data("product-id"));
        let quantity_input = button.siblings(".quantityContainer").find(".quantityInput");
        let quantity = parseInt(quantity_input.val())

        $.ajax({
            method: "POST",
            url: '/api/v1/cart/add-to-cart/',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrf_token,
            },
            data: JSON.stringify({
                'product': product,
                'quantity': quantity,
            }),
            success: function(response){
                addCartItem(response.cartItem);
                updateCartTotals(response.cart)
                showCart();
            }
        })
    });


    $(document).on("click", ".removeCartItemBtn", function(){
        let button = $(this);
        let product = parseInt(button.closest(".cartItem").attr("data-item"))

        $.ajax({
            method: "POST",
            url: '/api/v1/cart/remove-from-cart/',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrf_token,
            },
            data: JSON.stringify({
                'product': product,
            }),
            success: function(response){
                removeCartItem(product);
                updateCartTotals(response.cart)
            }
        })
    });

    $(document).on("click", ".quantityBtn", function () {
        let button = $(this);
        let input = button.siblings(".quantityInput");
        let current_qty = parseInt(input.val())
        if(button.hasClass("quantityMinus")){
            if(current_qty <= 1 ) {
                return false;
            }
            input.val(current_qty - 1);
            return true
        } else {
            input.val(current_qty + 1);
            return true;
        }
    })


    $(document).on("click", ".cartItemQuantityBtn", function() {
        let button = $(this);
        let input = button.siblings(".cartItem_quantityInput");
        let current_qty = parseInt(input.val())
        let cartItem_el = button.closest(".cartItem");
        let product_id = parseInt(cartItem_el.attr("data-item"));
        if(button.hasClass("quantityMinus")){
            if(current_qty <= 1 ) {
                $.ajax({
                    method: "POST",
                    url: '/api/v1/cart/remove-from-cart/',
                    contentType: 'application/json',
                    headers: {
                        'X-CSRFToken': csrf_token,
                    },
                    data: JSON.stringify({
                        'product': product_id,
                    }),
                    success: function(response){
                        removeCartItem(product_id);
                        updateCartTotals(response.cart)
                    }
                })
                return false;
            }
            $.ajax({
                method: "POST",
                url: '/api/v1/cart/update-cart-item/',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrf_token,
                },
                data: JSON.stringify({
                    'product': product_id,
                    'quantity': current_qty - 1,
                }),
                success: function(response){
                    updateCartItem(cartItem_el, current_qty-1);
                    updateCartTotals(response.cart)
                }
            })
            return true
        } else {
            $.ajax({
                method: "POST",
                url: '/api/v1/cart/update-cart-item/',
                contentType: 'application/json',
                headers: {
                    'X-CSRFToken': csrf_token,
                },
                data: JSON.stringify({
                    'product': product_id,
                    'quantity': current_qty + 1,
                }),
                success: function(response){
                    updateCartItem(cartItem_el, current_qty+1);
                    updateCartTotals(response.cart)
                }
            })
            return true;
        }
    })
    $(document).on("click", "#cartIcon", function(){
        showCart();
    })
})