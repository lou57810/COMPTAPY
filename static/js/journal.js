// ==================== Variables globales ====================

let hot = null;
let hotTotals = null;
let internalChange = false;
let baseRowsCount = 0;  // Nombre de lignes déjà en base (lecture seule)

const entrepriseId = document.getElementById("entreprise_id")?.value;
// const csrfToken = document.getElementById("csrf_token")?.value;
function getCookie(name) {
    return document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))
        ?.split('=')[1];
}

const csrfToken = getCookie('csrftoken');

console.log("CSRFToken:", csrfToken);
console.log("entrepriseId:", entrepriseId);

if (!entrepriseId) {
  console.error("❌ entrepriseId manquant");
}

// ==================== Fonctions utilitaires ====================

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
  const options = {
    year: "numeric",
    month: "numeric",
    day: "numeric",
  };
  const dateJour = new Date();
  const today = dateJour.toLocaleDateString("fr-FR", options);

  const data1 = [[today, "Totaux", "", "", ""]];

  return new Handsontable(container_totaux, {
    colHeaders: ["Date", "", "Débit", "Crédit", "Solde"],
    data: data1,
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

// ==================== Initialisation du tableau principal ====================

function initHandsontable(container, config) {
  const initialData = [["", "", "", "", "", "", "", "", "", ""]];

  const hotInstance = new Handsontable(container, {
    data: initialData,
    colHeaders: [
      "Date",
      "N° Compte",
      "Nom",
      "Auto",
      "Libellé",
      "PU ht",
      "Quantité",
      "Taux Tva",
      "Débit",
      "Crédit",
    ],
    columns: [
      { type: "date", dateFormat: "DD/MM/YYYY" }, // 0 - Date
      { type: "text" }, // 1 - Compte
      { type: "text", readOnly: true }, // 2 - Nom
      { type: "text" }, // 3 - N° Pièce
      { type: "text" }, // 4 - Libellé
      {
        type: "numeric", // 5 - PU HT
        numericFormat: {
          pattern: "0.00",
          culture: "fr-FR",
        },
      },
      {
        type: "numeric", // 6 - Quantité
        numericFormat: {
          pattern: "0.00",
          culture: "fr-FR",
        },
      },
      {
        type: "numeric", // 7 - Taux TVA
        numericFormat: {
          pattern: "0.00",
          culture: "fr-FR",
        },
      },
      {
        type: "numeric", // 8 - Débit
        numericFormat: {
          pattern: "0.00",
          culture: "fr-FR",
        },
      },
      {
        type: "numeric", // 9 - Crédit
        numericFormat: {
          pattern: "0.00",
          culture: "fr-FR",
        },
      },
    ],
    width: "100%",
    height: "auto",
    rowHeaders: true,
    colWidths: [80, 80, 200, 58, 300, 80, 80, 80, 80, 80],
    manualColumnResize: true,
    autoWrapRow: true,
    autoWrapCol: true,
    licenseKey: "non-commercial-and-evaluation",

    // Rendre les lignes déjà en base en lecture seule
    cells: function (row, col) {
      const cellProperties = {};
      if (row < baseRowsCount) {
        cellProperties.readOnly = true;
      }
      // Colonne "Nom" toujours readOnly
      if (col === 2) {
        cellProperties.readOnly = true;
      }
      return cellProperties;
    },
  });

  // ============ Chargement des écritures existantes du journal ============

  const journalType = document.getElementById("journal_type")?.value;
  const journalUrl = document.getElementById("journal_url")?.value;

  console.log("journalUrl:", journalUrl);
  console.log("journalType:", journalType);

  if (journalType && journalUrl) {
    internalChange = true; // Bloquer les hooks pendant le chargement

    fetch(`${journalUrl}?type=${journalType}`)
      .then((response) => response.json())
      .then((json) => {
        if (json.data && json.data.length > 0) {
          hotInstance.loadData(json.data);
          baseRowsCount = hotInstance.countRows(); // Ces lignes viennent de la base → lecture seule
        } else {
          baseRowsCount = 0;
        }

        // Ajouter une ligne vide pour la saisie
        hotInstance.alter("insert_row_below", hotInstance.countRows());
      })
      .catch((error) => {
        console.error("Erreur lors du chargement du journal :", error);
      })
      .finally(() => {
        internalChange = false;
      });
  } else {
    // Pas de journal existant → une ligne vide pour commencer
    baseRowsCount = 0;
    hotInstance.alter("insert_row_below", hotInstance.countRows());
  }

  // ============ Auto-complétion & calcul TTC sur la ligne principale ============

  hotInstance.addHook("afterChange", function (changes, source) {
    if (internalChange || !changes || source !== "edit") return;

    const [row, prop, oldValue, newValue] = changes[0];

    // Ne jamais modifier les lignes existantes (lecture seule)
    if (row < baseRowsCount) return;

    // Ignorer débit / crédit dans ce hook
    const colonnesTTC = ["8", "9"];
    if (colonnesTTC.includes(String(prop))) return;

    // Auto-complétion du nom du compte (colonne 1)
    if (String(prop) === "1" && newValue !== oldValue) {
      internalChange = true;
      fetch(
        `/api/comptes/${entrepriseId}/numero/?numero=${encodeURIComponent(
          newValue
        )}`
      )
        .then((response) => response.json())
        .then((data) => {
          if (data.nom) {
            hotInstance.setDataAtCell(row, 2, data.nom);
          } else {
            hotInstance.setDataAtCell(row, 2, "Compte introuvable");
          }
        })
        .catch((error) => {
          console.error("Erreur auto-complétion compte :", error);
        })
        .finally(() => {
          internalChange = false;
        });
      return;
    }

    // Récupération des valeurs nécessaires pour calculer le TTC
    const date = hotInstance.getDataAtCell(row, 0);
    const numero = hotInstance.getDataAtCell(row, 1);
    const nom = hotInstance.getDataAtCell(row, 2);
    const numeroPiece = hotInstance.getDataAtCell(row, 3);
    // const numeroPiece = hotInstance.setDataAtCell(row, 3, "Auto");
    const libelle = hotInstance.getDataAtCell(row, 4);
    const pu_ht = parseFloat(hotInstance.getDataAtCell(row, 5));
    const quantite = parseFloat(hotInstance.getDataAtCell(row, 6));
    const taux_tva = parseFloat(hotInstance.getDataAtCell(row, 7));

    const ligneEstComplete =
      date &&
      numero &&
      nom &&
      // numeroPiece &&
      libelle &&
      !isNaN(pu_ht) &&
      !isNaN(quantite) &&
      !isNaN(taux_tva);

    if (!ligneEstComplete) return;

    const montantHT = +(pu_ht * quantite).toFixed(2);
    const montantTVA = +((montantHT * taux_tva) / 100).toFixed(2);
    const montantTTC = +(montantHT + montantTVA).toFixed(2);

    // On ne touche qu'à la ligne principale : débit/crédit selon le sens
    internalChange = true;
    if (config.sens === "achats") {
      // Achats : on crédite le compte fournisseur de la ligne principale
      hotInstance.setDataAtCell(row, 9, montantTTC); // Crédit
      hotInstance.setDataAtCell(row, 8, ""); // Débit vide
    } else if (config.sens === "ventes") {
      // Ventes : on débite le compte client de la ligne principale
      hotInstance.setDataAtCell(row, 8, montantTTC); // Débit
      hotInstance.setDataAtCell(row, 9, ""); // Crédit vide
    }
    internalChange = false;
  });

  return hotInstance;
}

// ==================== DOMContentLoaded ====================

document.addEventListener("DOMContentLoaded", async function () {
  const typeJournal = document.getElementById("journal_type")?.value;

  const container = document.getElementById("hot");
  if (!container) return;

  const container_totaux = document.getElementById("hot-totals");
  if (!container_totaux) return;

  try {
    // Chargement dynamique du snippet (achats.js, ventes.js, etc.)
    const snippetModule = await import(`/static/js/snippets/${typeJournal}.js`);
    const config = snippetModule.configJournal();

    // Initialisation des tableaux
    hot = initHandsontable(container, config);
    hotTotals = initHandsonTotaltable(container_totaux);

    // Mise à jour des totaux à chaque modification (toutes lignes confondues)
    hot.addHook("afterChange", function (changes, source) {
      if (!changes || source === "loadData" || internalChange) return;
      const { totalDebit, totalCredit } = insertOrUpdateTotalRow(hot);
      updateTotalTable(hotTotals, totalDebit, totalCredit);
    });

    // Premier calcul
    const { totalDebit, totalCredit } = insertOrUpdateTotalRow(hot);
    updateTotalTable(hotTotals, totalDebit, totalCredit);
  } catch (error) {
    console.error(`❌ Erreur de chargement du snippet "${typeJournal}" :`, error);
    return;
  }

  // ==================== Validation des écritures ====================

  const btn = document.getElementById("validerEcritures");
  console.log("btn:", btn);

  if (!btn) return;

  btn.addEventListener("click", function (event) {
    event.preventDefault();
    event.stopPropagation();

    const urlValidation = btn.dataset.urlValidation;
    if (!urlValidation) {
      console.error("URL de validation absente");
      return;
    }

    if (!hot) {
      console.error("❌ Tableau non initialisé");
      return;
    }

    const allData = hot.getData();
    console.log("data complète Hot:", allData);

    const comptesTVA = [];        // Désormais gérés côté backend
    const comptesVentilation = []; // Idem (on ne filtre plus ici par numéro)

    const lignes = [];

    // On ne prend que les lignes SAISIES (index >= baseRowsCount)
    for (let row = baseRowsCount; row < hot.countRows(); row++) {
      const ligne = hot.getDataAtRow(row);

      const hasContent = ligne.some(
        (cell) => cell !== null && cell !== "" && cell !== undefined
      );
      if (!hasContent) continue;

      const date = ligne[0];
      const numero = ligne[1];
      const nom = ligne[2];
      const numero_piece = ligne[3];
      const libelle = ligne[4];
      const pu_ht = parseFloat(ligne[5]) || 0;
      const quantite = parseFloat(ligne[6]) || 0;
      const taux = parseFloat(ligne[7]) || 0;
      const debit = parseFloat(ligne[8]) || 0;
      const credit = parseFloat(ligne[9]) || 0;

      // On n’envoie que les lignes principales saisies par l’utilisateur.
      // Le backend se charge de créer TVA + ventilation.
      lignes.push({
        date,
        numero,
        nom,
        numero_piece,
        libelle,
        pu_ht,
        quantite,
        taux,
        debit,
        credit,
      });
    }

    console.log("Lignes à la validation:", lignes);
    console.log("URLVALID:", urlValidation);
    console.log("entreprise_id:", entrepriseId);

    if (lignes.length === 0) {
      alert("Aucune ligne à enregistrer.");
      return;
    }

    fetch(urlValidation, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
       entreprise_id: entrepriseId,
       lignes: lignes }),
    })
      .then((response) => {
        if (!response.ok) {
          return response.text().then((t) => {
            throw new Error(t);
          });
        }
        return response.json();
      })
      .then((data) => {
        alert("Écritures enregistrées avec succès ✅");

        // Après validation :
        // 1) On vide la partie saisie
        // 2) On recharge proprement depuis le backend (optionnel si tu veux)

        internalChange = true;

        // On ne touche pas aux lignes existantes (baseRowsCount),
        // mais on peut choisir de recharger entièrement depuis le backend pour être 100% synchro.
        // Ici, on choisit de recharger tout le journal.

        const journalType = document.getElementById("journal_type")?.value;
        const journalUrl = document.getElementById("journal_url")?.value;

        if (journalType && journalUrl) {
          fetch(`${journalUrl}?type=${journalType}`)
            .then((response) => response.json())
            .then((json) => {
              if (json.data && json.data.length > 0) {
                hot.loadData(json.data);
                baseRowsCount = hot.countRows();
                hot.alter("insert_row_below", hot.countRows());
              } else {
                hot.loadData([["", "", "", "", "", "", "", "", "", ""]]);
                baseRowsCount = 0;
              }

              const { totalDebit, totalCredit } = insertOrUpdateTotalRow(hot);
              updateTotalTable(hotTotals, totalDebit, totalCredit);
            })
            .catch((error) => {
              console.error(
                "Erreur lors du rechargement du journal après validation :",
                error
              );
            })
            .finally(() => {
              internalChange = false;
            });
        } else {
          // Fall back : on vide juste la partie saisie
          hot.loadData([["", "", "", "", "", "", "", "", "", ""]]);
          baseRowsCount = 0;
          const { totalDebit, totalCredit } = insertOrUpdateTotalRow(hot);
          updateTotalTable(hotTotals, totalDebit, totalCredit);
          internalChange = false;
        }
      })
      .catch((error) => {
        console.error("Erreur serveur réelle :", error);
        alert("Erreur lors de l’enregistrement ❌");
      });
  });
});
