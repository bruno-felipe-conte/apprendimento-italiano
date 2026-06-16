const fs = require('fs');

const file = 'data/dialogi.json';
const data = JSON.parse(fs.readFileSync(file, 'utf8'));

// Fix dial_001
const dial_1 = data.dialogi[0];
if (dial_1.id === 'dial_001') {
  dial_1.turni.forEach(t => {
    if (t.id === 4 && !t.alternativas) {
      t.alternativas = [
        "Grazie mille.",
        "Dov'è il bagno?",
        "Voglio il conto.",
        "Non mi piace."
      ];
      t.resposta_correta = 0;
    }
  });
}

// Fix dial_002
const dial_2 = data.dialogi[1];
if (dial_2.id === 'dial_002') {
  dial_2.turni.forEach(t => {
    if (t.id === 4 && t.alternativas) {
      t.alternativas = [
        "No, non ho allergie. Grazie.",
        "Sì, sono allergico alla penicillina.",
        "Non lo so.",
        "Ho molte allergie."
      ];
    }
  });
}

// Fix dial_003
const dial_3 = data.dialogi[2];
if (dial_3.id === 'dial_003') {
  dial_3.turni = [
    {
      "id": 1,
      "personaggio": "Addetta",
      "frase": "Buongiorno! Il passaporto e il biglietto, per favore.",
      "traducao": "Bom dia! O passaporte e a passagem, por favor.",
      "audio_ipa": ""
    },
    {
      "id": 2,
      "personaggio": "Tu",
      "frase": "Buongiorno. Ecco i miei documenti.",
      "traducao": "Bom dia. Aqui estão meus documentos.",
      "audio_ipa": "",
      "alternativas": [
        "Buongiorno. Ecco i miei documenti.",
        "Non voglio niente.",
        "Dov'è il treno?",
        "Non so parlare italiano."
      ],
      "resposta_correta": 0
    },
    {
      "id": 3,
      "personaggio": "Addetta",
      "frase": "Perfetto. Ha dei bagagli da stivare?",
      "traducao": "Perfeito. Você tem bagagens para despachar?",
      "audio_ipa": ""
    },
    {
      "id": 4,
      "personaggio": "Tu",
      "frase": "Sì, ho questa valigia grande e un bagaglio a mano.",
      "traducao": "Sim, tenho esta mala grande e uma bagagem de mão.",
      "audio_ipa": "",
      "alternativas": [
        "Sì, ho questa valigia grande e un bagaglio a mano.",
        "No, odio viaggiare.",
        "Dove si trova il bagno?",
        "È troppo caro."
      ],
      "resposta_correta": 0
    },
    {
      "id": 5,
      "personaggio": "Addetta",
      "frase": "Va benissimo. La metta sul nastro, per favore. Il suo volo partirà dal gate 5.",
      "traducao": "Tudo bem. Coloque na esteira, por favor. Seu voo partirá do portão 5.",
      "audio_ipa": ""
    },
    {
      "id": 6,
      "personaggio": "Tu",
      "frase": "Grazie mille. A che ora è l'imbarco?",
      "traducao": "Muito obrigado. A que horas é o embarque?",
      "audio_ipa": "",
      "alternativas": [
        "Grazie mille. A che ora è l'imbarco?",
        "Non voglio pagare.",
        "Non mi piace.",
        "Arrivederci!"
      ],
      "resposta_correta": 0
    }
  ];
}

fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
console.log('Success');
