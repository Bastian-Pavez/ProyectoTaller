document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const loadingOverlay = document.querySelector(".loading-overlay");
    
    form.addEventListener("submit", function() {
        loadingOverlay.style.display = "flex"; // Muestra el círculo de carga
    });
});



document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const loadingOverlay = document.querySelector(".loading-overlay");
    const errorMessage = document.querySelector(".error-message");

    // Muestra el overlay de carga al enviar el formulario
    form.addEventListener("submit", function() {
        loadingOverlay.style.display = "flex";
    });

    // Verifica si existe un mensaje de error
    if (errorMessage && errorMessage.textContent.trim() !== "") {
        // Muestra el mensaje de error
        errorMessage.style.display = "block";
        
        // Oculta el mensaje de error después de 5 segundos
        setTimeout(() => {
            errorMessage.style.display = "none";
        }, 5000);
    }
});


document.getElementById('loginForm').addEventListener('submit', function (e) {
    const overlay = document.getElementById('loadingOverlay');
    const submitBtn = this.querySelector('button[type="submit"]');

    overlay.classList.add('active');
    submitBtn.disabled = true;
});
