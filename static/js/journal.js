// journal.js (doit être chargé comme type="module")
// Initialisation
let totalDebit = 0;
let totalCredit = 0;
let ligneSaisie = 0;
let cell = 0;
let row_base = 0;
let row = 0;
let internalChange = false;
let col = 0;



// ✅ ################ Fonction d'initialisation du tableau Handsontable #######################
function initHandsontable(container, config) {

  let cell = 0;

  const initialData = [
                      ['', '', '', '', '', '', '', '', '', ''],
                      ];
  let hot = new Handsontable(container, {
    data: initialData,
    colHeaders: ['Date', 'N° Compte', 'Nom', 'N° pièce', 'Libellé', 'PU ht', 'Quantité', 'Taux Tva', 'Débit', 'Crédit'],
    columns: [
      { type: 'date', dateFormat: 'DD/MM/YYYY' }, // 0 - Date
      { type: 'text' },                           // 1 - Compte
      { type: 'text' , readOnly: true },          // 2 - nom
      { type: 'text'},                            // 3 -N° Pièce
      { type: 'text' },                           // 4 - Libellé
      { type: 'numeric',                          // 5 - Prix unitaire Ht
        numericFormat: {
        pattern: '0.00', // 👉 toujours 2 décimales
        culture: 'fr-FR' // optionnel, pour gérer la virgule décimale si besoin
        }
      },                        // 4 - PU ht
      { type: 'numeric' },                        // 6 - Quantité
      { type: 'numeric',                          // 7 - Tva
        numericFormat: {
        pattern: '0.00',
        culture: 'fr-FR'
        }
       },
      { type: 'numeric',                          // 8 - Débit
        numericFormat: {
        pattern: '0.00', // 👉 toujours 2 décimales
        culture: 'fr-FR' // optionnel, pour gérer la virgule décimale si besoin
        }
      },
      { type: 'numeric',                            // 9 - Crédit
        numericFormat: {
        pattern: '0.00', // 👉 toujours 2 décimales
        culture: 'fr-FR' // optionnel, pour gérer la virgule décimale si besoin
        }
      },
    ],
    width: '100%',
    height: 'auto',
    rowHeaders: true,
    colWidths: [80, 80, 200, 58, 300, 80, 80, 80, 80, 80],
    manualColumnResize: true,
    autoWrapRow: true,
    autoWrapCol: true,
    licenseKey: 'non-commercial-and-evaluation',
  });


  hot.addHook('afterChange', function (changes, source) {
  if (internalChange || !changes || source !== 'edit') return;

  const [row, prop, oldValue, newValue] = changes[0];

  // ⛔ Ignorer les changements sur les colonnes calculées (débit, crédit)
  const colonnesTTC = ['8', '9'];
  if (colonnesTTC.includes(String(prop))) return;

  // Auto-complétion du nom du compte
  if (String(prop) === '1' && newValue !== oldValue) {
    internalChange = true;
    fetch(`/api/comptes/numero/?numero=${encodeURIComponent(newValue)}`)
      .then(response => response.json())
      .then(data => {
        if (data.nom) {
          hot.setDataAtCell(row, 2, data.nom);
        } else {
          hot.setDataAtCell(row, 2, 'Compte introuvable');
        }
        internalChange = false;
      });
    return; // Ne continue pas plus loin
  }

  // Récupération des valeurs nécessaires
  const date = hot.getDataAtCell(row, 0);
  const numeroPiece = hot.getDataAtCell(row, 3);
  const libelle = hot.getDataAtCell(row, 4);
  const pu_ht = parseFloat(hot.getDataAtCell(row, 5));
  const quantite = parseFloat(hot.getDataAtCell(row, 6));
  const taux_tva = parseFloat(hot.getDataAtCell(row, 7));

  const ligneEstComplete = date && numeroPiece && libelle && !isNaN(pu_ht) && !isNaN(quantite) && !isNaN(taux_tva);
  if (!ligneEstComplete) return;

  const montantHT = +(pu_ht * quantite).toFixed(2);
  const montantTVA = +(montantHT * taux_tva / 100).toFixed(2);
  const montantTTC = +(montantHT + montantTVA).toFixed(2);

  internalChange = true;
  if (config.sens === 'achats') {
    hot.setDataAtCell(row, 9, montantTTC); // Crédit
    hot.setDataAtCell(row, 8, '');         // Vide le débit
    col = 8;
    ajouterEcrituresAutomatiques(hot, config, row, col, date, numeroPiece, libelle, pu_ht, quantite, taux_tva, montantHT, montantTVA);
  } else if (config.sens === 'ventes') {
    hot.setDataAtCell(row, 8, montantTTC); // Débit
    hot.setDataAtCell(row, 9, '');         // Vide le crédit
    col = 9;
    ajouterEcrituresAutomatiques(hot, config, row, col, date, numeroPiece, libelle, pu_ht, quantite, taux_tva, montantHT, montantTVA);
  }

  // Ligne 4 : Ajout ligne de Saisie à la fin ##########################
    let ligneFin = hot.countRows();
    hot.alter('insert_row_below', ligneFin);
  

    internalChange = false;
});
}

function ajouterEcrituresAutomatiques(hot, config, row, col, date, numeroPiece, libelle, pu_ht, quantite, taux_tva, montantHT, montantTVA) {
      console.log('ROW', row);
      console.log('col:', col);

      // 🔸 Ligne TVA
      const ligneTVA = hot.countRows(); // ⚠️ attention ici, il compte AVANT d'ajouter la ligne
      console.log('LigneTVAbefore:', ligneTVA);


      hot.setDataAtCell(ligneTVA, 0, date);
      hot.setDataAtCell(ligneTVA, 1, config.comptesTVA[0].numero);
      hot.setDataAtCell(ligneTVA, 2, config.comptesTVA[0].nom);
      hot.setDataAtCell(ligneTVA, 3, numeroPiece);
      hot.setDataAtCell(ligneTVA, 4, libelle);
      console.log('LigneTVAafter:', ligneTVA);

      // 🔸 row : crédit (ventes) ou débit (achats)
      hot.setDataAtCell(ligneTVA, col, montantTVA);// config.sens === 'achats' ? montantTVA : ''); // Crédit
      // hot.setDataAtCell(ligneTVA, 9, config.sens === 'ventes' ? montantTVA : '');  // Débit
      // console.log('LigneTVA2:', ligneTVA);

      // ✅ Ligne charge ou produit
      const ligneVentilation = hot.countRows();
      console.log('ligneVentilation:', ligneVentilation);

      hot.setDataAtCell(ligneVentilation, 0, date);
      hot.setDataAtCell(ligneVentilation, 1, config.comptesVentilation[0].numero);
      hot.setDataAtCell(ligneVentilation, 2, config.comptesVentilation[0].nom);
      hot.setDataAtCell(ligneVentilation, 3, numeroPiece);
      hot.setDataAtCell(ligneVentilation, 4, libelle);

      // 🔸 row : crédit (ventes) ou débit (achats)
      hot.setDataAtCell(ligneVentilation, col, montantHT);// config.sens === 'achats' ? montantHT : ''); // Crédit
      // hot.setDataAtCell(row, 9, col, montantHT// config.sens === 'ventes' ? montantHT : '');  // Débit

};

// ############### Fonction tableau totaux ###################

function insertOrUpdateTotalRow(hot) {
      totalDebit = 0;
      totalCredit = 0;

      const s_rows = hot.countRows();
      for (let row = 0; row < s_rows; row++) {
        const debit = parseFloat(hot.getDataAtCell(row, 8)) || 0;
        const credit = parseFloat(hot.getDataAtCell(row, 9)) || 0;
        totalDebit += debit;
        totalCredit += credit;
      }
      return { totalDebit, totalCredit };
    }

// 🔁 Mettre à jour le tableau Totaux à chaque modification :
function updateTotalTable(hotTotals, totalDebit, totalCredit) {
  hotTotals.setDataAtCell(0, 2, totalDebit.toFixed(2));
  hotTotals.setDataAtCell(0, 3, totalCredit.toFixed(2));
  hotTotals.setDataAtCell(0, 4, (totalDebit - totalCredit).toFixed(2));
  }

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

// ############################# Bloc Page #############################

document.addEventListener('DOMContentLoaded', async function () {
  let typeJournal = document.getElementById('journal')?.value;


// ########################## Tableau saisie ###########################

  const container = document.getElementById('hot');
  if (!container) return;

  let hot = null;

  try {
      // ✅ Chargement dynamique du bon snippet
      console.log('typeJournal:', typeJournal);
      const snippetModule = await import(`/static/js/snippets/${typeJournal}.js`);
      const config = snippetModule.configJournal();


      // ✅ Appel Fonction d'initialisation du tableau avec les règles spécifiques
      // 🔄 Stocker l'instance de Handsontable retournée par initHandsontable
      hot = initHandsontable(container, config);

      } catch (error) {
        console.error(`❌ Erreur de chargement du snippet "${typeJournal}" :`, error);
      }

  // ######################## Tableau Totaux #############################
  /*
  // ######## Récupération date du jour #####################
     let options = {
      year: "numeric",
      month: "numeric",
      day: "numeric",
      };
    const dateJour = new Date();
    let today = dateJour.toLocaleDateString("fr-FR", options);
  // #########################################################


  var data1 = [
            [today, 'Totaux', '', '', '', ],
            ];
  const container_totaux = document.getElementById('hot-totals');
  if (!container_totaux) return;

  const hotTotals = new Handsontable(container_totaux, {
          colHeaders: ['Date', '', 'Débit', 'Crédit', 'Solde',],
          data: data1,
          startRows: 1,
          startCols: 6,
          width: '100%',
          height: 'auto',
          colWidths: [80, 930, 80, 80, 80],
          manualColumnResize: true,
          autoWrapRow: true,
          autoWrapCol: true,
          licenseKey: 'non-commercial-and-evaluation',
          });

  if (hot) {
      hot.addHook('afterChange', function () {
      const { totalDebit, totalCredit } = insertOrUpdateTotalRow(hot);
      updateTotalTable(hotTotals, totalDebit, totalCredit);
    });

    // ✅ Appel initial
    const { totalDebit, totalCredit } = insertOrUpdateTotalRow(hot);
    updateTotalTable(hotTotals, totalDebit, totalCredit);
  }*/


// ############################# Validation des écritures #####################################

    document.getElementById('validerEcritures').addEventListener('click', function (event) {
    event.preventDefault();
    const data = hot.getData(); // Récupère toutes les lignes du tableau Handsontable
    console.log('data:', data);

    // Filtrer les lignes vides et "TOTAL"
    const lignes = hot.getData().filter(ligne => ligne.some(cell => cell !== null && cell !== ''))
        .map(row => ({
        date: row[0],         // ✅ bien envoyer la date
        numero: row[1],
        nom: row[2],
        numero_piece: row[3],
        libelle: row[4],
        debit: row[8] || 0,
        credit: row[9] || 0
      }));
      console.log('Lignes à la validation: ', lignes)

    const urlValidation = document.getElementById('validerEcritures')?.dataset?.urlValidation;
    console.log('URLVALID:', urlValidation);
    console.log("✅ Données à envoyer :", lignes);
    fetch(urlValidation, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        // 'X-CSRFToken': getCookie('csrftoken'), // si CSRF est activé
      },
      // body: JSON.stringify({ lignes: payload }),
      body: JSON.stringify({ lignes: lignes }),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Erreur serveur');
        }
        return response.json();
      })
      .then(data => {
        alert('Écritures enregistrées avec succès ✅');
      })
      .catch(error => {
        console.error('Erreur lors de l’enregistrement :', error);
        alert('Une erreur est survenue ❌');
      });
  });

// ############## Fin document.addEventListener('DOMContentLoaded', async function () ##########
});
// #############################################################################################
/*if (['5', '6', '7'].includes(String(prop))) {
          const pu_ht = parseFloat(this.getDataAtCell(row, 5)) || 0;
          const quantite = parseFloat(this.getDataAtCell(row, 6)) || 0;
          const taux_tva = parseFloat(this.getDataAtCell(row, 7)) || 0;

          // tva != 0 sinon les lignes s'affichent avant le choix du taux et s'affichent 3 X (9 lignes au lieu de 3)

          if (pu_ht && quantite && taux_tva != 0) {
            const montantHT = +(pu_ht * quantite).toFixed(2);
            const montantTVA = +(montantHT * taux_tva / 100).toFixed(2);
            const montantTTC = montantHT + montantTVA;

            const date = this.getDataAtCell(row, 0);
            const libelle = this.getDataAtCell(row, 4);
            const numeroPiece = this.getDataAtCell(row, 3);

            this.setDataAtCell(row, 9, montantTTC); // crédit

            // ✅ Ligne TVA
            const ligneTVA = this.countRows();
            this.alter('insert_row_below', ligneTVA);
            this.setDataAtCell(ligneTVA, 0, date);
            this.setDataAtCell(ligneTVA, 1, config.comptesTVA[0].numero);
            this.setDataAtCell(ligneTVA, 2, config.comptesTVA[0].nom);
            this.setDataAtCell(ligneTVA, 3, numeroPiece);
            this.setDataAtCell(ligneTVA, 4, libelle);
            this.setDataAtCell(ligneTVA, 8, montantTVA); // débit TVA

            // ✅ Ligne charge
            const ligneCharge = this.countRows();
            this.alter('insert_row_below', ligneCharge);
            this.setDataAtCell(ligneCharge, 0, date);
            this.setDataAtCell(ligneCharge, 1, config.comptesCharges[0].numero);
            this.setDataAtCell(ligneCharge, 2, config.comptesCharges[0].nom);
            this.setDataAtCell(ligneCharge, 3, numeroPiece);
            this.setDataAtCell(ligneCharge, 4, libelle);
            this.setDataAtCell(ligneCharge, 8, montantHT); // débit charges

            // Ligne 4 : Ajout ligne de Saisie à la fin ##########################
            let ligneFin = this.countRows();
            this.alter('insert_row_below', ligneFin);
          }

          console.log('n°Piece,:', numeroPiece, 'compte:', compte, 'nom:', nom, 'libelle:', libelle, 'pu_ht:', pu_ht, 'quantite:', quantite, 'taux_tva:', taux_tva);
        */




