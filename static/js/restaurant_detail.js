
const API_URL = "/api/v1/restaurants/";

const detailContainer = document.getElementById("restaurantDetail");
const detailContent = document.getElementById("detailContent");
const loadingMessage = document.getElementById("loadingMessage");
const detailMessage = document.getElementById("detailMessage");

const restaurantId = detailContainer.dataset.restaurantId;


// ==========================================
// CARGAR DETALLES DEL RESTAURANTE
// ==========================================
async function loadRestaurantDetail() {
    try {
        const response = await fetch(
            API_URL + encodeURIComponent(restaurantId)
        );

        if (response.status === 404) {
            throw new Error("No se encontró el restaurante solicitado.");
        }

        if (!response.ok) {
            throw new Error("No se pudo consultar el restaurante.");
        }

        const restaurant = await response.json();

        document.getElementById("detailName").textContent =
            restaurant.name;

        document.getElementById("detailCategory").textContent =
            "Categoría: " + restaurant.category;

        document.getElementById("detailCity").textContent =
            "Ciudad: " + restaurant.city;

        document.getElementById("detailPrice").textContent =
            "Precio: " + "$".repeat(restaurant.price);

        const average = Number(restaurant.avgRating || 0);
        const numberOfRatings = Number(restaurant.numRatings || 0);

        document.getElementById("detailRating").textContent =
            numberOfRatings > 0
                ? "★ " + average.toFixed(1) +
                  " (" + numberOfRatings + " opiniones)"
                : "Sin calificaciones";

        const image = document.getElementById("detailImage");

        image.src = restaurant.photoUrl ||
            "https://placehold.co/900x500?text=FriendlyEats";

        image.onerror = () => {
            image.onerror = null;
            image.src =
                "https://placehold.co/900x500?text=Restaurante";
        };

        document.getElementById("editRestaurant").addEventListener(
            "click",
            () => {
                window.location.href =
                    "/restaurant/new?id=" +
                    encodeURIComponent(restaurant.id);
            }
        );

        document.getElementById("deleteRestaurant").addEventListener(
            "click",
            deleteRestaurant
        );

        loadingMessage.hidden = true;
        detailContent.hidden = false;

    } catch (error) {
        loadingMessage.hidden = true;
        detailMessage.textContent = error.message;
        console.error(error);
    }
}


// ==========================================
// ELIMINAR RESTAURANTE
// ==========================================
async function deleteRestaurant() {
    const confirmation = window.confirm(
        "¿Seguro que deseas eliminar este restaurante? Esta acción no se puede deshacer."
    );

    if (!confirmation) {
        return;
    }

    try {
        const response = await fetch(
            API_URL + encodeURIComponent(restaurantId),
            {
                method: "DELETE"
            }
        );

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));

            throw new Error(
                errorData.detail || "No se pudo eliminar el restaurante."
            );
        }

        window.alert("Restaurante eliminado correctamente.");

        window.location.href = "/";

    } catch (error) {
        detailMessage.textContent = error.message;
        console.error(error);
    }
}


// ==========================================
// INICIAR PÁGINA
// ==========================================
loadRestaurantDetail();
