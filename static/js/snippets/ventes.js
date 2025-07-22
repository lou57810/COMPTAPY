// Journal Achats – logique spécifique
export function configJournal(hotInstance) {
  return {
    comptesTVA: [
      { numero: '44571', nom: 'TVA collectée' },
      { numero: '44562', nom: 'TVA sur immobilisations' },
    ],
    comptesCharges: [
      { numero: '701', nom: 'Ventes de produits finis' },
      { numero: '7012', nom: 'Produits finis (ou groupe) B' },
    ],
    defaultNomTVA: 'TVA déductible',
    defaultNomCharge: 'Ventes',
  };
}
