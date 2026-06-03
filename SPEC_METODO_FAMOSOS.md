# SPEC — Método dos Famosos: 5 Novas Features
## App: Italiano Autentico | Repo: bruno-felipe-conte/apprendimento-italiano

Inspirado em como atores, jogadores, cantores e lutadores aprendem idiomas.
Cada feature mapeia um método real documentado.

---

## VISÃO GERAL DAS 5 FEATURES

| # | Feature | Inspiração | Prioridade | Esforço |
|---|---------|-----------|-----------|---------|
| 1 | **Modo Diálogo** | Atores (prática situacional) | Alta | Médio |
| 2 | **Meta com Prazo** | Pressão de deadline | Alta | Pequeno |
| 3 | **Modo Canzone** | Cantores (letra com lacunas) | Média | Médio |
| 4 | **Modo Imitação** | Imitar fonética em voz alta | Média | Pequeno |
| 5 | **Vocabulário por Contexto** | Cenas de filmes/séries | Baixa | Grande |

---

## O QUE JÁ EXISTE NO APP (não reimplementar)

- `App.pronunciar(texto)` em `js/core.js` — TTS italiano via Web Speech API + ResponsiveVoice fallback
- `App.ganharXP(n)` / `Progressao.ganhar(n)` — sistema de XP com streak e level-up
- `App.notificar(msg, tipo)` — toasts de notificação (sucesso/erro/alerta)
- `App.estado.progresso` — objeto de progresso salvo em localStorage
- `App.salvarProgresso()` — persiste progresso
- `App.navegar(secao)` — navegação entre abas
- Sistema de conquistas em `js/conquistas.js`
- Bottom nav mobile com 5 abas: templi, flashcard, quiz, grammatica, profilo

---

## FEATURE 1 — MODO DIÁLOGO (Cenários de Conversação)

### Conceito
Atores praticam situações reais antes de precisar delas. O usuário escolhe um cenário (restaurante, aeroporto, farmácia…), lê o diálogo completo com áudio, depois pratica respondendo às falas do personagem.

### Estrutura de Dados

**Criar `data/dialogi.json`:**
```json
{
  "dialogi": [
    {
      "id": "dial_001",
      "titulo": "Al Ristorante",
      "icone": "🍽️",
      "nivel": "A1",
      "contexto": "Você entra em um restaurante italiano para jantar.",
      "turni": [
        {
          "id": 1,
          "personaggio": "Cameriere",
          "frase": "Buonasera! Avete prenotato?",
          "traducao": "Boa noite! Vocês têm reserva?",
          "audio_ipa": "/bwɔnaˈseːra"
        },
        {
          "id": 2,
          "personaggio": "Tu",
          "frase": "No, non abbiamo prenotato. C'è un tavolo per due?",
          "traducao": "Não, não temos reserva. Tem mesa para dois?",
          "audio_ipa": "",
          "alternativas": [
            "No, non abbiamo prenotato. C'è un tavolo per due?",
            "Sì, abbiamo prenotato. Il nome è Rossi.",
            "Voglio un tavolo, per favore.",
            "Non capisco, scusi."
          ],
          "resposta_correta": 0
        },
        {
          "id": 3,
          "personaggio": "Cameriere",
          "frase": "Certo! Seguitemi, prego.",
          "traducao": "Claro! Sigam-me, por favor.",
          "audio_ipa": ""
        },
        {
          "id": 4,
          "personaggio": "Tu",
          "frase": "Grazie mille.",
          "traducao": "Muito obrigado.",
          "audio_ipa": ""
        },
        {
          "id": 5,
          "personaggio": "Cameriere",
          "frase": "Ecco il menù. Volete qualcosa da bere?",
          "traducao": "Aqui está o cardápio. Querem algo para beber?",
          "audio_ipa": ""
        },
        {
          "id": 6,
          "personaggio": "Tu",
          "frase": "Un'acqua minerale naturale e un bicchiere di vino rosso.",
          "traducao": "Uma água mineral sem gás e uma taça de vinho tinto.",
          "audio_ipa": "",
          "alternativas": [
            "Un'acqua minerale naturale e un bicchiere di vino rosso.",
            "Solo acqua, grazie.",
            "Una birra grande, per favore.",
            "Non ho sete, grazie."
          ],
          "resposta_correta": 0
        }
      ],
      "vocabulario_chave": ["prenotare", "tavolo", "menù", "cameriere", "conto"],
      "xp_recompensa": 50
    },
    {
      "id": "dial_002",
      "titulo": "In Farmacia",
      "icone": "💊",
      "nivel": "A2",
      "contexto": "Você está com dor de cabeça e vai à farmácia.",
      "turni": [
        {"id":1,"personaggio":"Farmacista","frase":"Buongiorno, posso aiutarla?","traducao":"Bom dia, posso ajudá-lo?","audio_ipa":""},
        {"id":2,"personaggio":"Tu","frase":"Sì, ho mal di testa. Ha qualcosa per il dolore?","traducao":"Sim, estou com dor de cabeça. Tem algo para a dor?","audio_ipa":"","alternativas":["Sì, ho mal di testa. Ha qualcosa per il dolore?","Ho la febbre alta.","Cerco un farmaco per la tosse.","Non sto bene, ho bisogno di aiuto."],"resposta_correta":0},
        {"id":3,"personaggio":"Farmacista","frase":"Certo. Ha allergie a qualche farmaco?","traducao":"Claro. Você tem alergia a algum remédio?","audio_ipa":""},
        {"id":4,"personaggio":"Tu","frase":"No, non ho allergie. Grazie.","traducao":"Não, não tenho alergias. Obrigado.","audio_ipa":"","alternativas":["No, non ho allergie. Grazie.","Sì, sono allergico alla penicillina.","Non lo so.","Ho allergie molte."],"resposta_correta":0},
        {"id":5,"personaggio":"Farmacista","frase":"Prenda due compresse ogni otto ore dopo i pasti.","traducao":"Tome dois comprimidos a cada oito horas após as refeições.","audio_ipa":""},
        {"id":6,"personaggio":"Tu","frase":"Capito. Quanto costano?","traducao":"Entendi. Quanto custam?","audio_ipa":"","alternativas":["Capito. Quanto costano?","Va bene, arrivederci.","Non capisco.","Posso pagare con carta?"],"resposta_correta":0}
      ],
      "vocabulario_chave":["mal di testa","farmaco","allergia","compressa","pasto"],
      "xp_recompensa":50
    },
    {
      "id": "dial_003",
      "titulo": "All'Aeroporto",
      "icone": "✈️",
      "nivel": "A2",
      "contexto": "Você está no aeroporto e precisa fazer o check-in.",
      "turni": [
        {"id":1,"personaggio":"Addetta","frase":"Buongiorno! Posso vedere il suo passaporto e il biglietto?","traducao":"Bom dia! Posso ver seu passaporte e bilhete?","audio_ipa":""},
        {"id":2,"personaggio":"Tu","frase":"Ecco il passaporto e il mio biglietto elettronico.","traducao":"Aqui está o passaporte e meu bilhete eletrônico.","audio_ipa":"","alternativas":["Ecco il passaporto e il mio biglietto elettronico.","Non ho il passaporto con me.","Aspetti un momento.","Ho perso il biglietto."],"resposta_correta":0},
        {"id":3,"personaggio":"Addetta","frase":"Ha bagagli da imbarcare?","traducao":"Tem bagagens para despachar?","audio_ipa":""},
        {"id":4,"personaggio":"Tu","frase":"Sì, una valigia grande e uno zaino come bagaglio a mano.","traducao":"Sim, uma mala grande e uma mochila como bagagem de mão.","audio_ipa":"","alternativas":["Sì, una valigia grande e uno zaino come bagaglio a mano.","No, solo bagaglio a mano.","Ho tre valigie.","Non lo so."],"resposta_correta":0},
        {"id":5,"personaggio":"Addetta","frase":"Vuole il posto al finestrino o al corridoio?","traducao":"Quer assento na janela ou no corredor?","audio_ipa":""},
        {"id":6,"personaggio":"Tu","frase":"Al finestrino, se possibile.","traducao":"Na janela, se possível.","audio_ipa":"","alternativas":["Al finestrino, se possibile.","Non importa.","Al corridoio, grazie.","Dove vuole lei."],"resposta_correta":0}
      ],
      "vocabulario_chave":["passaporto","biglietto","valigia","bagaglio","finestrino","corridoio"],
      "xp_recompensa":50
    },
    {
      "id": "dial_004",
      "titulo": "Dal Medico",
      "icone": "🏥",
      "nivel": "B1",
      "contexto": "Você não está se sentindo bem e vai ao médico.",
      "turni": [
        {"id":1,"personaggio":"Medico","frase":"Buongiorno. Come si sente oggi?","traducao":"Bom dia. Como se sente hoje?","audio_ipa":""},
        {"id":2,"personaggio":"Tu","frase":"Non mi sento bene. Ho febbre alta e mal di gola da tre giorni.","traducao":"Não me sinto bem. Tenho febre alta e dor de garganta há três dias.","audio_ipa":"","alternativas":["Non mi sento bene. Ho febbre alta e mal di gola da tre giorni.","Sto benissimo, grazie.","Ho solo un po' di tosse.","Non so descrivere i sintomi."],"resposta_correta":0},
        {"id":3,"personaggio":"Medico","frase":"Apra la bocca e dica 'aaah'. Ha anche mal di testa?","traducao":"Abra a boca e diga 'aaah'. Também tem dor de cabeça?","audio_ipa":""},
        {"id":4,"personaggio":"Tu","frase":"Sì, soprattutto al mattino. E mi sento molto stanco.","traducao":"Sim, principalmente de manhã. E me sinto muito cansado.","audio_ipa":"","alternativas":["Sì, soprattutto al mattino. E mi sento molto stanco.","No, nessun mal di testa.","Solo un pochino.","Non ricordo."],"resposta_correta":0},
        {"id":5,"personaggio":"Medico","frase":"Sembra un'influenza. Le prescrivo un antibiotico e del riposo.","traducao":"Parece uma gripe. Vou prescrever um antibiótico e repouso.","audio_ipa":""},
        {"id":6,"personaggio":"Tu","frase":"Grazie dottore. Per quanto tempo devo prendere l'antibiotico?","traducao":"Obrigado doutor. Por quanto tempo devo tomar o antibiótico?","audio_ipa":"","alternativas":["Grazie dottore. Per quanto tempo devo prendere l'antibiotico?","Va bene, arrivederci.","Non prendo medicine.","Quanto costa la visita?"],"resposta_correta":0}
      ],
      "vocabulario_chave":["febbre","mal di gola","sintomi","antibiotico","riposo","ricetta"],
      "xp_recompensa":60
    },
    {
      "id": "dial_005",
      "titulo": "In Banca",
      "icone": "🏦",
      "nivel": "B1",
      "contexto": "Você precisa abrir uma conta bancária na Itália.",
      "turni": [
        {"id":1,"personaggio":"Impiegato","frase":"Buongiorno, come posso aiutarla?","traducao":"Bom dia, como posso ajudá-lo?","audio_ipa":""},
        {"id":2,"personaggio":"Tu","frase":"Vorrei aprire un conto corrente. Quali documenti servono?","traducao":"Gostaria de abrir uma conta corrente. Quais documentos são necessários?","audio_ipa":"","alternativas":["Vorrei aprire un conto corrente. Quali documenti servono?","Voglio fare un prelievo.","Ho perso la carta di credito.","Devo fare un bonifico."],"resposta_correta":0},
        {"id":3,"personaggio":"Impiegato","frase":"Servono il passaporto, il codice fiscale e una prova di residenza.","traducao":"São necessários passaporte, código fiscal e comprovante de residência.","audio_ipa":""},
        {"id":4,"personaggio":"Tu","frase":"Ho tutti i documenti con me. Posso procedere subito?","traducao":"Tenho todos os documentos comigo. Posso proceder agora?","audio_ipa":"","alternativas":["Ho tutti i documenti con me. Posso procedere subito?","Non ho il codice fiscale.","Torno domani con i documenti.","Qual è la vostra commissione?"],"resposta_correta":0},
        {"id":5,"personaggio":"Impiegato","frase":"Certamente. La carta di debito arriverà entro una settimana.","traducao":"Certamente. O cartão de débito chegará em uma semana.","audio_ipa":""},
        {"id":6,"personaggio":"Tu","frase":"Perfetto. Offrite anche il servizio di internet banking?","traducao":"Perfeito. Vocês também oferecem serviço de internet banking?","audio_ipa":"","alternativas":["Perfetto. Offrite anche il servizio di internet banking?","Quanto tempo ci vuole?","Non mi interessa.","Va bene, grazie."],"resposta_correta":0}
      ],
      "vocabulario_chave":["conto corrente","codice fiscale","residenza","carta di debito","bonifico"],
      "xp_recompensa":60
    },
    {
      "id": "dial_006",
      "titulo": "Al Mercato",
      "icone": "🛒",
      "nivel": "A1",
      "contexto": "Você está num mercado de rua comprando frutas e legumes.",
      "turni": [
        {"id":1,"personaggio":"Venditore","frase":"Prego! Cosa desidera?","traducao":"Pois não! O que deseja?","audio_ipa":""},
        {"id":2,"personaggio":"Tu","frase":"Vorrei un chilo di pomodori e mezzo chilo di peperoni.","traducao":"Gostaria de um quilo de tomates e meio quilo de pimentões.","audio_ipa":"","alternativas":["Vorrei un chilo di pomodori e mezzo chilo di peperoni.","Solo mele, grazie.","Quanto costano le mele?","Non so ancora cosa voglio."],"resposta_correta":0},
        {"id":3,"personaggio":"Venditore","frase":"Eccoli! Vuole altro? Abbiamo delle belle mele oggi.","traducao":"Aqui estão! Quer mais alguma coisa? Temos maçãs bonitas hoje.","audio_ipa":""},
        {"id":4,"personaggio":"Tu","frase":"Sì, mi dia anche un kilo di mele. Quanto viene in tutto?","traducao":"Sim, me dê também um quilo de maçãs. Quanto fica no total?","audio_ipa":"","alternativas":["Sì, mi dia anche un kilo di mele. Quanto viene in tutto?","No grazie, basta così.","Sono fresche le mele?","Non mi piacciono le mele."],"resposta_correta":0},
        {"id":5,"personaggio":"Venditore","frase":"Cinque euro e cinquanta in tutto.","traducao":"Cinco euros e cinquenta no total.","audio_ipa":""},
        {"id":6,"personaggio":"Tu","frase":"Ecco sei euro. Tenga il resto.","traducao":"Aqui estão seis euros. Fique com o troco.","audio_ipa":"","alternativas":["Ecco sei euro. Tenga il resto.","Ho solo banconote grandi.","Posso pagare con carta?","Ho solo cinque euro."],"resposta_correta":0}
      ],
      "vocabulario_chave":["chilo","pomodori","peperoni","mele","resto","banconota"],
      "xp_recompensa":40
    },
    {
      "id": "dial_007",
      "titulo": "In Hotel",
      "icone": "🏨",
      "nivel": "A2",
      "contexto": "Você chega a um hotel italiano para fazer check-in.",
      "turni": [
        {"id":1,"personaggio":"Receptionist","frase":"Benvenuto! Ha una prenotazione?","traducao":"Bem-vindo! Tem uma reserva?","audio_ipa":""},
        {"id":2,"personaggio":"Tu","frase":"Sì, ho prenotato una camera doppia per tre notti. Il nome è Silva.","traducao":"Sim, reservei um quarto duplo por três noites. O nome é Silva.","audio_ipa":"","alternativas":["Sì, ho prenotato una camera doppia per tre notti. Il nome è Silva.","No, non ho prenotato.","Voglio una camera singola.","Ho prenotato online ieri."],"resposta_correta":0},
        {"id":3,"personaggio":"Receptionist","frase":"Perfetto. La camera è al secondo piano. La colazione è inclusa.","traducao":"Perfeito. O quarto é no segundo andar. O café da manhã está incluído.","audio_ipa":""},
        {"id":4,"personaggio":"Tu","frase":"Ottimo. C'è il parcheggio gratuito?","traducao":"Ótimo. Tem estacionamento gratuito?","audio_ipa":"","alternativas":["Ottimo. C'è il parcheggio gratuito?","A che ora è la colazione?","Posso avere una camera diversa?","Il Wi-Fi funziona?"],"resposta_correta":0},
        {"id":5,"personaggio":"Receptionist","frase":"Sì, il parcheggio è gratuito per gli ospiti. Ecco la chiave.","traducao":"Sim, o estacionamento é gratuito para os hóspedes. Aqui está a chave.","audio_ipa":""},
        {"id":6,"personaggio":"Tu","frase":"Grazie. A che ora è il check-out domani?","traducao":"Obrigado. A que horas é o check-out amanhã?","audio_ipa":"","alternativas":["Grazie. A che ora è il check-out domani?","Posso avere un'altra chiave?","Il wi-fi qual è la password?","Dov'è l'ascensore?"],"resposta_correta":0}
      ],
      "vocabulario_chave":["prenotazione","camera doppia","colazione","parcheggio","chiave","check-out"],
      "xp_recompensa":50
    },
    {
      "id": "dial_008",
      "titulo": "Chiedere Indicazioni",
      "icone": "🗺️",
      "nivel": "A1",
      "contexto": "Você está perdido e pede indicações para um passante.",
      "turni": [
        {"id":1,"personaggio":"Tu","frase":"Scusi, sa dov'è il Colosseo?","traducao":"Com licença, sabe onde fica o Coliseu?","audio_ipa":"","alternativas":["Scusi, sa dov'è il Colosseo?","Mi sono perso.","Dove sono?","Mi aiuti per favore."],"resposta_correta":0},
        {"id":2,"personaggio":"Passante","frase":"Certo! Vada dritto per duecento metri, poi giri a destra.","traducao":"Claro! Vá reto por duzentos metros, depois vire à direita.","audio_ipa":""},
        {"id":3,"personaggio":"Tu","frase":"Grazie. È lontano da qui a piedi?","traducao":"Obrigado. É longe daqui a pé?","audio_ipa":"","alternativas":["Grazie. È lontano da qui a piedi?","Non capisco, scusi.","Posso prendere il bus?","Devo girare a sinistra?"],"resposta_correta":0},
        {"id":4,"personaggio":"Passante","frase":"No, sono circa dieci minuti a piedi.","traducao":"Não, são aproximadamente dez minutos a pé.","audio_ipa":""},
        {"id":5,"personaggio":"Tu","frase":"Perfetto, grazie mille!","traducao":"Perfeito, muito obrigado!","audio_ipa":"","alternativas":["Perfetto, grazie mille!","Non importa.","Arrivederci.","Capisco."],"resposta_correta":0},
        {"id":6,"personaggio":"Passante","frase":"Prego! Buona visita!","traducao":"De nada! Boa visita!","audio_ipa":""}
      ],
      "vocabulario_chave":["scusi","dritto","girare","destra","sinistra","lontano","vicino"],
      "xp_recompensa":40
    }
  ]
}
```

### Interface — Nova Aba/Seção "Dialoghi"

**Adicionar ao bottom nav mobile** (index.html):
- Substituir ou adicionar ícone 💬 no bottom nav
- Ou: Adicionar como sub-aba dentro da aba "Grammatica"

**Estrutura de telas:**
1. **Seletor de diálogos** — grade de cards com ícone, título, nível e XP
2. **Modo Leitura** — exibe diálogo completo com áudio de cada fala (clique para ouvir)
3. **Modo Prática** — turno a turno: frases do personagem aparecem, usuário escolhe a resposta correta (múltipla escolha)
4. **Resultado** — XP ganho, vocabulário chave, botão "Rever"

### JS — Novo módulo `js/dialoghi.js`

```javascript
const Dialoghi = {
  dados: null,
  dialogoAtual: null,
  turnoAtual: 0,
  modo: 'leitura', // 'leitura' | 'pratica'
  acertos: 0,
  
  async carregar() {
    if (this.dados) return;
    const r = await fetch('data/dialogi.json');
    this.dados = await r.json();
  },
  
  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('dialoghi-container');
    if (!c) return;
    // Renderiza grade de cards de diálogos
    // Card mostra: icone, titulo, nivel badge, XP recompensa
  },
  
  abrirDialogo(id, modo) {
    this.dialogoAtual = this.dados.dialogi.find(d => d.id === id);
    this.turnoAtual = 0;
    this.acertos = 0;
    this.modo = modo || 'leitura';
    this.renderizarDialogo();
  },
  
  renderizarDialogo() {
    // Modo leitura: mostra todos os turnos com botão 🔊 em cada frase
    // Modo prática: mostra um turno por vez, com choices para turni do "Tu"
  },
  
  checarResposta(indice) {
    const turno = this.dialogoAtual.turni[this.turnoAtual];
    const correto = indice === turno.resposta_correta;
    if (correto) this.acertos++;
    // Anima, avança para próximo turno
    this.turnoAtual++;
    if (this.turnoAtual >= this.dialogoAtual.turni.length) {
      this.mostrarResultado();
    } else {
      this.renderizarTurno();
    }
  },
  
  mostrarResultado() {
    const pct = Math.round(this.acertos / this.dialogoAtual.turni.filter(t => t.alternativas).length * 100);
    Progressao.ganhar(this.dialogoAtual.xp_recompensa);
    // Mostra resultado com XP ganho e vocabulário chave
  }
};
```

### HTML — Seção Dialoghi

**Adicionar após sec-vocabolario em index.html:**
```html
<section id="sec-dialoghi" class="section">
  <h2 class="section-titulo">I Dialoghi</h2>
  <p style="text-align:center;color:#888;font-size:0.9rem;margin-bottom:1rem;">
    Pratique situações reais do dia a dia — como os atores fazem antes de uma cena.
  </p>
  <div id="dialoghi-container"></div>
</section>
```

**Adicionar no nav top (desktop):**
```html
<button class="nav-tab" data-section="dialoghi" onclick="App.navegar('dialoghi')">
  💬 <span class="tab-texto">Dialoghi</span>
</button>
```

**Adicionar no bottom nav (mobile):**
```html
<button data-section="dialoghi" onclick="App.navegar('dialoghi')">💬<span>Diálogos</span></button>
```

**Adicionar script em index.html (junto aos outros scripts):**
```html
<script src="js/dialoghi.js?v=1"></script>
```

**Adicionar em `App.init()` (js/core.js):**
```javascript
if (typeof Dialoghi !== 'undefined') Dialoghi.renderizarSeletor();
```

**Adicionar em `App.navegar()` (js/core.js):**
```javascript
if (secao === 'dialoghi' && typeof Dialoghi !== 'undefined') Dialoghi.renderizarSeletor();
```

### CSS — Estilo dos Diálogos

```css
/* Seletor */
.dialogo-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; }
.dialogo-card { background: white; border-radius: 14px; padding: 1.2rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08); cursor: pointer; text-align: center; transition: transform 0.2s, box-shadow 0.2s; border: 2px solid transparent; }
.dialogo-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); border-color: #9B2335; }
.dialogo-icone { font-size: 2.5rem; margin-bottom: 0.5rem; }
.dialogo-titulo { font-family: 'Cinzel', serif; font-size: 0.9rem; font-weight: 700; color: #9B2335; margin-bottom: 0.3rem; }
.dialogo-nivel { font-size: 0.7rem; background: #F5EDD8; color: #9B2335; padding: 0.1rem 0.4rem; border-radius: 8px; display: inline-block; }

/* Modo Leitura */
.dialogo-conversa { display: flex; flex-direction: column; gap: 0.8rem; padding: 1rem; }
.dialogo-turno { display: flex; gap: 0.8rem; align-items: flex-start; }
.dialogo-turno.personaggio { justify-content: flex-start; }
.dialogo-turno.utente { justify-content: flex-end; flex-direction: row-reverse; }
.dialogo-bubble { max-width: 75%; padding: 0.75rem 1rem; border-radius: 14px; line-height: 1.5; }
.dialogo-turno.personaggio .dialogo-bubble { background: #F5EDD8; color: #2C2C2C; border-bottom-left-radius: 4px; }
.dialogo-turno.utente .dialogo-bubble { background: #9B2335; color: white; border-bottom-right-radius: 4px; }
.dialogo-nome { font-size: 0.7rem; font-weight: 700; opacity: 0.7; margin-bottom: 0.2rem; }
.dialogo-traducao { font-size: 0.78rem; opacity: 0.7; margin-top: 0.3rem; font-style: italic; }
.dialogo-audio-btn { background: none; border: none; cursor: pointer; font-size: 1rem; opacity: 0.7; }
.dialogo-audio-btn:hover { opacity: 1; }

/* Modo Prática */
.dialogo-pratica-frase { background: #F5EDD8; border-radius: 14px; padding: 1rem 1.2rem; margin: 1rem; font-size: 1rem; line-height: 1.5; }
.dialogo-pratica-traducao { font-size: 0.82rem; color: #888; font-style: italic; margin-top: 0.3rem; }
.dialogo-opcoes { display: flex; flex-direction: column; gap: 0.6rem; padding: 0 1rem; }
.dialogo-opcao { background: white; border: 2px solid #ddd; border-radius: 10px; padding: 0.75rem 1rem; text-align: left; cursor: pointer; font-size: 0.9rem; transition: all 0.15s; }
.dialogo-opcao:hover { border-color: #9B2335; background: #fdf5f5; }
.dialogo-opcao.correta { background: #d5f5e3; border-color: #27AE60; color: #1a7a40; }
.dialogo-opcao.errada { background: #fde8e6; border-color: #C0392B; color: #922b21; }
```

### SW + core.js Updates

**sw.js** — adicionar no array STATIC:
```javascript
'./data/dialogi.json',
'./js/dialoghi.js',
```

**Incrementar versão:** `italiano-v10` → `italiano-v11`

---

## FEATURE 2 — META COM PRAZO

### Conceito
A maior diferença dos famosos: **deadline real**. O app calcula quanto XP/dia é necessário para atingir o nível desejado até a data escolhida, e mostra uma previsão honesta.

### Dados (localStorage)

```javascript
// Adicionar ao carregarProgresso() em core.js
if (!p.meta_prazo) p.meta_prazo = null;
// Estrutura:
{
  nivel_alvo: 15,           // nível que quer atingir
  data_alvo: "2026-12-31", // data limite
  xp_na_criacao: 1200,     // XP quando criou a meta
  criado_em: 1748000000000  // timestamp
}
```

### JS — Adicionar em `js/progression.js`

```javascript
// Calcular meta com prazo
calcularMetaPrazo() {
  const p = App.estado.progresso;
  if (!p || !p.meta_prazo) return null;
  
  const meta = p.meta_prazo;
  const hoje = Date.now();
  const dataAlvo = new Date(meta.data_alvo).getTime();
  const diasRestantes = Math.ceil((dataAlvo - hoje) / 86400000);
  
  // XP necessário para o nível alvo
  const XP_POR_NIVEL = [0,500,1200,2100,3200,4500,6000,7700,9600,11700,14000,16500,19200,22100,25200,28500,32000,35700,39600,43700,48000];
  const xpAlvo = XP_POR_NIVEL[meta.nivel_alvo] || 48000;
  const xpFaltante = Math.max(0, xpAlvo - p.xp);
  const xpPorDia = diasRestantes > 0 ? Math.ceil(xpFaltante / diasRestantes) : xpFaltante;
  
  // Velocidade atual (média últimos 7 dias)
  const diario = JSON.parse(localStorage.getItem('it_diario') || '{}');
  const hoje7 = new Date(); 
  let xpSemana = 0;
  for (let i = 0; i < 7; i++) {
    const d = new Date(hoje7); d.setDate(d.getDate() - i);
    const k = d.toISOString().slice(0,10);
    const entry = diario[k];
    if (entry) xpSemana += (typeof entry === 'object' ? entry.xp : 0);
  }
  const xpMedioDia = Math.round(xpSemana / 7);
  
  // Previsão: quantos dias faltam se continuar assim
  const diasNecessarios = xpMedioDia > 0 ? Math.ceil(xpFaltante / xpMedioDia) : 9999;
  const dataPrevisao = new Date(hoje + diasNecessarios * 86400000).toLocaleDateString('pt-BR');
  const atingeNoPrazo = diasNecessarios <= diasRestantes;
  
  return { diasRestantes, xpFaltante, xpPorDia, xpMedioDia, dataPrevisao, atingeNoPrazo, nivel_alvo: meta.nivel_alvo, data_alvo: meta.data_alvo };
},

definirMetaPrazo(nivelAlvo, dataAlvo) {
  const p = App.estado.progresso;
  p.meta_prazo = { nivel_alvo: nivelAlvo, data_alvo: dataAlvo, xp_na_criacao: p.xp, criado_em: Date.now() };
  App.salvarProgresso();
  App.notificar('🎯 Meta definida! Boa sorte!', 'sucesso');
},

removerMetaPrazo() {
  App.estado.progresso.meta_prazo = null;
  App.salvarProgresso();
}
```

### Interface — Card na Home (Templi)

**Adicionar em `renderizarTemplos()` no `core.js`** após `renderizarCardContinuar()`:
```javascript
// Render meta com prazo
const metaContainer = document.getElementById('meta-prazo-container');
if (metaContainer) {
  metaContainer.innerHTML = this._renderizarMetaPrazo();
}
```

```javascript
_renderizarMetaPrazo() {
  const p = this.estado.progresso;
  if (!p || !p.meta_prazo) {
    return `<div class="card-meta-prazo card-meta-vazia" onclick="App.abrirModalMetaPrazo()">
      <span>🎯</span>
      <span>Definir uma meta com prazo</span>
      <span class="cc-cta">→</span>
    </div>`;
  }
  const dados = Progressao.calcularMetaPrazo();
  if (!dados) return '';
  const cor = dados.atingeNoPrazo ? '#27AE60' : '#E74C3C';
  const emoji = dados.atingeNoPrazo ? '✅' : '⚠️';
  return `<div class="card-meta-prazo" onclick="App.abrirModalMetaPrazo()">
    <div class="meta-prazo-titulo">${emoji} Meta: Nível ${dados.nivel_alvo} até ${new Date(dados.data_alvo).toLocaleDateString('pt-BR')}</div>
    <div class="meta-prazo-info">
      <span style="color:${cor}">${dados.xpPorDia} XP/dia necessários</span>
      <span>·</span>
      <span>${dados.diasRestantes} dias restantes</span>
    </div>
    <div class="meta-prazo-previsao">No ritmo atual: ${dados.dataPrevisao}</div>
  </div>`;
}
```

**Modal para definir/editar meta** (adicionar ao index.html):
```html
<div id="modal-meta-prazo" class="modal" style="display:none">
  <div class="modal-conteudo" style="max-width:400px">
    <h3 style="font-family:'Cinzel',serif;color:#9B2335;margin-bottom:1rem;">🎯 Minha Meta</h3>
    <label>Quero atingir o nível:</label>
    <select id="meta-nivel-alvo" style="width:100%;margin:0.5rem 0 1rem;padding:0.5rem;border:2px solid #ddd;border-radius:8px;">
      <option value="5">Nível 5 — Iniciante Consolidado</option>
      <option value="10">Nível 10 — Intermediário</option>
      <option value="15">Nível 15 — Avançado</option>
      <option value="20">Nível 20 — Italiano Autentico</option>
    </select>
    <label>Até a data:</label>
    <input type="date" id="meta-data-alvo" style="width:100%;margin:0.5rem 0 1rem;padding:0.5rem;border:2px solid #ddd;border-radius:8px;">
    <div id="meta-prazo-preview" style="margin-bottom:1rem;"></div>
    <div style="display:flex;gap:0.5rem;">
      <button class="btn-primario" style="flex:1" onclick="App.confirmarMetaPrazo()">Definir Meta</button>
      <button class="btn-secondario" onclick="App.fecharModalMetaPrazo()">Cancelar</button>
    </div>
    <button onclick="Progressao.removerMetaPrazo();App.fecharModalMetaPrazo();" style="width:100%;margin-top:0.5rem;background:none;border:none;color:#C0392B;cursor:pointer;font-size:0.85rem;">Remover meta atual</button>
  </div>
</div>
```

**Adicionar em index.html (HTML da home, após continuar-container):**
```html
<div id="meta-prazo-container"></div>
```

### CSS

```css
.card-meta-prazo { background: white; border-radius: 12px; padding: 0.9rem 1.1rem; box-shadow: 0 2px 12px rgba(0,0,0,0.08); margin-bottom: 1rem; cursor: pointer; border-left: 4px solid #9B2335; transition: box-shadow 0.2s; }
.card-meta-prazo:hover { box-shadow: 0 4px 18px rgba(0,0,0,0.13); }
.card-meta-vazia { display: flex; align-items: center; gap: 0.6rem; color: #aaa; font-size: 0.88rem; border-left-color: #ddd; }
.meta-prazo-titulo { font-weight: 700; font-size: 0.9rem; color: #2C2C2C; margin-bottom: 0.3rem; }
.meta-prazo-info { font-size: 0.83rem; display: flex; gap: 0.5rem; margin-bottom: 0.2rem; }
.meta-prazo-previsao { font-size: 0.78rem; color: #888; font-style: italic; }
```

---

## FEATURE 3 — MODO CANZONE

### Conceito
Cantores internalizam idiomas através de músicas — a repetição emocional fixa o vocabulário. O usuário ouve a música (TTS) e preenche lacunas na letra.

### Dados — `data/canzoni.json`

```json
{
  "canzoni": [
    {
      "id": "can_001",
      "titulo": "Bella Ciao",
      "artista": "Canção Tradicional",
      "nivel": "A2",
      "icone": "🌹",
      "tema": "storia",
      "estrofes": [
        {
          "id": 1,
          "texto_completo": "Una mattina mi sono alzato, o bella ciao, bella ciao, bella ciao ciao ciao!",
          "texto_lacuna": "Una mattina mi sono ___, o bella ciao, bella ciao, bella ciao ciao ciao!",
          "palavra_oculta": "alzato",
          "traducao": "Uma manhã eu me levantei, ó bella ciao, bella ciao, bella ciao ciao ciao!",
          "dica": "passato prossimo de 'alzarsi'"
        },
        {
          "id": 2,
          "texto_completo": "Una mattina mi sono alzato e ho trovato l'invasor.",
          "texto_lacuna": "Una mattina mi sono alzato e ho ___ l'invasor.",
          "palavra_oculta": "trovato",
          "traducao": "Uma manhã eu me levantei e encontrei o invasor.",
          "dica": "passato prossimo de 'trovare'"
        },
        {
          "id": 3,
          "texto_completo": "O partigiano, portami via, o bella ciao, bella ciao, bella ciao ciao ciao!",
          "texto_lacuna": "___ partigiano, portami via, o bella ciao, bella ciao, bella ciao ciao ciao!",
          "palavra_oculta": "O",
          "traducao": "Ó partigiano, leva-me embora, ó bella ciao, bella ciao, bella ciao ciao ciao!",
          "dica": "interjeição italiana"
        },
        {
          "id": 4,
          "texto_completo": "O partigiano, portami via, ché mi sento di morir.",
          "texto_lacuna": "O partigiano, portami via, ché mi sento di ___.",
          "palavra_oculta": "morir",
          "traducao": "Ó partigiano, leva-me embora, pois me sinto a morrer.",
          "dica": "infinitivo de 'morire'"
        }
      ],
      "vocabulario_chave": ["alzarsi", "trovare", "partigiano", "invasore", "morire"],
      "xp_recompensa": 40
    },
    {
      "id": "can_002",
      "titulo": "Azzurro",
      "artista": "Adriano Celentano",
      "nivel": "B1",
      "icone": "🎵",
      "tema": "amore",
      "estrofes": [
        {
          "id": 1,
          "texto_completo": "Cerco l'estate tutto l'anno e all'improvviso eccola qua.",
          "texto_lacuna": "Cerco l'___ tutto l'anno e all'improvviso eccola qua.",
          "palavra_oculta": "estate",
          "traducao": "Procuro o verão o ano todo e de repente aqui está.",
          "dica": "stagione calda"
        },
        {
          "id": 2,
          "texto_completo": "Lei è partita per le spiagge e sono solo qua.",
          "texto_lacuna": "Lei è ___ per le spiagge e sono solo qua.",
          "palavra_oculta": "partita",
          "traducao": "Ela foi para as praias e estou sozinho aqui.",
          "dica": "passato prossimo di 'partire' (femminile)"
        },
        {
          "id": 3,
          "texto_completo": "Azzurro, il pomeriggio è troppo azzurro e lungo per me.",
          "texto_lacuna": "Azzurro, il ___ è troppo azzurro e lungo per me.",
          "palavra_oculta": "pomeriggio",
          "traducao": "Azul celeste, a tarde é azul demais e longa para mim.",
          "dica": "parte do dia entre il mezzogiorno e la sera"
        },
        {
          "id": 4,
          "texto_completo": "Mi accorgo di non avere più risorse, senza di te.",
          "texto_lacuna": "Mi accorgo di non avere più ___, senza di te.",
          "palavra_oculta": "risorse",
          "traducao": "Percebo que não tenho mais recursos, sem você.",
          "dica": "plurale di 'risorsa' — forze, energia"
        }
      ],
      "vocabulario_chave": ["estate", "partire", "pomeriggio", "azzurro", "accorgersi", "risorse"],
      "xp_recompensa": 50
    },
    {
      "id": "can_003",
      "titulo": "Nel Blu Dipinto di Blu (Volare)",
      "artista": "Domenico Modugno",
      "nivel": "B1",
      "icone": "🎶",
      "tema": "sogno",
      "estrofes": [
        {
          "id": 1,
          "texto_completo": "Penso che un sogno così non ritorni mai più.",
          "texto_lacuna": "Penso che un ___ così non ritorni mai più.",
          "palavra_oculta": "sogno",
          "traducao": "Penso que um sonho assim nunca mais voltará.",
          "dica": "ciò che si vede dormendo"
        },
        {
          "id": 2,
          "texto_completo": "Mi dipingevo le mani e la faccia di blu.",
          "texto_lacuna": "Mi dipingevo le mani e la ___ di blu.",
          "palavra_oculta": "faccia",
          "traducao": "Pintava minhas mãos e meu rosto de azul.",
          "dica": "parte del viso"
        },
        {
          "id": 3,
          "texto_completo": "Volare, oh oh! Cantare, oh oh oh oh!",
          "texto_lacuna": "___, oh oh! Cantare, oh oh oh oh!",
          "palavra_oculta": "Volare",
          "traducao": "Voar, oh oh! Cantar, oh oh oh oh!",
          "dica": "spostarsi nell'aria come gli uccelli"
        },
        {
          "id": 4,
          "texto_completo": "Nel blu dipinto di blu, felice di stare lassù.",
          "texto_lacuna": "Nel blu dipinto di blu, ___ di stare lassù.",
          "palavra_oculta": "felice",
          "traducao": "No azul pintado de azul, feliz de estar lá em cima.",
          "dica": "contrario di 'triste'"
        }
      ],
      "vocabulario_chave": ["sogno", "faccia", "volare", "cantare", "felice", "dipingere"],
      "xp_recompensa": 50
    }
  ]
}
```

### JS — Módulo `js/canzoni.js`

```javascript
const Canzoni = {
  dados: null,
  canzonAtual: null,
  estrofeAtual: 0,
  acertos: 0,
  
  async carregar() {
    if (this.dados) return;
    const r = await fetch('data/canzoni.json');
    this.dados = await r.json();
  },
  
  async renderizarSeletor() {
    await this.carregar();
    const c = document.getElementById('canzoni-container');
    if (!c) return;
    let html = '<div class="dialogo-grid">';
    for (const can of this.dados.canzoni) {
      html += `<div class="dialogo-card" onclick="Canzoni.abrirCanzone('${can.id}')">
        <div class="dialogo-icone">${can.icone}</div>
        <div class="dialogo-titulo">${can.titulo}</div>
        <div style="font-size:0.75rem;color:#888;margin:0.2rem 0">${can.artista}</div>
        <div class="dialogo-nivel">${can.nivel}</div>
      </div>`;
    }
    html += '</div>';
    c.innerHTML = html;
  },
  
  async abrirCanzone(id) {
    await this.carregar();
    this.canzonAtual = this.dados.canzoni.find(c => c.id === id);
    this.estrofeAtual = 0;
    this.acertos = 0;
    this.renderizarEstrofe();
  },
  
  renderizarEstrofe() {
    const c = document.getElementById('canzoni-container');
    const can = this.canzonAtual;
    const est = can.estrofes[this.estrofeAtual];
    const total = can.estrofes.length;
    const pct = Math.round(this.estrofeAtual / total * 100);
    
    c.innerHTML = `
      <div class="gram-lesson-nav">
        <button class="gram-btn-back" onclick="Canzoni.renderizarSeletor()">‹ Canzoni</button>
        <span style="font-size:0.85rem;color:#888">${this.estrofeAtual+1}/${total}</span>
      </div>
      <div style="text-align:center;padding:1rem 0 0.5rem">
        <div style="font-size:1.5rem">${can.icone}</div>
        <div style="font-family:'Cinzel',serif;font-weight:700;color:#9B2335">${can.titulo}</div>
        <div style="font-size:0.8rem;color:#888">${can.artista}</div>
      </div>
      <div class="gram-ex-progress-bar" style="margin:0.5rem 1rem"><div class="gram-ex-progress-fill" style="width:${pct}%"></div></div>
      <div class="gram-card" style="margin:1rem">
        <div style="font-size:1rem;line-height:1.8;padding:1rem;text-align:center;font-style:italic;color:#2C2C2C">
          ${est.texto_lacuna.replace('___', '<input id="canzone-input" type="text" autocomplete="off" autocorrect="off" spellcheck="false" style="border:none;border-bottom:2px solid #9B2335;font-size:1rem;font-style:italic;width:100px;text-align:center;outline:none;background:transparent" placeholder="___" onkeydown="if(event.key===\'Enter\')Canzoni.verificar()">')}
        </div>
        <div style="text-align:center;font-size:0.82rem;color:#888;font-style:italic;padding:0 1rem 0.5rem">${est.traducao}</div>
        <div style="text-align:center;font-size:0.78rem;color:#D4A843;padding-bottom:1rem">💡 Dica: ${est.dica}</div>
        <div id="canzone-feedback"></div>
        <div style="display:flex;justify-content:center;gap:0.5rem;padding:0.5rem">
          <button class="btn-primario" onclick="Canzoni.verificar()">✔ Verificar</button>
          <button class="btn-secondario" onclick="App.pronunciar('${est.texto_completo.replace(/'/g,"\\'")}')">🔊 Ouvir</button>
        </div>
      </div>`;
    setTimeout(() => document.getElementById('canzone-input')?.focus(), 100);
  },
  
  verificar() {
    const est = this.canzonAtual.estrofes[this.estrofeAtual];
    const input = document.getElementById('canzone-input');
    const fb = document.getElementById('canzone-feedback');
    if (!input || !fb) return;
    const digitado = input.value.trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
    const correto = est.palavra_oculta.trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g,'');
    const acertou = digitado === correto;
    if (acertou) {
      this.acertos++;
      App.ganharXP(5);
      fb.innerHTML = `<div style="color:#27AE60;text-align:center;padding:0.5rem;font-weight:700">✅ Corretto! "${est.palavra_oculta}"</div>`;
    } else {
      fb.innerHTML = `<div style="color:#C0392B;text-align:center;padding:0.5rem">❌ A palavra era: <strong>${est.palavra_oculta}</strong></div>`;
    }
    input.disabled = true;
    input.value = est.palavra_oculta;
    input.style.color = acertou ? '#27AE60' : '#C0392B';
    setTimeout(() => {
      this.estrofeAtual++;
      if (this.estrofeAtual >= this.canzonAtual.estrofes.length) this.mostrarResultado();
      else this.renderizarEstrofe();
    }, 1500);
  },
  
  mostrarResultado() {
    const can = this.canzonAtual;
    const total = can.estrofes.length;
    const pct = Math.round(this.acertos / total * 100);
    Progressao.ganhar(can.xp_recompensa);
    const c = document.getElementById('canzoni-container');
    c.innerHTML = `<div style="text-align:center;padding:2rem">
      <div style="font-size:3rem">${pct >= 80 ? '🎤' : '🎵'}</div>
      <div style="font-family:'Cinzel',serif;font-size:1.2rem;color:#9B2335;margin:0.5rem 0">${can.titulo}</div>
      <div style="font-size:1.5rem;font-weight:700;margin:0.5rem 0">${this.acertos}/${total} corretas</div>
      <div style="color:#888;margin-bottom:1rem">+${can.xp_recompensa} XP</div>
      <div style="display:flex;gap:0.5rem;justify-content:center">
        <button class="btn-primario" onclick="Canzoni.abrirCanzone('${can.id}')">🔄 Repetir</button>
        <button class="btn-secondario" onclick="Canzoni.renderizarSeletor()">‹ Outras músicas</button>
      </div>
    </div>`;
  }
};
```

### HTML — Integração

**Adicionar seção (index.html):**
```html
<section id="sec-canzoni" class="section">
  <h2 class="section-titulo">Le Canzoni</h2>
  <p style="text-align:center;color:#888;font-size:0.9rem;margin-bottom:1rem;">
    Aprenda italiano como os cantores fazem — com músicas reais.
  </p>
  <div id="canzoni-container"></div>
</section>
```

**Adicionar script:** `<script src="js/canzoni.js?v=1"></script>`

**Lazy-render em `App.navegar()`:**
```javascript
if (secao === 'canzoni' && typeof Canzoni !== 'undefined') Canzoni.renderizarSeletor();
```

---

## FEATURE 4 — MODO IMITAÇÃO FONÉTICA

### Conceito
Simples: botão "🎤 Gravar" no flashcard. Usuário tenta pronunciar. App usa SpeechRecognition para verificar se a palavra foi reconhecida.

### Limitações conhecidas
- `SpeechRecognition` só funciona online (Google Speech API por baixo)
- Não funciona em todos os browsers (Firefox não suporta)
- Não é comparação perfeita — verifica se a palavra foi reconhecida no texto transcrito

### JS — Adicionar em `js/flashcards.js`

```javascript
// Adicionar propriedades ao objeto Flashcards:
gravando: false,
_recognition: null,

// Método de inicialização (chamar em toggleEscuta ou em init):
_iniciarReconhecimento() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) return null;
  const r = new SR();
  r.lang = 'it-IT';
  r.continuous = false;
  r.interimResults = false;
  return r;
},

// Botão de gravação:
toggleGravar() {
  if (!this.cartaAtual) return;
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { App.notificar('Seu browser não suporta reconhecimento de voz.', 'alerta'); return; }
  
  if (this.gravando) {
    if (this._recognition) this._recognition.stop();
    this.gravando = false;
    return;
  }
  
  this.gravando = true;
  const btnGravar = document.getElementById('btn-gravar');
  if (btnGravar) { btnGravar.textContent = '⏹ Parar'; btnGravar.style.background = '#C0392B'; }
  
  this._recognition = this._iniciarReconhecimento();
  this._recognition.onresult = (e) => {
    const texto = e.results[0][0].transcript.toLowerCase();
    const alvo = (this.cartaAtual.italiano || '').toLowerCase();
    const reconheceu = texto.includes(alvo) || alvo.includes(texto.split(' ')[0]);
    this._mostrarFeedbackPronuncia(texto, reconheceu);
  };
  this._recognition.onerror = () => { App.notificar('Não consegui ouvir. Tente novamente.', 'alerta'); };
  this._recognition.onend = () => {
    this.gravando = false;
    if (btnGravar) { btnGravar.textContent = '🎤 Imitar'; btnGravar.style.background = ''; }
  };
  this._recognition.start();
},

_mostrarFeedbackPronuncia(texto, reconheceu) {
  const fb = document.getElementById('imitacao-feedback');
  if (!fb) return;
  if (reconheceu) {
    fb.innerHTML = `<span style="color:#27AE60">✅ Bene! Reconheci: "${texto}"</span>`;
    App.ganharXP(3);
  } else {
    fb.innerHTML = `<span style="color:#E67E22">🔄 Ouvi: "${texto}" — tente de novo!</span>`;
  }
  fb.style.display = 'block';
  setTimeout(() => { if(fb) fb.style.display = 'none'; }, 3000);
}
```

### HTML — Botão no Flashcard

**Adicionar em `index.html` junto ao btn-audio e btn-dica:**
```html
<button class="btn-audio" onclick="Flashcards.toggleGravar()" id="btn-gravar">🎤 Imitar</button>
<div id="imitacao-feedback" style="display:none;text-align:center;font-size:0.85rem;margin-top:0.3rem;padding:0.3rem;"></div>
```

**Nota:** Mostrar/ocultar o botão baseado no suporte:
```javascript
// Em Flashcards.init() ou mostrarCarta():
const btnGravar = document.getElementById('btn-gravar');
if (btnGravar) {
  const suporta = !!(window.SpeechRecognition || window.webkitSpeechRecognition);
  btnGravar.style.display = suporta ? '' : 'none';
}
```

---

## ORDEM DE IMPLEMENTAÇÃO RECOMENDADA

1. **Feature 2** (Meta com Prazo) — mais impactante, menos código, sem novos arquivos de dados
2. **Feature 1** (Diálogos) — cria novo arquivo de dados + módulo JS + seção HTML
3. **Feature 3** (Canzoni) — mesma estrutura dos diálogos, mais fácil depois de ter o padrão
4. **Feature 4** (Imitação) — pequena adição ao flashcards.js

---

## ARQUIVOS A MODIFICAR / CRIAR

| Ação | Arquivo | Mudança |
|------|---------|---------|
| CRIAR | `data/dialogi.json` | 8+ diálogos completos (incluídos nesta spec) |
| CRIAR | `data/canzoni.json` | 3+ músicas com lacunas (incluídas nesta spec) |
| CRIAR | `js/dialoghi.js` | Módulo completo de diálogos |
| CRIAR | `js/canzoni.js` | Módulo completo de canzoni |
| MODIFICAR | `js/core.js` | `_renderizarMetaPrazo()`, `abrirModalMetaPrazo()`, navegar() |
| MODIFICAR | `js/progression.js` | `calcularMetaPrazo()`, `definirMetaPrazo()`, `removerMetaPrazo()` |
| MODIFICAR | `js/flashcards.js` | `toggleGravar()`, `_iniciarReconhecimento()`, `_mostrarFeedbackPronuncia()` |
| MODIFICAR | `index.html` | Nova seção dialoghi, nova seção canzoni, modal meta prazo, botão gravar |
| MODIFICAR | `sw.js` | Versão v11, adicionar novos arquivos no cache |

---

## VERIFICAÇÃO FINAL

Após implementar, testar:

- [x] Home: card "Meta com Prazo" aparece; clicar abre modal; definir meta; verificar cálculo de XP/dia
- [x] Navegar para "Dialoghi": lista de diálogos aparece; clicar abre modo leitura com áudio; modo prática funciona com múltipla escolha; XP é concedido
- [x] Navegar para "Canzoni": lista de músicas; clicar abre exercício de lacuna; digitar palavra; verificar; resultado mostra XP
- [x] Flashcard: botão "🎤 Imitar" aparece (Chrome); clicar inicia gravação; falar a palavra italiana; feedback aparece
- [ ] GitHub Pages: `git push origin master && git push origin master:gh-pages --force`
