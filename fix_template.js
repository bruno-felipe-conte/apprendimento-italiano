const fs = require('fs');
const file = 'data/dialogi.json';
const data = JSON.parse(fs.readFileSync(file, 'utf8'));

function applyTemplate(dial) {
  const v0 = dial.vocabulario_chave[0];
  const v1 = dial.vocabulario_chave[1];
  const v2 = dial.vocabulario_chave[2];
  
  let p1 = "Personaggio";
  if (dial.turni && dial.turni[0] && dial.turni[0].personaggio) {
    p1 = dial.turni[0].personaggio;
  }
  
  dial.turni = [
    {
      "id": 1,
      "personaggio": p1,
      "frase": "Buongiorno, come posso aiutarla?",
      "traducao": "Bom dia, come posso ajudá-lo(a)?",
      "audio_ipa": ""
    },
    {
      "id": 2,
      "personaggio": "Tu",
      "frase": "Salve, avrei bisogno di aiuto per " + v0 + ".",
      "traducao": "Olá, eu precisaria de ajuda para " + v0 + ".",
      "audio_ipa": "",
      "alternativas": [
        "Salve, avrei bisogno di aiuto per " + v0 + ".",
        "Non voglio niente.",
        "Arrivederci.",
        "Non so parlare italiano."
      ],
      "resposta_correta": 0
    },
    {
      "id": 3,
      "personaggio": p1,
      "frase": "Certamente. Ecco qui il suo " + v0 + ". Le serve anche " + v1 + "?",
      "traducao": "Certamente. Aqui está o seu " + v0 + ". Precisa também de " + v1 + "?",
      "audio_ipa": ""
    },
    {
      "id": 4,
      "personaggio": "Tu",
      "frase": "Sì, grazie. E vorrei anche " + v2 + ".",
      "traducao": "Sim, obrigado. E gostaria também de " + v2 + ".",
      "audio_ipa": "",
      "alternativas": [
        "Sì, grazie. E vorrei anche " + v2 + ".",
        "No, odio questa cosa.",
        "Dove si trova il bagno?",
        "È troppo caro."
      ],
      "resposta_correta": 0
    },
    {
      "id": 5,
      "personaggio": p1,
      "frase": "Va benissimo. Saranno 15 euro in totale.",
      "traducao": "Tudo bem. Serão 15 euros no total.",
      "audio_ipa": ""
    },
    {
      "id": 6,
      "personaggio": "Tu",
      "frase": "Ecco a lei. Arrivederci!",
      "traducao": "Aqui está. Até logo!",
      "audio_ipa": "",
      "alternativas": [
        "Ecco a lei. Arrivederci!",
        "Non voglio pagare.",
        "Scappi via!",
        "Non mi piace."
      ],
      "resposta_correta": 0
    }
  ];
}

applyTemplate(data.dialogi[0]);
applyTemplate(data.dialogi[1]);
applyTemplate(data.dialogi[2]);

fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf8');
console.log('Template applied to first 3 dialogs');
