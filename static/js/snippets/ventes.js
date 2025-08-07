// Journal Achats – logique spécifique
export function configJournal() {
  return {
    // compteContrepartie: { numero: '411000', nom: 'Client' },
    comptesTVA: [{ numero: '445700', nom: 'TVA collectée' }],
    comptesVentilation: [{ numero: '706000', nom: 'Ventes Marchandises' }],
    sens: 'ventes',
  };
}
