
let cart = [];

function addToCart(name, price) {
    cart.push({
        name: name,
        price: price
    });

    updateCart();
}

function updateCart() {
    let cartItems = document.getElementById("cart-items");
    let total = 0;

    cartItems.innerHTML = "";

    cart.forEach((item, index) => {
        total += item.price;

        cartItems.innerHTML += `
            <p>${item.name} - ₹${item.price}
            <button onclick="removeFromCart(${index})">Remove</button></p>
        `;
    });

    document.getElementById("total").innerText = total;
    document.getElementById("cart-count").innerText = cart.length;
}

function removeFromCart(index) {
    cart.splice(index, 1);
    updateCart();
}

const searchInput = document.getElementById("search");

searchInput.addEventListener("input", function () {
    let searchValue = searchInput.value.toLowerCase();

    let products = document.querySelectorAll(".product-card");

    products.forEach(function (product) {
        let productName = product.querySelector("h3").innerText.toLowerCase();

        if (productName.includes(searchValue)) {
            product.style.display = "inline-block";
        } else {
            product.style.display = "none";
        }
    });
});

function checkout() {
    if (cart.length === 0) {
        alert("Your cart is empty!");
        return;
    }

    fetch("/place_order", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ cart: cart })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);

        if (data.success) {
            cart = [];
            updateCart();
        }
    })
    .catch(error => {
        alert("Something went wrong!");
        console.error(error);
    });
}
