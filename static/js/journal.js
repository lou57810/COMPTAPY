// journal.js (doit être chargé comme type="module")
// Initialisation portée globale

let hot = null;
let hotTotals = null;
let ligneFin = 0;
let row = 0;
let internalChange = false;
let col = 0;
const entrepriseId = document.getElementById("entreprise_id")?.value;
console.log('entrepriseId:', entrepriseId)
if (!entrepriseId) {
  console.error("❌ entrepriseId manquant");
  //return;
}



// ✅ ################ Fonction d'initialisation du tableau Handsontable #######################
function initHandsontable(container, config) {

  // let cell = 0;

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
      fetch(`/api/comptes/${entrepriseId}/numero/?numero=${encodeURIComponent(newValue)}`)
      // fetch(`/api/comptes/numero/?numero=${encodeURIComponent(newValue)}`)
      // fetch(`/api/comptes/numero/?entreprise=${entrepriseId}&numero=${encodeURIComponent(newValue)}`)
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
      ligneFin = hot.countRows();
      hot.alter('insert_row_below', ligneFin);
      internalChange = false;
  });

  return hot;
}

function ajouterEcrituresAutomatiques(hot, config, row, col, date, numeroPiece, libelle, pu_ht, quantite, taux_tva, montantHT, montantTVA) {

      // 🔸 Ligne TVA
      const ligneTVA = hot.countRows(); // ⚠️ attention ici, il compte AVANT d'ajouter la ligne

      hot.setDataAtCell(ligneTVA, 0, date);
      hot.setDataAtCell(ligneTVA, 1, config.comptesTVA[0].numero);
      hot.setDataAtCell(ligneTVA, 2, config.comptesTVA[0].nom);
      hot.setDataAtCell(ligneTVA, 3, numeroPiece);
      hot.setDataAtCell(ligneTVA, 4, libelle);

      hot.setDataAtCell(ligneTVA, col, montantTVA);

      // ✅ Ligne charge ou produit
      const ligneVentilation = hot.countRows();

      hot.setDataAtCell(ligneVentilation, 0, date);
      hot.setDataAtCell(ligneVentilation, 1, config.comptesVentilation[0].numero);
      hot.setDataAtCell(ligneVentilation, 2, config.comptesVentilation[0].nom);
      hot.setDataAtCell(ligneVentilation, 3, numeroPiece);
      hot.setDataAtCell(ligneVentilation, 4, libelle);

      hot.setDataAtCell(ligneVentilation, col, montantHT);
};

// ############### Fonction tableau totaux ###################
// 🔁 Mettre à jour le tableau Totaux à chaque modification :
function updateTotalTable(hotTotals, totalDebit, totalCredit) {
  hotTotals.setDataAtCell(0, 2, totalDebit.toFixed(2));
  hotTotals.setDataAtCell(0, 3, totalCredit.toFixed(2));
  hotTotals.setDataAtCell(0, 4, (totalDebit - totalCredit).toFixed(2));
  }

function insertOrUpdateTotalRow(hot) {
  let totalDebit = 0;
  let totalCredit = 0;
  const s_rows = hot.countRows();
  for (let row = 0; row < s_rows; row++) {

    const debit = parseFloat(hot.getDataAtCell(row, 8)) || 0;
    const credit = parseFloat(hot.getDataAtCell(row, 9)) || 0;
    totalDebit += debit;
    totalCredit += credit;
    }
      return { totalDebit, totalCredit };
  }

function initHandsonTotaltable(container_totaux) {
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
    return new Handsontable(container_totaux, {
          colHeaders: ['Date', '', 'Débit', 'Crédit', 'Solde',],
          data: data1,
          startRows: 1,
          startCols: 6,
          width: '100%',
          height: 'auto',
          colWidths: [80, 850, 80, 80, 80],
          manualColumnResize: true,
          autoWrapRow: true,
          autoWrapCol: true,
          licenseKey: 'non-commercial-and-evaluation',
          });
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

  const container_totaux = document.getElementById('hot-totals');
    if (!container_totaux) return;

  try {
      // ✅ Chargement dynamique du bon snippet
      const snippetModule = await import(`/static/js/snippets/${typeJournal}.js`);
      const config = snippetModule.configJournal();


      // ✅ Appel Fonction d'initialisation du tableau avec les règles spécifiques
      // 🔄 Stocker l'instance de Handsontable retournée par initHandsontable
      hot = initHandsontable(container, config);
      hotTotals = initHandsonTotaltable(container_totaux);


      // ✅ Hook sur la table principale seulement
      hot.addHook('afterChange', function (changes, source) {
      if (source === 'loadData') return; // éviter boucle
      const { totalDebit, totalCredit } = insertOrUpdateTotalRow(hot);
      updateTotalTable(hotTotals, totalDebit, totalCredit);
      });

      // ✅ Premier calcul
      const { totalDebit, totalCredit } = insertOrUpdateTotalRow(hot);
      updateTotalTable(hotTotals, totalDebit, totalCredit);

      } catch (error) {
        console.error(`❌ Erreur de chargement du snippet "${typeJournal}" :`, error);
      }

});

// ############################# Validation des écritures #####################################

    document.getElementById('validerEcritures').addEventListener('click', function (event) {
    event.preventDefault();

    if (!hot) {
    console.error('❌ Tableau non initialisé');
    return;
  }

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


