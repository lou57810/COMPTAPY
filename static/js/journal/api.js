// static/js/journal/api.js

export async function fetchCompte(entrepriseId, numero) {
    const r = await fetch(`/api/comptes/${entrepriseId}/numero/?numero=${numero}`);
    return r.json();
}

export async function createCompteAuto(entrepriseId, payload) {
    const r = await fetch(`/api/comptes/${entrepriseId}/auto-create/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });
    return r.json();
}
