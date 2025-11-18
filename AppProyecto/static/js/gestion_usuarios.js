// Buscar usuarios (filtro simple)
document.getElementById("searchInput").addEventListener("keyup", function () {
    let filter = this.value.toLowerCase();
    let rows = document.querySelectorAll("#userTableBody tr");

    rows.forEach(row => {
        let text = row.innerText.toLowerCase();
        row.style.display = text.includes(filter) ? "" : "none";
    });
});

// Botón de "Nuevo Usuario"
document.getElementById("addUserBtn").addEventListener("click", function () {
    alert("Aquí puedes abrir un modal o redirigir a crear un usuario.");
});
