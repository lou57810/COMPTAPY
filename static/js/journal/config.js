// static/js/journal/config.js

export const colHeaders = [
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
];


export const columnsConfig = [
    { type: "date", dateFormat: "DD/MM/YYYY" }, // 0
    { type: "text" },                           // 1
    { type: "text" },                           // 2
    { type: "text" },                           // 3
    { type: "text" },                           // 4
    { type: "numeric", numericFormat: { pattern: "0.00", culture: "fr-FR" } }, // 5
    { type: "numeric", numericFormat: { pattern: "0.00", culture: "fr-FR" } }, // 6
    { type: "numeric", numericFormat: { pattern: "0.00", culture: "fr-FR" } }, // 7
    { type: "numeric", numericFormat: { pattern: "0.00", culture: "fr-FR" } }, // 8
    { type: "numeric", numericFormat: { pattern: "0.00", culture: "fr-FR" } }, // 9
];


export const hotSettings = {
    width: "100%",
    height: "auto",
    rowHeaders: true,
    colWidths: [80, 80, 200, 58, 300, 80, 80, 80, 80, 80],
    manualColumnResize: true,
    autoWrapRow: true,
    autoWrapCol: true,
    licenseKey: "non-commercial-and-evaluation",
};

