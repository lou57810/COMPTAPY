// static/js/journal/save.js

import { computeTotals, updateTotalTable } from "./calculs.js";
import { loadJournalEntries } from "./loader.js";

export function setupSaveButton(hot, hotTotals, entrepriseId, csrfToken, baseRowsCountRef) {
    const btn = document.getElementById("validerEcritures");
    if (!btn) return;

    btn.addEventListener("click", async (event) => {
        event.preventDefault();
        event.stopPropagation();

        const urlValidation = btn.dataset.urlValidation;
        if (!urlValidation) {
            console.error("URL de validation absente");
            return;
        }

        // Collecte des lignes saisies
        const lignes = collectLignes(hot, baseRowsCountRef.value);

        if (lignes.length === 0) {
            alert("Aucune ligne à enregistrer.");
            return;
        }

        // Envoi au backend
        const ok = await sendToBackend(urlValidation, entrepriseId, csrfToken, lignes);
        if (!ok) return;

        alert("Écritures enregistrées avec succès ✅");

        // Rechargement du journal
        await reloadJournal(hot, hotTotals, baseRowsCountRef);
    });
}

// ==================== Collecte des lignes ====================

function collectLignes(hot, baseRowsCount) {
    const lignes = [];

    for (let row = baseRowsCount; row < hot.countRows(); row++) {
        const ligne = hot.getDataAtRow(row);

        const hasContent = ligne.some(
            (cell) => cell !== null && cell !== "" && cell !== undefined
        );
        if (!hasContent) continue;

        const [
            date, numero, nom, numero_piece, libelle,
            pu_ht_raw, quantite_raw, taux_raw, debit_raw, credit_raw
        ] = ligne;

        lignes.push({
            date,
            numero,
            nom,
            numero_piece,
            libelle,
            pu_ht: parseFloat(pu_ht_raw) || 0,
            quantite: parseFloat(quantite_raw) || 0,
            taux: parseFloat(taux_raw) || 0,
            debit: parseFloat(debit_raw) || 0,
            credit: parseFloat(credit_raw) || 0,
        });
    }

    return lignes;
}

// ==================== Envoi au backend ====================

async function sendToBackend(url, entrepriseId, csrfToken, lignes) {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({
                entreprise_id: entrepriseId,
                lignes: lignes,
            }),
        });

        if (!response.ok) {
            const text = await response.text();
            throw new Error(text);
        }

        return true;

    } catch (error) {
        console.error("Erreur serveur réelle :", error);
        alert("Erreur lors de l’enregistrement ❌");
        return false;
    }
}

// ==================== Rechargement du journal ====================

async function reloadJournal(hot, hotTotals, baseRowsCountRef) {
    const journalType = document.getElementById("journal_type")?.value;
    const journalUrl = document.getElementById("journal_url")?.value;

    if (!journalType || !journalUrl) {
        // fallback : vider la saisie
        hot.loadData([["", "", "", "", "", "", "", "", "", ""]]);
        baseRowsCountRef.value = 0;

        const { totalDebit, totalCredit } = computeTotals(hot);
        updateTotalTable(hotTotals, totalDebit, totalCredit);
        return;
    }

    const { baseRowsCount } = await loadJournalEntries(hot, journalUrl, journalType);
    baseRowsCountRef.value = baseRowsCount;

    const { totalDebit, totalCredit } = computeTotals(hot);
    updateTotalTable(hotTotals, totalDebit, totalCredit);
}
