// Journal Achats – logique spécifique
export function configJournal() {
  return {
    comptesTVA: [{ numero: '445660', nom: 'TVA déductible' }],
    comptesVentilation: [{ numero: '606100', nom: 'Achats Marchandises' }],
    sens: 'achats',
  };
}
