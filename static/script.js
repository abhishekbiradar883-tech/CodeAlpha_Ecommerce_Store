// 1. Load saved cart
var cart = [];

try {
    cart = JSON.parse(localStorage.getItem("cart")) || [];
} catch (error) {
    cart = [];
}

// 2. Save cart
function saveCart() {
    localStorage.setItem("cart", JSON.stringify(cart));
}

// 3. Add product to cart
function addToCart(id, name, price) {

    id = Number(id);
    price = Number(price);

    var existingProduct = null;

    for (var i = 0; i < cart.length; i++) {
        if (Number(cart[i].id) === id) {
            existingProduct = cart[i];
            break;
        }
    }

    if (existingProduct) {
        existingProduct.quantity++;
    } else {
        cart.push({
            id: id,
            name: name,
            price: price,
            quantity: 1
        });
    }

    saveCart();
    updateCart();

    alert(name + " added to cart!");
}

// 4. Display cart
function updateCart() {

    var cartItems = document.getElementById("cart-items");
    var totalElement = document.getElementById("total");
    var countElement = document.getElementById("cart-count");

    if (!cartItems || !totalElement || !countElement) {
        return;
    }

    var total = 0;
    var count = 0;

    cartItems.innerHTML = "";

    for (var i = 0; i < cart.length; i++) {

        var item = cart[i];
        var itemTotal = item.price * item.quantity;

        total += itemTotal;
        count += item.quantity;

        var paragraph = document.createElement("p");

        paragraph.textContent =
            item.name + " - ₹" + item.price +
            " x " + item.quantity +
            " = ₹" + itemTotal.toFixed(2) + " ";

        var removeButton = document.createElement("button");

        removeButton.textContent = "Remove";
        removeButton.type = "button";

        removeButton.onclick = (function(index) {
            return function() {
                removeFromCart(index);
            };
        })(i);

        paragraph.appendChild(removeButton);
        cartItems.appendChild(paragraph);
    }

    totalElement.textContent = total.toFixed(2);
    countElement.textContent = count;
}

// 5. Remove product
function removeFromCart(index) {

    cart.splice(index, 1);

    saveCart();
    updateCart();
}

// 6. Search products
document.addEventListener("DOMContentLoaded", function() {

    var searchInput = document.getElementById("search");

    if (searchInput) {

        searchInput.addEventListener("input", function() {

            var searchValue = searchInput.value.toLowerCase();

            var products = document.querySelectorAll(
                ".products-container .product-card"
            );

            products.forEach(function(product) {

                var heading = product.querySelector("h3");

                if (heading) {
                    var productName = heading.textContent.toLowerCase();

                    product.style.display =
                        productName.includes(searchValue) ? "" : "none";
                }
            });
        });
    }

    updateCart();
});

// 7. Get Django CSRF token
function getCSRFToken() {

    var cookieValue = null;

    var cookies = document.cookie.split(";");

    for (var i = 0; i < cookies.length; i++) {

        var cookie = cookies[i].trim();

        if (cookie.indexOf("csrftoken=") === 0) {
            cookieValue = decodeURIComponent(
                cookie.substring("csrftoken=".length)
            );
            break;
        }
    }

    return cookieValue;
}

// 8. Checkout
function checkout() {

    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    fetch("/place_order/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },

        body: JSON.stringify({
            cart: cart.map(function(item) {
                return {
                    id: item.id,
                    quantity: item.quantity
                };
            })
        })

    })

    .then(function(response) {
        return response.json();
    })

    .then(function(data) {

        alert(data.message);

        if (data.success) {
            cart = [];
            saveCart();
            updateCart();
        }

    })

    .catch(function(error) {

        console.error("Checkout error:", error);

        alert("Something went wrong. Please try again.");
    });
}