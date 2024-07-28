$(document).ready(function () {
  const csrf_token = $("[name=csrfmiddlewaretoken]").val();
  const cartQuantityContainer = $("#cartQuantityContainer");
  const overlay = $("#overlay");
  const cartContainer = $("#sideCart");
  const cartBody = cartContainer.find(".cartBody");
  const cartTotalContainer = $("#cartTotal");
  const cartItem_template = $("#cartItem_template");
  const menuIcon = $("#menuIcon");
  const menuContainer = $("#menuContainer");
  let searchResultsContainer = $('#searchResultsContainer');
  const toggleables = document.querySelectorAll('.toggleable');

  toggleables.forEach(function (toggle) {
    toggle.addEventListener('click', function () {
      const targetId = this.getAttribute('data-target');
      const descriptions = document.querySelectorAll('.description');

      descriptions.forEach(desc => {
        if (desc.id === targetId) {
          desc.style.display = 'block';
          toggle.classList.add('text-brand-tertiary');
        } else {
          document.querySelector('[data-target="' + desc.id + '"]').classList.remove('text-brand-tertiary');
          desc.style.display = 'none';
        }
      });
    });
  });

  function showCart() {
    showOverlay();
    cartContainer.addClass("active")
  }

  function hideCart() {
    hideOverlay();
    cartContainer.removeClass("active")
  }

  function showOverlay() {
    $("body").addClass("overflow-hidden");
    overlay.show();
  }

  function hideOverlay() {
    $("body").removeClass("overflow-hidden");
    overlay.hide();
  }


  function addCartItem(response) {
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


  function removeCartItem(id) {
    let el = cartBody.find(`.cartItem[data-item='${id}']`).remove();
  }

  function updateCartTotals(response) {
    cartQuantityContainer.text(response.productCount);
    cartTotalContainer.text(response.total_price);
  }


  function updateCartItem(cartItem_el, quantity) {
    cartItem_el.find(".cartItem_quantityText").text(quantity);
    cartItem_el.find(".cartItem_quantityInput").val(quantity);
  }

  $(document).on("click", "#menuIcon", function () {
    menuContainer.toggleClass("hidden");
  })

  $(document).on("click", ".addToCartBtn", function () {
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
      success: function (response) {
        if (button.hasClass("goToCheckoutBtn")) {
          window.location.href = '/checkout/';
          return;
        }
        addCartItem(response.cartItem);
        updateCartTotals(response.cart)
        showCart();
      }
    })
  });


  $(document).on("click", ".removeCartItemBtn", function () {
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
      success: function (response) {
        removeCartItem(product);
        updateCartTotals(response.cart)
      }
    })
  });

  $(document).on("click", ".quantityBtn", function () {
    let button = $(this);
    let input = button.siblings(".quantityInput");
    let current_qty = parseInt(input.val())
    if (button.hasClass("quantityMinus")) {
      if (current_qty <= 1) {
        return false;
      }
      input.val(current_qty - 1);
      return true
    } else {
      input.val(current_qty + 1);
      return true;
    }
  })


  $(document).on("click", ".cartItemQuantityBtn", function () {
    let button = $(this);
    let input = button.siblings(".cartItem_quantityInput");
    let current_qty = parseInt(input.val())
    let cartItem_el = button.closest(".cartItem");
    let product_id = parseInt(cartItem_el.attr("data-item"));
    if (button.hasClass("quantityMinus")) {
      if (current_qty <= 1) {
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
          success: function (response) {
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
        success: function (response) {
          updateCartItem(cartItem_el, current_qty - 1);
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
        success: function (response) {
          updateCartItem(cartItem_el, current_qty + 1);
          updateCartTotals(response.cart)
        }
      })
      return true;
    }
  })
  $(document).on("click", "#cartIcon", function () {
    showCart();
  })

  $(document).on("click", "#cart__closeButton", function () {
    hideCart();
  })

  $(document).on("click", "#overlay", function () {
    hideCart();
  })

  $('.searchInput').each(function () {
    $(this).on('input', function () {
      let searchTerm = $(this).val();
      let searchResultsContainer = $(this).siblings('.searchResultsContainer');

      $.ajax({
        url: '/api/v1/search-product-titles/',
        type: 'GET',
        headers: {
          'X-CSRFToken': csrf_token,
        },
        data: {q: searchTerm},
        dataType: 'json',
        success: function (response) {
          console.log(response.products);
          searchResultsContainer.empty();

          if (response.products && response.products.length > 0) {
            response.products.forEach(function (product) {
              searchResultsContainer.append('<a href="' + product.url + '" class="font-bold text-brand-secondary hover:text-white hover:bg-brand-primary/80 p-2 w-full rounded-b-lg">' + product.title + '</a>');
            });
          } else {
            searchResultsContainer.append('<p>Не пронајдовме резултати...</p>');
          }
        },
        error: function (xhr, status, error) {
          console.error('Error fetching product titles:', error);
        }
      });
    });
  });


})