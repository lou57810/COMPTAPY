// static/js/journal/comptes.js

import { fetchCompte, createCompteAuto } from "./api.js";

export async function handleCompteChange(hot, row, newValue, entrepriseId, journalType) {

    // ===================== COLONNE 2 =====================
    //if (String(prop) === "2" && newValue && newValue !== oldValue) {
    if (newValue) {


        // const numeroActuel = hotInstance.getDataAtCell(row, 1);
        const numeroActuel = hot.getDataAtCell(row, 1);


        // Cas : l'utilisateur tape un NOM alors que le numéro est vide
        if (!numeroActuel) {

            fetch(`/api/comptes/${entrepriseId}/auto-create/`, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    nom: newValue,
                    journal_type: journalType
                })
            })
            .then(r => r.json())
            .then(created => {
                internalChange = true;
                hot.setDataAtCell(row, 1, created.numero); // numéro généré
                hot.setDataAtCell(row, 2, created.nom);    // nom normalisé
                internalChange = false;
            });

            return;
        }
    }
    // Cas : nom saisi
    if (isNaN(newValue)) {
        const created = await createCompteAuto(entrepriseId, {
            nom: newValue,
            journal_type: journalType
        });

        hot.setDataAtCell(row, 1, created.numero);
        hot.setDataAtCell(row, 2, created.nom);
        return;
    }

    // Cas : numéro saisi
    const data = await fetchCompte(entrepriseId, newValue);

    if (data.nom) {
        hot.setDataAtCell(row, 2, data.nom);
    } else {
        const created = await createCompteAuto(entrepriseId, {
            numero: newValue,
            journal_type: journalType
        });

        hot.setDataAtCell(row, 1, created.numero);
        hot.setDataAtCell(row, 2, created.nom);
    }
}
