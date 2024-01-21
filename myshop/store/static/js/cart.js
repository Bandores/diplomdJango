document.addEventListener("DOMContentLoaded", function () {
    const increaseButtons = document.querySelectorAll(".increase-quantity");
    const decreaseButtons = document.querySelectorAll(".decrease-quantity");
    const quantityElements = document.querySelectorAll(".item-quantity");
    const priceElements = document.querySelectorAll(".cart-item-price");
    const cartTotalElement = document.getElementById("cart-total");

    updateCartTotal();  // Вызов функции при загрузке страницы

    increaseButtons.forEach((button, index) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            const currentItem = event.target.closest(".cart-item");
            const quantityElement = currentItem.querySelector(".item-quantity");
            const priceElement = currentItem.querySelector(".cart-item-price");
            const pricePerItem = parseFloat(priceElement.getAttribute("data-price"));
            const currentQuantity = parseInt(quantityElement.textContent);

            quantityElement.textContent = currentQuantity + 1;
            updateCartItemPrice(priceElement, pricePerItem, currentQuantity + 1);
            updateCartTotal();
        });
    });

    decreaseButtons.forEach((button, index) => {
        button.addEventListener("click", (event) => {
            event.preventDefault();
            const currentItem = event.target.closest(".cart-item");
            const quantityElement = currentItem.querySelector(".item-quantity");
            const priceElement = currentItem.querySelector(".cart-item-price");
            const pricePerItem = parseFloat(priceElement.getAttribute("data-price"));
            const currentQuantity = parseInt(quantityElement.textContent);

            if (currentQuantity > 1) {
                quantityElement.textContent = currentQuantity - 1;
                updateCartItemPrice(priceElement, pricePerItem, currentQuantity - 1);
                updateCartTotal();
            }
        });
    });

    function updateCartItemPrice(priceElement, pricePerItem, quantity) {
        const totalPrice = (pricePerItem * quantity).toFixed(2);
        priceElement.textContent = "$" + totalPrice;
    }

    function updateCartTotal() {
        let total = 0;
        priceElements.forEach((priceElement) => {
            const pricePerItem = parseFloat(priceElement.getAttribute("data-price"));
            const quantityElement = priceElement.closest(".cart-item").querySelector(".item-quantity");
            const quantity = parseInt(quantityElement.textContent);
            total += pricePerItem * quantity;
        });
        cartTotalElement.textContent = total.toFixed(2);
    }
});
