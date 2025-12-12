document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("form-create-gerant");

    form.addEventListener("submit", function (e) {
        e.preventDefault();  // empêche le rechargement classique

        const formData = new FormData(form);

        fetch(form.action, {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest"
            }
        })
        .then(r => r.json())
        .then(data => {
            console.log("Réponse serveur:", data);

            if (data.success) {
                // 🔥 Redirige automatiquement vers le PGC du gérant créé
                const newEntrepriseId = data.entreprise_id;
                console.log("Nouvelle entreprise ID:", newEntrepriseId);

                window.location.href = `http:\/\/127.0.0.1:8000/api/entreprise/${newEntrepriseId}/pgc/`;
            } else {
                document.getElementById("response").innerHTML =
                    `<p style="color:red;">Erreur : ${data.error}</p>`;
            }
        })
        .catch(err => {
            console.error("Erreur AJAX:", err);
        });
    });
});
