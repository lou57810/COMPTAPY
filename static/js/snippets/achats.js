// Journal Achats – logique spécifique
export function configJournal(hotInstance) {
  return {
    comptesTVA: [
      { numero: '44551', nom: 'TVA à décaisser' },
      { numero: '44562', nom: 'TVA sur immobilisations' },
    ],
    comptesCharges: [
      { numero: '607', nom: 'Achats de marchandises' },
      { numero: '6061', nom: 'Fournitures non stockées' },
    ],
    defaultNomTVA: 'TVA déductible',
    defaultNomCharge: 'Achats',
  };
}
