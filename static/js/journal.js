// ############# Tableau saisie ###################

let totalDebit = 0;
let totalCredit = 0;
document.addEventListener("DOMContentLoaded", function () {

  const container = document.getElementById('hot');
  if (!container) return;

  // const journalType = container.dataset.journalType || 'autre';
  let internalChange = false;

  // Données initiales : 1 ligne de saisie + 1 ligne TOTAL
  const initialData = [
    ['', '', '', '', '', '', '', '', '', ''],
  ];

  const hot = new Handsontable(container, {
    data: initialData,
    colHeaders: ['Date', 'Compte', 'Nom', 'Libellé', 'PU ht', 'Quantité', 'Taux Tva', 'Débit', 'Crédit', 'Solde'],
    columns: [
      { type: 'date', dateFormat: 'DD/MM/YYYY' }, // 0 - Date
      { type: 'text' },                           // 1 - Compte
      { type: 'text', readOnly: true },           // 2 - nom
      { type: 'text' },                           // 3 - Libellé
      { type: 'numeric',
        numericFormat: {
        pattern: '0.00', // 👉 toujours 2 décimales
        culture: 'fr-FR' // optionnel, pour gérer la virgule décimale si besoin
        }
      },                        // 4 - PU ht
      { type: 'numeric' },                        // 5 - Quantité
      { type: 'numeric' },                        // 6 - Tva
      { type: 'numeric',
        numericFormat: {
        pattern: '0.00', // 👉 toujours 2 décimales
        culture: 'fr-FR' // optionnel, pour gérer la virgule décimale si besoin
        }
      },                        // 7 - Débit
      { type: 'numeric',
        numericFormat: {
        pattern: '0.00', // 👉 toujours 2 décimales
        culture: 'fr-FR' // optionnel, pour gérer la virgule décimale si besoin
        }
      },                        // 8 - Crédit
      { type: 'numeric',
        numericFormat: {
        pattern: '0.00', // 👉 toujours 2 décimales
        culture: 'fr-FR' // optionnel, pour gérer la virgule décimale si besoin
        }
      },                        // 9 - Solde
    ],
    width: '100%',
    height: 'auto',
    rowHeaders: true,
    colWidths: [80, 80, 200, 300, 80, 80, 80, 80, 80, 80],
    manualColumnResize: true,
    // minSpareRows: 1,
    autoWrapRow: true,
    autoWrapCol: true,
    licenseKey: 'non-commercial-and-evaluation',

    afterChange: function (changes, source) {
      if (internalChange || source !== 'edit') return;

      changes.forEach(([row, prop, oldValue, newValue]) => {
        // 🔹 Auto-complétion nom du compte fournisseur
        if (String(prop) === '1' && newValue !== oldValue) {
          fetch(`/api/comptes/numero/?numero=${encodeURIComponent(newValue)}`)
            .then(response => response.json())
            .then(data => {
              if (data.nom) {
                hot.setDataAtCell(row, 2, data.nom); // Colonne 2 = Nom
              } else {
                hot.setDataAtCell(row, 2, 'Compte introuvable');
              }
              internalChange = false;
            });
          }

        if (['4', '5', '6'].includes(String(prop))) {
          const pu_ht = parseFloat(hot.getDataAtCell(row, 4)) || 0;
          const quantite = parseFloat(hot.getDataAtCell(row, 5)) || 0;
          const taux_tva = parseFloat(hot.getDataAtCell(row, 6)) || 0;

                                                          //   ^^
          if (pu_ht && quantite && taux_tva != 0) {    // tva != 0  ^^ sinon les lignes s'affichent avant le choix du taux
            const montantHT = +(pu_ht * quantite).toFixed(2);
            const montantTVA = +(montantHT * taux_tva / 100).toFixed(2);
            const montantTTC = +(montantHT * (1 + taux_tva / 100)).toFixed(2);

            const date = hot.getDataAtCell(row, 0);
            internalChange = true;

            // 🔹 Calcul automatique après modification PU HT, Quantité, TVA
            // Crédit du fournisseur
            hot.setDataAtCell(row, 8, montantTTC);

            // Ligne 2 : TVA ###########################################
            const ligneTVA = hot.countRows();
            hot.alter('insert_row_below', ligneTVA);
            hot.setDataAtCell(ligneTVA, 0, date);
            hot.setDataAtCell(ligneTVA, 1, '44551');
            hot.setDataAtCell(ligneTVA, 2, 'TVA à décaisser');
            hot.setDataAtCell(ligneTVA, 7, montantTVA);

            // Copie du libellé (colonne 4) depuis la ligne client
            const libelleClient = hot.getDataAtCell(row, 3);
            if (libelleClient) {
              hot.setDataAtCell(ligneTVA, 3, libelleClient);
            }

            // Ligne 3 : Charge (HT) ####################################
            const ligneCharge = hot.countRows();
            hot.alter('insert_row_below', ligneCharge);
            hot.setDataAtCell(ligneCharge, 0, date);
            hot.setDataAtCell(ligneCharge, 1, '607');
            hot.setDataAtCell(ligneCharge, 2, 'Achats de marchandises');
            hot.setDataAtCell(ligneCharge, 7, montantHT);

            // Copie du libellé (colonne 4) depuis la ligne client
            // const libelleClient = hot.getDataAtCell(row, 3);
            if (libelleClient) {
              hot.setDataAtCell(ligneCharge, 3, libelleClient);
            }

            // Ligne 4 : Ajout ligne de Saisie ##########################
            const ligneSaisie = hot.countRows();
            internalChange = true;
            hot.alter('insert_row_below', ligneSaisie);
            internalChange = false;
          }
        }
      });


       insertOrUpdateTotalRow();
    }
  });

    function insertOrUpdateTotalRow() {
      totalDebit = 0;
      totalCredit = 0;

      const s_rows = hot.countRows();
      for (let row = 0; row < s_rows; row++) {
        const debit = parseFloat(hot.getDataAtCell(row, 7)) || 0;
        const credit = parseFloat(hot.getDataAtCell(row, 8)) || 0;
        totalDebit += debit;
        totalCredit += credit;
      }
      console.log('Totaux:', totalDebit, totalCredit);
    }

      // ############ Tableau Totaux #################

      // Date du jour
      const dateJour = new Date();
      today = dateJour.toLocaleDateString("fr");

      var data1 = [
          [today, 'Totaux', '', '', '', ],
          ];
      container1 = document.getElementById('hot-totals');

      const hotTotals = new Handsontable(container1, {
        colHeaders: ['Date', '', 'Débit', 'Crédit', 'Solde',],
        data: data1,
        startRows: 1,
        startCols: 6,
        width: '100%',
        height: 'auto',
        colWidths: [80, 875, 80, 80, 80],
        manualColumnResize: true,
        autoWrapRow: true,
        autoWrapCol: true,
        licenseKey: 'non-commercial-and-evaluation',
        });

      // 🔁 Mettre à jour le 2e tableau à chaque modification :
      function updateSecondTable() {
        hotTotals.setDataAtCell(0, 2, totalDebit.toFixed(2));
        hotTotals.setDataAtCell(0, 3, totalCredit.toFixed(2));
        hotTotals.setDataAtCell(0, 4, (totalDebit - totalCredit).toFixed(2));
        }

      // Appel régulier (ou depuis afterChange) :
      hot.addHook('afterChange', function () {
      insertOrUpdateTotalRow();
      updateSecondTable();

  });
    document.getElementById('validerEcritures').addEventListener('click', function () {
    const data = hot.getData(); // Récupère toutes les lignes du tableau Handsontable

    // Filtrer les lignes vides et "TOTAL"
    const lignesValides = data.filter(row => {
      const isEmpty = row.every(cell => cell === null || cell === '');
      const isTotalRow = String(row[4] || '').trim().toLowerCase() === 'total';
      return !isEmpty && !isTotalRow;
    });

    // Structure des données à envoyer à Django
    const payload = lignesValides.map(row => ({
      numero: row[1],     // numéro du compte
      nom: row[2],        // nom du compte
      libelle: row[4],    // libellé
      debit: row[7] || 0,
      credit: row[8] || 0,
    }));

    fetch('/api/journaux/valider_journal_achats/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'), // si CSRF est activé
      },
      body: JSON.stringify({ lignes: payload }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erreur serveur');
        }
        return response.json();
      })
      .then(data => {
        alert('Écritures enregistrées avec succès ✅');
        console.log(data);
      })
      .catch(error => {
        console.error('Erreur lors de l’enregistrement :', error);
        alert('Une erreur est survenue ❌');
      });
  });

  // Fonction pour récupérer le token CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) {
          cookieValue = decodeURIComponent(value);
          break;
        }
      }
    }
    return cookieValue;
  }

});


