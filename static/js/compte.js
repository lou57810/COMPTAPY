const container = document.getElementById('journal-display');

const hot = new Handsontable(container, {
  data: journalData,
  colHeaders: ['Date', 'Libellé', 'Débit', 'Crédit'],
  columns: [
    { type: 'text', readOnly: true },
    { type: 'text', readOnly: true },
    { type: 'numeric', numericFormat: { pattern: '0.00' }, readOnly: true },
    { type: 'numeric', numericFormat: { pattern: '0.00' }, readOnly: true },
  ],
  licenseKey: 'non-commercial-and-evaluation',
});
