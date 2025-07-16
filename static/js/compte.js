// compte.js

document.addEventListener('DOMContentLoaded', function () {
  const container = document.getElementById('journal-display');
  if (container) {
  const numeroCompte = document.querySelector('[data-compte-numero]')?.dataset?.compteNumero;

  if (numeroCompte) {
    console.log('numero js:', numeroCompte);
    fetch(`/api/ecritures/?numero=${numeroCompte}`)
      .then(response => response.json())
      .then(data => {
        // Préparation des lignes pour Handsontable avec calcul du solde
        let solde = 0;
        console.log("👉 Écritures reçues:", data);
        const journalData = data.map(ligne => {
            solde += (parseFloat(ligne.debit) || 0) - (parseFloat(ligne.credit) || 0);
        return [
              ligne.date,
              ligne.numero_piece,
              ligne.libelle,
              ligne.debit,
              ligne.credit,
              solde.toFixed(2)
            ];
          });

        new Handsontable(container, {
            data: journalData,
            colHeaders: ['Date', 'N° Pièce', 'Libellé', 'Débit', 'Crédit', 'Solde'],
            columns: [
              { type: 'text', readOnly: true },
              { type: 'text', readOnly: true },
              { type: 'text', readOnly: true },
              { type: 'numeric', numericFormat: { pattern: '0.00' }, readOnly: true },
              { type: 'numeric', numericFormat: { pattern: '0.00' }, readOnly: true },
              { type: 'numeric', numericFormat: { pattern: '0.00' }, readOnly: true }
            ],
            width: '100%',
            height: 'auto',
            rowHeaders: true,
            colWidths: [80, 80, 300, 100, 100, 100],
            manualColumnResize: true,
            autoWrapRow: true,
            autoWrapCol: true,
            licenseKey: 'non-commercial-and-evaluation',
          });
        });
    }
  }
});


