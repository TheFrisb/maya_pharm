$(document).ready(function(){
    const csrf_token = $("[name=csrfmiddlewaretoken]").val();

    $(document).on("click", ".confirmOrderBtn", function(){
        let button = $(this);
        let orderId = parseInt($(button).data("order-id"));

        $.ajax({
            method: "POST",
            url: '/shopmanager/api/confirm-order/',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrf_token,
            },
            data: JSON.stringify({
                'order': orderId,
            }),
            success: function(){
                let row = button.closest("tr");
                row.addClass("bg-green-200")
                row.fadeOut("slow", function() {
                    row.remove();
                })
            }
        })
    })


    $(document).on("click", ".deleteOrderBtn", function(){
        let button = $(this);
        let orderId = parseInt($(button).data("order-id"));

        $.ajax({
            method: "POST",
            url: '/shopmanager/api/delete-order/',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrf_token,
            },
            data: JSON.stringify({
                'order': orderId,
            }),
            success: function(){
                let row = button.closest("tr");
                row.addClass("bg-black text-white")
                row.fadeOut("5000", function() {
                    row.remove();
                })
            }
        })
    })


     $(document).on("click", ".restoreOrderBtn", function(){
        let button = $(this);
        let orderId = parseInt($(button).data("order-id"));

        $.ajax({
            method: "POST",
            url: '/shopmanager/api/restore-order/',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrf_token,
            },
            data: JSON.stringify({
                'order': orderId,
            }),
            success: function(){
                let row = button.closest("tr");
                row.addClass("bg-black text-white")
                row.fadeOut("5000", function() {
                    row.remove();
                })
            }
        })
    })
})