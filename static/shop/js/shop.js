$(document).ready(function(){
    console.log("jquery loaded")
    const csrf_token = $("[name=csrfmiddlewaretoken]").val();
    $(document).on("click", ".addToCartBtn", function(){
        console.log('')
        let button = $(this);
        let product = parseInt(button.data("product-id"));

        $.ajax({
            method: "POST",
            url: '/api/v1/cart/add-to-cart/',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrf_token,
            },
            data: JSON.stringify({
                'product': product,
            }),
            success: function(){
                alert("added to cart")
            }
        })
    })
})