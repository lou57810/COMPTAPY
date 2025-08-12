// =======================
// Snippet Journal Banque
// =======================
export function configJournal() {
  return {
    nom: "Journal Banque",
    sens: "banque", // Type spécifique pour gestion des paiements
    colonnes: [
      { data: 0, type: 'date', title: 'Date' },
      { data: 1, type: 'text', title: 'Compte' },     // Banque
      { data: 2, type: 'text', title: 'Nom' },        // Client/Fournisseur
      { data: 3, type: 'text', title: 'Numéro Pièce' },
      { data: 4, type: 'text', title: 'Libellé' },
      // { data: 5, type: 'numeric', title: 'PU HT', numericFormat: { pattern: '0.00' } },
      // { data: 6, type: 'numeric', title: 'Quantité', numericFormat: { pattern: '0' } },
      { data: 7, type: 'numeric', title: 'Taux TVA %', numericFormat: { pattern: '0.00' } },
      { data: 8, type: 'numeric', title: 'Débit', numericFormat: { pattern: '0.00' } },
      { data: 9, type: 'numeric', title: 'Crédit', numericFormat: { pattern: '0.00' } },
    ],
    afterChangeHandler: function (hot, changes, source) {
      if (source === 'loadData' || internalChange) return;

      changes.forEach(([row, prop, oldValue, newValue]) => {
        // Détection : dès qu’on a assez d’infos pour calculer
        if (['5', '6', '7'].includes(prop)) {
          // const pu_ht = parseFloat(hot.getDataAtCell(row, 5)) || 0;
          // const quantite = parseFloat(hot.getDataAtCell(row, 6)) || 0;
          // const taux_tva = parseFloat(hot.getDataAtCell(row, 7)) || 0;

          // const montantHT = +(pu_ht * quantite).toFixed(2);
          // const montantTVA = +(montantHT * taux_tva / 100).toFixed(2);
          // const montantTTC = +(montantHT + montantTVA).toFixed(2);

          internalChange = true;

          // Règle : si montant positif → Encaissement (Débit banque)
          if (montantTTC > 0) {
            hot.setDataAtCell(row, 8, montantTTC); // Débit
            hot.setDataAtCell(row, 9, '');         // Vide crédit
          }
          // Si montant négatif → Décaissement (Crédit banque)
          else {
            hot.setDataAtCell(row, 9, Math.abs(montantTTC)); // Crédit
            hot.setDataAtCell(row, 8, '');                   // Vide débit
          }

          // Ajout auto des lignes TVA et contrepartie
          ajouterEcrituresAutomatiques(hot, { sens: 'banque' }, row,
            hot.getDataAtCell(row, 0), // date
            hot.getDataAtCell(row, 3), // numeroPiece
            hot.getDataAtCell(row, 4), // libelle
            pu_ht, quantite, taux_tva
          );

          internalChange = false;
        }
      });
    }
  };
}

