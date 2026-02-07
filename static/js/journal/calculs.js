// static/js/journal/calculs.js

// ==================== Mise à jour du tableau des totaux ====================

export function updateTotalTable(hotTotals, totalDebit, totalCredit) {
    hotTotals.setDataAtCell(0, 2, totalDebit.toFixed(2));
    hotTotals.setDataAtCell(0, 3, totalCredit.toFixed(2));
    hotTotals.setDataAtCell(0, 4, (totalDebit - totalCredit).toFixed(2));
}

// ==================== Calcul des totaux Débit / Crédit ====================

export function computeTotals(hot) {
    let totalDebit = 0;
    let totalCredit = 0;
    const rowCount = hot.countRows();

    for (let row = 0; row < rowCount; row++) {
        const debit = parseFloat(hot.getDataAtCell(row, 8)) || 0;
        const credit = parseFloat(hot.getDataAtCell(row, 9)) || 0;
        totalDebit += debit;
        totalCredit += credit;
    }

    return { totalDebit, totalCredit };
}

// ==================== Initialisation du tableau des totaux ====================
export function initTotalsTable(container) {
    const options = { year: "numeric", month: "numeric", day: "numeric" };
    const today = new Date().toLocaleDateString("fr-FR", options);

    const data = [[today, "Totaux", "", "", ""]];

    return new Handsontable(container, {
        colHeaders: ["Date", "", "Débit", "Crédit", "Solde"],
        data: data,
        startRows: 1,
        startCols: 5,
        width: "100%",
        height: "auto",
        colWidths: [80, 850, 80, 80, 80],
        manualColumnResize: true,
        autoWrapRow: true,
        autoWrapCol: true,
        licenseKey: "non-commercial-and-evaluation",
    });
}



export function calculTTC(pu, qte, tva) {
    return pu * qte * (1 + tva / 100);
}
export function ligneEstComplete(hot, row) {
    const date = hot.getDataAtCell(row, 0);
    const numero = hot.getDataAtCell(row, 1);
    const nom = hot.getDataAtCell(row, 2);
    const libelle = hot.getDataAtCell(row, 4);

    const pu_ht = parseFloat(hot.getDataAtCell(row, 5));
    const quantite = parseFloat(hot.getDataAtCell(row, 6));
    const taux_tva = parseFloat(hot.getDataAtCell(row, 7));

    return (
        date &&
        numero &&
        nom &&
        libelle &&
        !isNaN(pu_ht) &&
        !isNaN(quantite) &&
        !isNaN(taux_tva)
    );
}

export function calculMontants(hot, row) {
    const pu_ht = parseFloat(hot.getDataAtCell(row, 5));
    const quantite = parseFloat(hot.getDataAtCell(row, 6));
    const taux_tva = parseFloat(hot.getDataAtCell(row, 7));

    const montantHT = +(pu_ht * quantite).toFixed(2);
    const montantTVA = +((montantHT * taux_tva) / 100).toFixed(2);
    const montantTTC = +(montantHT + montantTVA).toFixed(2);

    return { montantHT, montantTVA, montantTTC };
}

export function appliquerDebitCredit(hot, row, montantTTC, sens) {
    if (sens === "achats") {
        // Achats → crédit fournisseur
        hot.setDataAtCell(row, 9, montantTTC); // Crédit
        hot.setDataAtCell(row, 8, "");         // Débit vide
    } else if (sens === "ventes") {
        // Ventes → débit client
        hot.setDataAtCell(row, 8, montantTTC); // Débit
        hot.setDataAtCell(row, 9, "");         // Crédit vide
    }
}

