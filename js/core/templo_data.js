// ============================================================
// js/core/templo_data.js — Temple Metadata & Constants (ARC-02)
// ============================================================

const AppTemploData = {
  // Temple gradient palettes (index = temple number, 1-based)
  TEMPLO_CORES: [
    null,
    'linear-gradient(135deg, #9B2335, #6B1525)',   // 1  Roma
    'linear-gradient(135deg, #1A5276, #154360)',   // 2  Venezia
    'linear-gradient(135deg, #1E8449, #145A32)',   // 3  Firenze
    'linear-gradient(135deg, #7D3C98, #5B2C6F)',   // 4  Napoli
    'linear-gradient(135deg, #CA6F1E, #9C4A1A)',   // 5  Milano
    'linear-gradient(135deg, #2E86C1, #1A5276)',   // 6  Bologna
    'linear-gradient(135deg, #C0392B, #922B21)',   // 7  Torino
    'linear-gradient(135deg, #117A65, #0E6655)',   // 8  Palermo
    'linear-gradient(135deg, #6E2F8F, #512E6D)',   // 9  Bari
    'linear-gradient(135deg, #B7950B, #9A7D0A)',   // 10 Siena
    'linear-gradient(135deg, #2C3E50, #1A252F)',   // 11
    'linear-gradient(135deg, #1ABC9C, #148F77)',   // 12
    'linear-gradient(135deg, #E74C3C, #CB4335)',   // 13
    'linear-gradient(135deg, #3498DB, #2980B9)',   // 14
    'linear-gradient(135deg, #27AE60, #1E8449)',   // 15
    'linear-gradient(135deg, #F39C12, #D68910)',   // 16
    'linear-gradient(135deg, #8E44AD, #7D3C98)',   // 17
    'linear-gradient(135deg, #16A085, #148F77)',   // 18
    'linear-gradient(135deg, #D35400, #BA4A00)',   // 19
    'linear-gradient(135deg, #2980B9, #1A5276)',   // 20
    'linear-gradient(135deg, #C0392B, #9B2335)',   // 21
    'linear-gradient(135deg, #27AE60, #196F3D)',   // 22
    'linear-gradient(135deg, #8E44AD, #512E6D)',   // 23
    'linear-gradient(135deg, #E67E22, #CA6F1E)',   // 24
    'linear-gradient(135deg, #2E86C1, #154360)',   // 25
    'linear-gradient(135deg, #6C3483, #512E6D)',   // 26
    'linear-gradient(135deg, #1A5276, #0E3460)',   // 27
    'linear-gradient(135deg, #117A65, #0B5345)',   // 28
    'linear-gradient(135deg, #9B59B6, #7D3C98)',   // 29
    'linear-gradient(135deg, #B7950B, #7D6608)',   // 30
    'linear-gradient(135deg, #1F618D, #154360)',   // 31
    'linear-gradient(135deg, #922B21, #7B241C)',   // 32
    'linear-gradient(135deg, #1E8449, #196F3D)',   // 33
    'linear-gradient(135deg, #CA6F1E, #A04000)',   // 34
    'linear-gradient(135deg, #148F77, #0E6655)',   // 35
    'linear-gradient(135deg, #2980B9, #1F618D)',   // 36
    'linear-gradient(135deg, #6D4C41, #4E342E)',   // 37
    'linear-gradient(135deg, #455A64, #263238)',   // 38
    'linear-gradient(135deg, #283593, #1A237E)',   // 39
    'linear-gradient(135deg, #00695C, #004D40)',   // 40
    'linear-gradient(135deg, #4A148C, #38006B)',   // 41
    'linear-gradient(135deg, #BF360C, #870000)',   // 42
    'linear-gradient(135deg, #827717, #5D4037)',   // 43
    'linear-gradient(135deg, #1B5E20, #003300)',   // 44
    'linear-gradient(135deg, #0D47A1, #002171)',   // 45
    'linear-gradient(135deg, #880E4F, #560027)',   // 46
    'linear-gradient(135deg, #E65100, #BF360C)',   // 47
    'linear-gradient(135deg, #37474F, #1C313A)',   // 48
    'linear-gradient(135deg, #4E342E, #3E2723)',   // 49
    'linear-gradient(135deg, #9B2335, #4A0A15)',   // 50
    'linear-gradient(135deg, #D35400, #962D00)',   // 51 La Cucina Regionale
  ],

  // Temple names (index = templo number)
  TEMPLO_NOMES: [
    null,
    'Le Fondamenta',       // 1 Roma
    'Il Cuore',            // 2 Venezia
    'Il Viaggio',          // 3 Firenze
    'Il Gusto',            // 4 Napoli
    'Il Tempo',            // 5 Milano
    'La Grammatica',       // 6 Bologna
    'La Conversazione',    // 7 Torino
    'La Cultura',          // 8 Palermo
    'Il Lavoro',           // 9 Bari
    'La Letteratura',      // 10 Siena
  ],

  // Minimum level to unlock each temple (matches Progressao.TEMPLO_NIVEL)
  TEMPLO_NIVEL_MINIMO: {
    1:1,  2:2,  3:4,  4:6,  5:8,  6:10, 7:13, 8:15, 9:17, 10:20,
    36:2, // T36 I Social Media e Internet (A1/A2)
    11:2, 12:2, 13:2, 14:2, 15:2, 17:2, 18:2, 19:2,
    22:2, 23:2, 25:2, 28:2, 33:2, 34:2,
    16:4, 20:4, 21:4, 24:4, 29:4, 32:4, 35:4, 51:4,
    26:7, 27:7, 30:7, 31:7, 37:7, 38:7, 43:7, 46:7,
    39:11, 40:11, 42:11, 44:11, 45:11,
    41:15, 47:15, 48:15, 49:15, 50:15,
  },

  // Italian descriptions per temple (difficulty proportional to level)
  TEMPLO_DESC: [
    null,
    'Roma è grande e bella. Qui inizi a parlare italiano. Impari "buongiorno", "grazie", "per favore" — i primi passi. Con queste parole puoi salutare, contare e presentarti. Le fondamenta di tutto.',
    'Venezia è unica al mondo. In questo tempio parli della famiglia e della casa: chi è tua madre, come si chiama tuo fratello, dove abiti. Impari a descrivere le persone e i luoghi della tua vita quotidiana.',
    'Firenze è la culla del Rinascimento. Qui trovi tutto il vocabolario per viaggiare in Italia: la stazione, il treno, l\'albergo, le indicazioni stradali. Questo tempio ti prepara per ogni avventura in terra italiana.',
    'Napoli ha inventato la pizza e ha insegnato al mondo come mangiare con passione. In questo tempio entri nella cucina italiana: ingredienti, piatti tipici, abitudini a tavola. Imparare a parlare di cibo è imparare la cultura italiana.',
    'Milano è veloce, precisa, sempre in movimento. Questo tempio ti insegna a gestire il tempo in italiano — le ore, gli appuntamenti, le stagioni — e a descrivere la tua routine quotidiana con naturalezza e precisione.',
    'Bologna, sede della più antica università d\'Europa, è il luogo ideale per studiare la struttura della lingua. Qui affronti il congiuntivo, i pronomi relativi, le costruzioni implicite. Non solo regole: impari a pensare in italiano.',
    'Torino, città sobria e intellettuale, è dove si impara a conversare con stile. In questo tempio esplori l\'argomentazione, il dibattito e la cortesia formale. Come si difende un\'opinione? Come si negozia con eleganza? L\'italiano fluente ti aspetta.',
    'Palermo porta i segni di tutte le civiltà che l\'hanno abitata: greci, arabi, normanni. Questo tempio ti apre al patrimonio culturale dell\'Italia — l\'arte, la storia, le tradizioni regionali di un popolo complesso e affascinante.',
    'Bari, porta d\'Italia verso il Mediterraneo, è una città che lavora. Questo tempio ti fornisce il vocabolario professionale: curriculum, riunioni, negoziazioni. L\'italiano del trabalho richiede precisione e rispetto delle forme.',
    'Siena custodisce il volgare illustre, la lingua di Dante. Nel decimo tempio raggiungi la vetta: il linguaggio della letteratura, della filosofia e dell\'espressione artistica. Le parole non comunicano soltanto — evocano, suggeriscono, trasformano.',
  ]
};

if (typeof globalThis !== 'undefined') {
  globalThis.AppTemploData = AppTemploData;
}
if (typeof window !== 'undefined') {
  window.AppTemploData = AppTemploData;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = AppTemploData;
}
