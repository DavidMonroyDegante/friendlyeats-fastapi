
const API_URL = "/api/v1/restaurants/";

const form = document.getElementById("restaurantForm");
const formMessage = document.getElementById("formMessage");
const saveButton = document.getElementById("saveButton");
const formTitle = document.getElementById("formTitle");

const restaurantId = form.dataset.restaurantId;

function showMessage(message) {
    formMessage.textContent = message;
}

async function loadRestaurant() {
    if (!restaurantId) {
        return;
    }

    formTitle.textContent = "Editar restaurante";
    saveButton.textContent = "Guardar cambios";

    try {
        const response = await fetch(
            API_URL + encodeURIComponent(restaurantId)
        );

        if (!response.ok) {
            throw new Error("No se encontró el restaurante.");
        }

        const restaurant = await response.json();

        document.getElementById("name").value = restaurant.name || "";
        document.getElementById("category").value = restaurant.category || "";
        document.getElementById("city").value = restaurant.city || "";
        document.getElementById("price").value = String(restaurant.price || "");
        document.getElementById("photoUrl").value = restaurant.photoUrl || "";

    } catch (error) {
        showMessage(error.message);
        saveButton.disabled = true;
    }
}

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const data = {
        name: document.getElementById("name").value.trim(),
        category: document.getElementById("category").value.trim(),
        city: document.getElementById("city").value.trim(),
        price: Number(document.getElementById("price").value),
        photoUrl: document.getElementById("photoUrl").value.trim() || null
    };

    saveButton.disabled = true;
    saveButton.textContent = "Guardando...";
    showMessage("");

    try {
        const isEditing = Boolean(restaurantId);

        const response = await fetch(
            isEditing
                ? API_URL + encodeURIComponent(restaurantId)
                : API_URL,
            {
                method: isEditing ? "PUT" : "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            }
        );

        const result = await response.json().catch(() => ({}));

        if (!response.ok) {
            const detail = result.detail;

            if (Array.isArray(detail)) {
                throw new Error(
                    detail.map(item => item.msg).join(", ")
                );
            }

            throw new Error(
                typeof detail === "string"
                    ? detail
                    : "No se pudo guardar el restaurante."
            );
        }

        window.location.href =
            "/restaurant/" + encodeURIComponent(result.id);

    } catch (error) {
        showMessage(error.message);
        saveButton.disabled = false;
        saveButton.textContent = restaurantId
            ? "Guardar cambios"
            : "Guardar restaurante";
    }
});

loadRestaurant();
