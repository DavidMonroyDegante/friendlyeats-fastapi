const API_URL = "/api/v1/restaurants/";

const restaurantsList = document.getElementById("restaurantsList");
const resultsCount = document.getElementById("resultsCount");
const filterForm = document.getElementById("filterForm");
const clearFilters = document.getElementById("clearFilters");
const message = document.getElementById("message");

const citySelect = document.getElementById("city");
const categorySelect = document.getElementById("category");
const priceSelect = document.getElementById("price");



const pagination = document.getElementById("pagination");

const PAGE_SIZE = 5;

let currentPage = 1;
let currentRestaurants = [];


// ==========================================
// CARGAR CIUDADES Y CATEGORÍAS
// ==========================================
async function loadFilterOptions() {
    try {
        const response = await fetch(
            "/api/v1/restaurants/filter-options"
        );

        if (!response.ok) {
            throw new Error(
                "No se pudieron cargar las opciones de los filtros."
            );
        }

        const options = await response.json();

        // Cargar ciudades
        citySelect.innerHTML = "";

        const allCities = document.createElement("option");
        allCities.value = "";
        allCities.textContent = "Todas las ciudades";
        citySelect.appendChild(allCities);

        options.cities.forEach((city) => {
            const option = document.createElement("option");
            option.value = city;
            option.textContent = city;

            citySelect.appendChild(option);
        });

        // Cargar categorías
        categorySelect.innerHTML = "";

        const allCategories = document.createElement("option");
        allCategories.value = "";
        allCategories.textContent = "Todas las categorías";
        categorySelect.appendChild(allCategories);

        options.categories.forEach((category) => {
            const option = document.createElement("option");
            option.value = category;
            option.textContent = category;

            categorySelect.appendChild(option);
        });

    } catch (error) {
        console.error("Error al cargar los filtros:", error);

        message.textContent =
            "No se pudieron cargar las ciudades y categorías.";
    }
}


// ==========================================
// CARGAR RESTAURANTES Y APLICAR FILTROS
// ==========================================
async function loadRestaurants(filters = {}) {
    currentPage = 1;
    restaurantsList.innerHTML = "<p>Cargando restaurantes...</p>";
    resultsCount.textContent = "Consultando...";
    message.textContent = "";

    const params = new URLSearchParams();

    if (filters.city) {
        params.append("city", filters.city);
    }

    if (filters.category) {
        params.append("category", filters.category);
    }

    if (filters.price) {
        params.append("price", filters.price);
    }

    let url = API_URL;

    if (params.toString()) {
        url = "/api/v1/restaurants/filter?" + params.toString();
    }

    try {
        const response = await fetch(url);

        if (!response.ok) {
            throw new Error(
                "No se pudieron consultar los restaurantes."
            );
        }

        const restaurants = await response.json();

        currentRestaurants = restaurants;
        displayRestaurants();   

    } catch (error) {
        restaurantsList.innerHTML = "";
        resultsCount.textContent = "";

        message.textContent =
            "Ocurrió un error al cargar los restaurantes. " +
            "Comprueba que la aplicación esté funcionando.";

        console.error(error);
    }
}


// ==========================================
// MOSTRAR TARJETAS DE RESTAURANTES
// ==========================================

function displayRestaurants() {
    restaurantsList.innerHTML = "";
    pagination.innerHTML = "";

    const total = currentRestaurants.length;
    const totalPages = Math.ceil(total / PAGE_SIZE);

    if (total === 0) {
        resultsCount.textContent = "0 restaurantes encontrados";
        restaurantsList.innerHTML =
            "<p>No se encontraron restaurantes con esos filtros.</p>";
        return;
    }

    const start = (currentPage - 1) * PAGE_SIZE;
    const end = Math.min(start + PAGE_SIZE, total);
    const pageRestaurants = currentRestaurants.slice(start, end);

    resultsCount.textContent =
        `Mostrando ${start + 1}-${end} de ${total} restaurantes`;

    pageRestaurants.forEach((restaurant) => {
        const card = document.createElement("article");
        card.className = "restaurant-card";

        const image = document.createElement("img");
        image.className = "restaurant-image";
        image.alt = "Fotografía de " + restaurant.name;
        image.loading = "lazy";
        image.src = restaurant.photoUrl ||
            "https://placehold.co/600x400?text=FriendlyEats";

        image.onerror = () => {
            image.onerror = null;
            image.src = "https://placehold.co/600x400?text=Restaurante";
        };

        const info = document.createElement("div");
        info.className = "restaurant-info";

        const name = document.createElement("h3");
        name.textContent = restaurant.name;

        const category = document.createElement("p");
        category.textContent = restaurant.category;

        const city = document.createElement("p");
        city.textContent = "📍 " + restaurant.city;

        const price = document.createElement("p");
        price.textContent = "Precio: " + "$".repeat(restaurant.price);

        const rating = document.createElement("p");
        rating.className = "restaurant-rating";

        const average = Number(restaurant.avgRating || 0);
        const numberOfRatings = Number(restaurant.numRatings || 0);

        rating.textContent = numberOfRatings > 0
            ? "★ " + average.toFixed(1) +
              " (" + numberOfRatings + " opiniones)"
            : "Sin calificaciones";

        const link = document.createElement("a");
        link.className = "restaurant-link";
        link.href = "/restaurant/" + encodeURIComponent(restaurant.id);
        link.textContent = "Ver detalles →";

        info.append(name, category, city, price, rating, link);
        card.append(image, info);
        restaurantsList.appendChild(card);
    });

    if (totalPages > 1) {
        const previousButton = document.createElement("button");
        previousButton.type = "button";
        previousButton.className = "btn-secondary";
        previousButton.textContent = "← Anterior";
        previousButton.disabled = currentPage === 1;

        previousButton.addEventListener("click", () => {
            if (currentPage > 1) {
                currentPage--;
                displayRestaurants();
            }
        });

        const pageLabel = document.createElement("span");
        pageLabel.textContent =
            `Página ${currentPage} de ${totalPages}`;

        const nextButton = document.createElement("button");
        nextButton.type = "button";
        nextButton.className = "btn-secondary";
        nextButton.textContent = "Siguiente →";
        nextButton.disabled = currentPage === totalPages;

        nextButton.addEventListener("click", () => {
            if (currentPage < totalPages) {
                currentPage++;
                displayRestaurants();
            }
        });

        pagination.append(previousButton, pageLabel, nextButton);
    }
}



// ==========================================
// BUSCAR CON LOS FILTROS SELECCIONADOS
// ==========================================
filterForm.addEventListener("submit", (event) => {
    event.preventDefault();

    const city = citySelect.value;
    const category = categorySelect.value;
    const price = priceSelect.value;

    loadRestaurants({
        city,
        category,
        price
    });
});


// ==========================================
// LIMPIAR FILTROS
// ==========================================
clearFilters.addEventListener("click", () => {
    filterForm.reset();

    loadRestaurants();
});


// ==========================================
// INICIAR LA PÁGINA
// ==========================================
async function initializePage() {
    await loadFilterOptions();
    await loadRestaurants();
}

initializePage();