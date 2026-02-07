// static/js/journal/hot.js

import { colHeaders, columnsConfig, hotSettings } from "./config.js";
import { handleCompteChange } from "./comptes.js";
import {
    computeTotals,
    updateTotalTable,
    initTotalsTable,
    ligneEstComplete,
    calculMontants,
    appliquerDebitCredit
} from "./calculs.js";
import { loadJournalEntries } from "./loader.js";
import { setupSaveButton } from "./save.js";

export async function initHot() {
    // 🔥 1) CSRF
    function getCookie(name) {
        return document.cookie
            .split('; ')
            .find(row => row.startsWith(name + '='))?.split('=')[1];
    }
    const csrfToken = getCookie("csrftoken");

    // 🔥 2) Variables locales
    let hot = null;
    let hotTotals = null;
    let internalChange = false;
    let baseRowsCount = 0;

    const journalType = document.getElementById("journal_type")?.value;
    const journalUrl = document.getElementById("journal_url")?.value;
    const entrepriseId = document.getElementById("entreprise_id")?.value;

    if (!journalType) {
        console.warn("Aucun journal sélectionné → initHot() en pause");
        return;
    }

    // 🔥 3) Chargement du snippet
    let config = {};
    try {
        const snippetModule = await import(`/static/js/snippets/${journalType}.js`);
        config = snippetModule.configJournal();
    } catch (error) {
        console.error(`❌ Erreur de chargement du snippet "${journalType}" :`, error);
        return;
    }

    // 🔥 4) Création du tableau Handsontable (IMPORTANT : AVANT setupSaveButton)
    const container = document.getElementById("journal-table");
    hot = new Handsontable(container, {
        data: [["", "", "", "", "", "", "", "", "", ""]],
        colHeaders: colHeaders,
        columns: columnsConfig,
        ...hotSettings,

        cells: function (row, col) {
            const props = {};
            if (row < baseRowsCount) props.readOnly = true;
            return props;
        },
    });

    // 🔥 5) Chargement initial des écritures
    const baseRowsCountRef = { value: 0 };

    internalChange = true;
    loadJournalEntries(hot, journalUrl, journalType)
        .then(({ baseRowsCount: count }) => {
            baseRowsCount = count;
            baseRowsCountRef.value = count;
        })
        .finally(() => {
            internalChange = false;
        });

    // 🔥 6) Initialisation du tableau des totaux
    const totalsContainer = document.getElementById("journal-totals");
    hotTotals = initTotalsTable(totalsContainer);

    // 🔥 7) Initialisation du bouton de sauvegarde (MAINTENANT que hot existe)
    setupSaveButton(hot, hotTotals, entrepriseId, csrfToken, baseRowsCountRef);

    // 🔥 8) Hook afterChange
    hot.addHook("afterChange", async (changes, source) => {
        if (!changes || source === "loadData") return;

        const [row, prop, oldValue, newValue] = changes[0];

        if (row < baseRowsCount) return;

        if (prop === 1) {
            await handleCompteChange(hot, row, newValue, entrepriseId, journalType);
        }

        if (ligneEstComplete(hot, row)) {
            internalChange = true;

            const { montantTTC } = calculMontants(hot, row);
            appliquerDebitCredit(hot, row, montantTTC, journalType);

            internalChange = false;
        }

        const { totalDebit, totalCredit } = computeTotals(hot);
        updateTotalTable(hotTotals, totalDebit, totalCredit);
    });
}
/*
import { colHeaders, columnsConfig, hotSettings } from "./config.js";
import { handleCompteChange } from "./comptes.js";
import {
    computeTotals,
    updateTotalTable,
    initTotalsTable,
    ligneEstComplete,
    calculMontants,
    appliquerDebitCredit
} from "./calculs.js";
import { loadJournalEntries } from "./loader.js";
import { setupSaveButton } from "./save.js";

export async function initHot() {
    // 🔥 1) Définition du CSRF token:
    function getCookie(name) {
        return document.cookie
            .split('; ')
            .find(row => row.startsWith(name + '='))?.split('=')[1];
    }
    const csrfToken = getCookie("csrftoken");
    // ==================== Variables locales ====================
    let hot = null;
    let hotTotals = null;
    let internalChange = false;
    let baseRowsCount = 0;

    const journalType = document.getElementById("journal_type")?.value;
    const journalUrl = document.getElementById("journal_url")?.value;
    const entrepriseId = document.getElementById("entreprise_id")?.value;

    // 2) Si aucun journal n’est sélectionné → on arrête tout
    if (!journalType) {
        console.warn("Aucun journal sélectionné → initHot() en pause");
        return;
    }

    // 3) Chargement du snippet
    let config = {};
    try {
        const snippetModule = await import(`/static/js/snippets/${journalType}.js`);
        config = snippetModule.configJournal();
    } catch (error) {
        console.error(`❌ Erreur de chargement du snippet "${journalType}" :`, error);
        return;
    }

    // Référence mutable pour baseRowsCount
    const baseRowsCountRef = { value: 0 };

    // Chargement initial
    loadJournalEntries(hot, journalUrl, journalType)
        .then(({ baseRowsCount }) => baseRowsCountRef.value = baseRowsCount);

    // Initialisation du bouton de sauvegarde
    setupSaveButton(hot, hotTotals, entrepriseId, csrfToken, baseRowsCountRef);

    // const journalType = document.getElementById("journal_type")?.value;
    // const entrepriseId = document.getElementById("entreprise_id")?.value;
    const container = document.getElementById("journal-table");

    if (!entrepriseId) {
        console.error("❌ entrepriseId manquant");
    }


    // ==================== Initialisation Handsontable ====================
    // ======== Création du tableau ====================
    hot = new Handsontable(container, {
        data: [["", "", "", "", "", "", "", "", "", ""]],
        colHeaders: colHeaders,
        columns: columnsConfig,
        ...hotSettings,

        cells: function (row, col) {
            const props = {};
            if (row < baseRowsCount) props.readOnly = true;
            return props;
        },
    });

    // Chargement des écritures existantes
    internalChange = true;

    loadJournalEntries(hot, journalUrl, journalType)
        .then(({ baseRowsCount: count }) => {
            baseRowsCount = count;
        })
        .finally(() => {
            internalChange = false;
        });

    // Initialisation du tableau des totaux
    const totalsContainer = document.getElementById("journal-totals");
    hotTotals = initTotalsTable(totalsContainer);

    // Hook afterChange
    hot.addHook("afterChange", async (changes, source) => {
    if (!changes || source === "loadData") return;

    // On récupère la première modification
    const [row, prop, oldValue, newValue] = changes[0];

    if (row < baseRowsCount) return;

    // Gestion du compte (colonne 1)
    if (prop === 1) {
        await handleCompteChange(hot, row, newValue, entrepriseId, journalType);
    }

    // Calcul TTC uniquement si la ligne est complète
    if (ligneEstComplete(hot, row)) {
        internalChange = true;

        const { montantTTC } = calculMontants(hot, row);
        appliquerDebitCredit(hot, row, montantTTC, journalType);

        internalChange = false;
    }

    // Mise à jour des totaux
    const { totalDebit, totalCredit } = computeTotals(hot);
    updateTotalTable(hotTotals, totalDebit, totalCredit);
  });
}
*/



