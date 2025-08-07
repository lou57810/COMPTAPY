// Journal Achats – logique spécifique
export function configJournal() {
  return {
    // compteContrepartie: { numero: '401000', nom: 'Fournisseur' },
    comptesTVA: [{ numero: '445660', nom: 'TVA déductible' }],
    comptesVentilation: [{ numero: '606100', nom: 'Achats Marchandises' }],
    sens: 'achats',
  };
}
