"""
Adiciona campos NMA às 5 unidades do módulo B1.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

b1 = next(m for m in data['moduli'] if m['id'] == 'B1')

# ─── b1-i: Il mondo digitale e i social media ───
u = next(x for x in b1['unidades'] if x['id'] == 'b1-i')
u['alerta'] = (
    "O vocabulário digital é o mais universal e também o mais dinâmico: "
    "metade das palavras são empréstimos do inglês. "
    "Esta unidade ensina a navegar no discurso digital em italiano — "
    "incluindo quando usar o anglicismo e quando não usar."
)
u['inventario'] = [
    "Internet: navigare in rete, il sito web, il motore di ricerca, scaricare, caricare (upload)",
    "Social: postare, condividere, seguire, il follower, il like, la storia (story), il profilo",
    "Comunicação: inviare un messaggio, il gruppo, la chat, il thread, il commento",
    "Problemas: il bug, crashare, il virus, la password, il backup, la connessione lenta",
    "Verbo USARE: uso, usi, usa, usiamo, usate, usano — e CONNETTERE, PUBBLICARE",
    "Congiuntivo presente com spero/penso: spero che sia / penso che abbia",
    "Periodo ipotetico reale: se hai il wifi, ti mando il file (se tiver, te mando)",
    "Neologismi: il selfie, lo screenshot, la videochiamata, il backup, il profilo verificato"
]
u['definicao'] = {
    "fenomeno": (
        "Você lê numa rivista italiana: *'Gli italiani passano in media 6 ore al giorno online, "
        "tra social, streaming e smart working. Il fenomeno della FOMO — "
        "Fear Of Missing Out — colpisce soprattutto i giovani tra i 18 e i 30 anni.'* "
        "Você entendeu o texto, mas notou que metade das palavras são inglesas."
    ),
    "causa": (
        "Por que o italiano usa tantos anglicismos no vocabulário digital? "
        "Quando se italianiza uma palavra (ex: *postare* de 'to post') "
        "e quando se mantém a forma inglesa (*selfie*, *hacker*)?"
    ),
    "conceito": (
        "O italiano **italianiza** verbos estrangeiros adicionando *-are*: "
        "*postare, chattare, googolare, crashare*. "
        "Substantivos geralmente mantêm a forma inglesa: *il selfie, lo screenshot, il like*. "
        "A norma linguística aceita ambos, mas o uso formal prefere equivalentes italianos "
        "quando existem: *scaricare* em vez de *downloadare*, *condividere* em vez de *shareare*."
    )
}
u['tecnica'] = (
    "**Como italianizar e usar vocabulário digital:**\n\n"
    "1. Verbos estrangeiros → adicionar **-are**: post → *postare* | chat → *chattare* | like → *likare*\n"
    "2. Artigo de anglicismos: use a fonética inicial → *il selfie* (s+vogal → il, não lo)\n"
    "   → exceto: *lo screenshot* (s+consonante → lo!)\n"
    "3. Congiuntivo com opinião: **penso/credo/spero che** + congiuntivo presente\n"
    "   → *penso che i social siano utili* | *spero che funzioni*\n"
    "4. Preferência formal: *scaricare* > downloadare | *condividere* > shareare | *pubblicare* > postare\n"
    "5. Plurais de anglicismos: invariáveis → *i selfie, i like, gli screenshot* (não *i likes*)"
)
u['exemplos_prc'] = [
    {
        "oracao": "Ho postato una foto e ho ricevuto molti like.",
        "pergunta": "Por que *postato* e *ricevuto* têm formas diferentes? Ambos são participi passati?",
        "resposta": "Sim: postare → postato (reg. -are); ricevere → ricevuto (reg. -ere). Ambos com ausiliare AVERE",
        "conclusao": "-are → -ato | -ere → -uto | -ire → -ito (participi passati regulares)"
    },
    {
        "oracao": "Penso che i social media abbiano cambiato il modo di comunicare.",
        "pergunta": "Por que *abbiano* (congiuntivo) e não *hanno* (indicativo)?",
        "resposta": "penso che + congiuntivo — verbos de opinião (pensare, credere, sperare) requerem congiuntivo na subordinada",
        "conclusao": "pensare/credere/sperare + che → congiuntivo presente"
    },
    {
        "oracao": "Se hai una buona connessione, possiamo fare una videochiamata.",
        "pergunta": "Que tipo de período hipotético é este? E quais tempos verbais usa?",
        "resposta": "Período hipotético real (tipo 1): se + indicativo presente → indicativo presente/futuro",
        "conclusao": "hipótese real: se + presente → presente/futuro (não congiuntivo!)"
    }
]
u['ponte'] = (
    "**Em português:** 'Postei uma foto e recebi muitos likes' — estrutura idêntica.\n\n"
    "**Em italiano:** *ho postato / ho ricevuto* — passato prossimo, não passado simples.\n\n"
    "**Diferença cultural:** os italianos distinguem mais claramente entre uso informal (*postare*) "
    "e formal (*pubblicare*). Em contexto profissional ou jornalístico, evite os anglicismos diretos."
)
u['coda'] = (
    "Siga perfis italianos nas redes sociais que você já usa — é o melhor laboratório para "
    "absorver esse vocabulário em contexto real e atualizado."
)

# ─── b1-ii: Ambiente di lavoro e linguaggio professionale ───
u = next(x for x in b1['unidades'] if x['id'] == 'b1-ii')
u['alerta'] = (
    "O italiano profissional é mais rígido em formalidade do que o português brasileiro. "
    "E-mails mal escritos, uso errado de *Lei* vs *tu*, ou fórmulas de cortesia ausentes "
    "podem comprometer sua credibilidade num ambiente corporativo italiano."
)
u['inventario'] = [
    "Riunioni: convocare una riunione, l'ordine del giorno, il verbale, prendere la parola",
    "E-mail formal: In riferimento a… / Le scrivo per… / Resto a disposizione / Cordiali saluti",
    "Estrutura e-mail: oggetto (assunto), mittente (remetente), destinatario, allegato (anexo)",
    "Hierarquia formal: il direttore, il responsabile, il collega, il collaboratore, il dipendente",
    "Congiuntivo in richieste formali: vorrei che Lei mi inviasse / è necessario che arrivi",
    "Condizionale di cortesia: potrebbe inviarmi…? / sarebbe possibile…? / le dispiacerebbe…?",
    "Passivo in contesti burocráticos: la riunione è stata convocata / il documento verrà firmato",
    "Nominalizzazioni: la gestione, l'implementazione, la valutazione, la pianificazione"
]
u['definicao'] = {
    "fenomeno": (
        "Você recebe um e-mail em italiano: *'Egregio Dott. Silva, "
        "in riferimento alla nostra telefonata di ieri, Le invio in allegato il contratto. "
        "La preghiamo di restituircelo firmato entro venerdì. Distinti saluti.'* "
        "O tom é completamente diferente de um e-mail brasileiro típico."
    ),
    "causa": (
        "O que é *Egregio*? Quando se usa *Dott.* antes do nome? "
        "E *La preghiamo* — quem é esse 'La'? "
        "Por que o italiano formal soa tão diferente do informal?"
    ),
    "conceito": (
        "**Egregio** = tratamento muito formal (ilustre), usado em cartas/e-mails formais. "
        "**Dott./Dott.ssa** = título acadêmico obrigatório para graduados. "
        "**La preghiamo** = *La* é o pronome direto formal de cortesia (Lei → La). "
        "O italiano formal usa passivo, congiuntivo e condizionale "
        "onde o informal usaria presente direto."
    )
}
u['tecnica'] = (
    "**Como escrever e-mails profissionais em italiano:**\n\n"
    "1. Abertura: **Egregio/Gentile** + título + cognome → *Gentile Dott.ssa Rossi,*\n"
    "2. Referência: *In riferimento a* + substantivo | *A seguito di* + evento\n"
    "3. Pedido educado: **condizionale** → *potrebbe inviarmi / le dispiacerebbe*\n"
    "4. Pedido formal com congiuntivo: *è necessario che* + congiuntivo → *che arrivi entro lunedì*\n"
    "5. Fechamento: *Resto a disposizione per qualsiasi chiarimento* + saudação\n"
    "   Saudações: *Cordiali saluti* (neutro) | *Distinti saluti* (mais formal) | *Saluti* (informal)"
)
u['exemplos_prc'] = [
    {
        "oracao": "Potrebbe inviarmi il documento entro domani?",
        "pergunta": "Por que *potrebbe* (condicional) e não *può* (presente)? Qual é a diferença?",
        "resposta": "potrebbe é mais educado e suave — equivale a 'poderia' em vez de 'pode?'. Em contexto formal, o condicional é preferível",
        "conclusao": "condizionale = forma polida de pedir em contexto profissional"
    },
    {
        "oracao": "È necessario che tutti i partecipanti arrivino in orario.",
        "pergunta": "Por que *arrivino* e não *arrivano*? O que muda o modo verbal?",
        "resposta": "è necessario che + congiuntivo presente — expressões impessoais de necessidade/obrigação requerem congiuntivo",
        "conclusao": "è necessario/importante/fondamentale che → congiuntivo"
    },
    {
        "oracao": "La riunione è stata rinviata a data da destinarsi.",
        "pergunta": "Identifique a voz passiva. Qual é o agente? Por que não está explícito?",
        "resposta": "è stata rinviata = passivo (essere + participio). Agente não explicitado — comum em comunicações burocráticas para despersonalizar a informação",
        "conclusao": "passivo sem agente = estilo burocrático italiano para despersonalizar decisões"
    }
]
u['ponte'] = (
    "**Em português:** o e-mail formal brasileiro usa 'Prezado Sr./Sra.' + corpo direto.\n\n"
    "**Em italiano:** *Egregio/Gentile* + título obrigatório se houver + corpo em Lei. "
    "O italiano formal usa mais estruturas passivas e condicionais do que o português brasileiro.\n\n"
    "**Armadilha cultural:** omitir o título (Dott./Ing./Avv.) em e-mails italianos pode ser "
    "percebido como falta de educação — não é opcional como no Brasil."
)
u['coda'] = (
    "Encontre modelos de e-mail formal italiano online e analise a estrutura antes de escrever o seu. "
    "A fórmula é rígida — e seguir a fórmula é mais importante do que ser criativo."
)

# ─── b1-iii: Cultura e società italiana contemporanea ───
u = next(x for x in b1['unidades'] if x['id'] == 'b1-iii')
u['alerta'] = (
    "Entender a cultura italiana contemporânea não é opcional para quem quer "
    "se comunicar de verdade em italiano. "
    "Esta unidade dá ferramentas para discutir tradições, mudanças sociais "
    "e a vida moderna italiana com naturalidade."
)
u['inventario'] = [
    "Tradições: il Carnevale, la Pasqua, il Ferragosto, la Festa della Repubblica (2 giugno)",
    "Família italiana: la famiglia allargata, vivere con i genitori, i mammoni, il pranzo domenicale",
    "Mudanças sociais: l'immigrazione, l'invecchiamento della popolazione, il lavoro precario",
    "Gastronomia: la DOP (Denominazione di Origine Protetta), il km0, il cibo biologico",
    "Verbo CAMBIARE: è cambiato (intransitivo) / ha cambiato (transitivo) — verbo ambiproprio",
    "Congiuntivo com nonostante/benché: nonostante sia / benché abbia",
    "Gerundio per causa/mezzo: essendo italiano, capisce… / lavorando tanto, ha successo",
    "Espressioni idiomatiche: fare la bella vita / avere il pallino per / non mollare"
]
u['definicao'] = {
    "fenomeno": (
        "Você lê: *'Il 77% dei giovani italiani tra 18 e 34 anni vive ancora con i genitori — "
        "un dato che sorprende molti stranieri. Ma gli italiani vedono la cosa diversamente: "
        "la famiglia è una rete di supporto, non una dipendenza.'* "
        "Você entende as palavras, mas não entende a cultura por trás delas."
    ),
    "causa": (
        "Por que tantos jovens italianos moram com os pais? "
        "É questão econômica, cultural, ou ambas? "
        "E como o italiano captura essa nuance — há diferença entre "
        "*dipendere dalla famiglia* e *appoggiarsi alla famiglia*?"
    ),
    "conceito": (
        "A cultura italiana valoriza a **famiglia come rete** (rede de suporte), "
        "não como dependência. *Dipendere* tem conotação negativa (depender passivamente); "
        "*appoggiarsi a* é neutro/positivo (apoiar-se em). "
        "O italiano usa **nonostante + congiuntivo** para concessões: "
        "*nonostante sia difficile, i giovani restano uniti alla famiglia.*"
    )
}
u['tecnica'] = (
    "**Como falar sobre cultura e sociedade italiana:**\n\n"
    "1. Concessão: **nonostante/benché/sebbene** + congiuntivo → *nonostante sia difficile, …*\n"
    "2. Causa com gerundio: **gerundio** no início → *essendo giovane, ha più opportunità*\n"
    "3. CAMBIARE ambiproprio: *è cambiato* (mudou sozinho) | *ha cambiato* (mudou algo)\n"
    "   → *il paese è cambiato* (o país mudou) | *ha cambiato lavoro* (trocou de emprego)\n"
    "4. Para dados/estatísticas: *secondo i dati* | *il X% degli italiani* | *in media*\n"
    "5. Opinião com sfumatura: *da un lato… dall'altro* (por um lado… por outro)"
)
u['exemplos_prc'] = [
    {
        "oracao": "Nonostante la crisi economica, gli italiani non rinunciano al caffè.",
        "pergunta": "Por que *nonostante* é seguido de artigo + substantivo aqui, sem congiuntivo?",
        "resposta": "nonostante + substantivo não requer congiuntivo. Só requer congiuntivo quando seguido de che + verbo: 'nonostante che la crisi sia grave'",
        "conclusao": "nonostante + sostantivo (sem congiuntivo) | nonostante che + congiuntivo"
    },
    {
        "oracao": "Il modo di vivere degli italiani è cambiato molto negli ultimi vent'anni.",
        "pergunta": "Por que *è cambiato* (essere) e não *ha cambiato* (avere)?",
        "resposta": "cambiare intransitivo (sem objeto) = essere; cambiare transitivo (com objeto) = avere. 'Il modo di vivere è cambiato' — sem objeto → essere",
        "conclusao": "cambiare intransitivo = essere | cambiare transitivo = avere"
    },
    {
        "oracao": "Da un lato la tradizione, dall'altro la modernità: questa è l'Italia di oggi.",
        "pergunta": "Como esta estrutura funciona argumentativamente? Quando se usa?",
        "resposta": "da un lato… dall'altro = 'por um lado… por outro' — estrutura para apresentar duas perspectivas sem tomar partido, útil em ensaios e discussões",
        "conclusao": "da un lato… dall'altro lato = estrutura argumentativa para perspectivas opostas"
    }
]
u['ponte'] = (
    "**Em português:** 'Apesar da crise, os italianos não abrem mão do café.'\n\n"
    "**Em italiano:** *Nonostante la crisi, gli italiani non rinunciano al caffè* — estrutura paralela.\n\n"
    "**Diferença:** *rinunciare a* = abrir mão de (com preposição *a*). "
    "Nunca *rinunciare* sem preposição — é uma armadilha para brasileiros."
)
u['coda'] = (
    "Cultura não se aprende só de livros. Assista a programas de notícias italianos, "
    "leia um jornal italiano online por 10 minutos por dia — o vocabulário cultural virá naturalmente."
)

# ─── b1-iv: Esprimere opinioni e argomentare ───
u = next(x for x in b1['unidades'] if x['id'] == 'b1-iv')
u['alerta'] = (
    "Saber expressar opinião de forma matizada — com certeza, dúvida, concordância parcial — "
    "é o que diferencia o falante intermediário do avançado. "
    "Esta unidade treina o italiano do debate, da argumentação e da negociação."
)
u['inventario'] = [
    "Opinião forte: sono convinto/a che + congiuntivo / è ovvio che / non c'è dubbio che",
    "Opinião suave: mi sembra che + congiuntivo / ho l'impressione che / potrebbe essere che",
    "Concordar: sono d'accordo / hai ragione / assolutamente / esattamente / per forza",
    "Discordar: non sono d'accordo / non mi convince / anzi / tutt'al contrario / mi permetta",
    "Concessão: hai ragione, però… / capisco il punto, ma… / in parte sì, ma…",
    "Intensificadores: decisamente / assolutamente / per niente / affatto / tutt'altro",
    "Congiuntivo dubitativo: dubito che sia / non credo che abbia / è improbabile che venga",
    "Struttura retorica: inizio (tesi) → sviluppo (argomenti) → conclusione (rafforzamento)"
]
u['definicao'] = {
    "fenomeno": (
        "Você está numa discussão sobre o futuro do trabalho remoto com colegas italianos. "
        "Um diz: *'Sono convinto che lo smart working abbia migliorato la qualità della vita.'* "
        "Outro responde: *'Non mi convince del tutto — mi sembra che si perda il senso di squadra.'*"
    ),
    "causa": (
        "Por que *abbia migliorato* e *si perda* estão no congiuntivo? "
        "Não seriam fatos objetivos? "
        "Qual é a diferença entre *sono convinto che* + congiuntivo "
        "e *è dimostrato che* + indicativo?"
    ),
    "conceito": (
        "**Verbi di opinione soggettiva** (credere, pensare, ritenere, essere convinto) "
        "requerem **congiuntivo** na subordinada — a opinião é subjetiva, não verificável. "
        "**Fatti oggettivi** (è dimostrato, è certo, è ovvio) usam **indicativo** — "
        "o falante apresenta como verdade objetiva. "
        "A escolha do modo verbal sinaliza o grau de certeza do falante."
        )
}
u['tecnica'] = (
    "**Como expressar e defender opinião em italiano:**\n\n"
    "1. Opinião subjetiva: **credo/penso/sono convinto che** + congiuntivo\n"
    "2. Fato objetivo: **è certo/è dimostrato/è evidente che** + indicativo\n"
    "3. Dúvida: **dubito che / non credo che** + congiuntivo\n"
    "4. Concessão elegante: *hai ragione sul fatto che…, tuttavia…*\n"
    "5. Contraposição: **d'altra parte / eppure / tuttavia / nonostante ciò**\n"
    "6. Reforço: *e non solo… ma anche* | *oltre a ciò* | *a maggior ragione*"
)
u['exemplos_prc'] = [
    {
        "oracao": "Sono convinto che il cambiamento climatico sia la sfida principale del nostro tempo.",
        "pergunta": "Por que *sia* (congiuntivo) e não *è* (indicativo)?",
        "resposta": "sono convinto che = verbo di opinione soggettiva → congiuntivo. Se fosse 'è dimostrato che', usaria indicativo (è)",
        "conclusao": "opinione soggettiva → congiuntivo | fatto oggettivo → indicativo"
    },
    {
        "oracao": "Capisco il tuo punto, però non mi convince del tutto.",
        "pergunta": "Que estratégia argumentativa está sendo usada aqui? Como funciona *però*?",
        "resposta": "Concessão + contraposição: reconhece o argumento do outro (capisco) antes de discordar (però non mi convince). Però = 'mas/porém' — mais suave que 'ma'",
        "conclusao": "concessão + però = discordância educada que preserva o diálogo"
    },
    {
        "oracao": "Non credo affatto che questa soluzione funzioni.",
        "pergunta": "O que adiciona *affatto* à frase? Pode ser usado com frases afirmativas?",
        "resposta": "affatto = absolutamente/de forma alguma. Com negação (non… affatto) = intensifica a negação. NÃO se usa em frases afirmativas (erro comum)",
        "conclusao": "non… affatto = intensificador de negação (≠ 'totalmente' em frases afirmativas)"
    }
]
u['ponte'] = (
    "**Em português:** 'Acredito que seja o maior desafio' — congiuntivo também!\n\n"
    "**Em italiano:** *credo che sia* — estrutura paralela. "
    "Ambas as línguas usam subjuntivo/congiuntivo após verbos de opinião subjetiva.\n\n"
    "**Vantagem:** o padrão é o mesmo que em português. A dificuldade é lembrar "
    "quais verbos italianos são 'de opinião' e quais são 'de fato'."
)
u['coda'] = (
    "Pratique escrevendo textos argumentativos curtos (10 linhas) sobre temas do cotidiano. "
    "A argumentação em italiano se aprende escrevendo — não apenas lendo."
)

# ─── b1-v: L'italiano regionale e i dialetti ───
u = next(x for x in b1['unidades'] if x['id'] == 'b1-v')
u['alerta'] = (
    "O italiano que você aprendeu é o *italiano standard* — falado em TV e contextos formais. "
    "Mas o italiano real, na rua, varia enormemente de região para região. "
    "Esta unidade prepara você para entender e navegar essa diversidade linguística."
)
u['inventario'] = [
    "Variedades: italiano standard / italiano regionale / dialetto / vernacolo",
    "Regiões linguísticas: fiorentino (base do standard), napoletano, siciliano, veneziano, milanese",
    "Traços regionais: cadenza (sotaque), vocabolario regionale, costruzione sintattica locale",
    "Dialeto vs italiano: il dialetto è una lingua autonoma / l'accento regionale è una variante",
    "Verbo RICONOSCERE: riconosco un accento / si riconosce subito che è del Sud",
    "Si impersonale: in Italia si parla molto in dialetto / si capisce facilmente",
    "Espressioni dialettali entrate nell'italiano: ammazzare (uccidere), casino (disordine)",
    "Code-switching: passare dall'italiano al dialetto secondo il contesto"
]
u['definicao'] = {
    "fenomeno": (
        "Você chega a Napoli e não entende metade do que as pessoas falam entre si. "
        "Em Firenze, entende tudo perfeitamente. "
        "Um napolitano diz: *'Mo ce ne jammo?'* — e você não reconhece nem uma palavra."
    ),
    "causa": (
        "Napolitano é uma variante do italiano ou uma língua diferente? "
        "Por que Firenze é mais fácil de entender para quem aprendeu italiano standard? "
        "E o que é exatamente um *accento regionale* vs um *dialetto*?"
    ),
    "conceito": (
        "O **italiano standard** foi baseado no toscano do século XIV (Dante, Petrarca, Boccaccio). "
        "Por isso o fiorentino moderno é o mais próximo do italiano estudado. "
        "**Dialetti** como o napoletano e o siciliano são sistemas linguísticos autônomos "
        "com gramática própria, não 'italiano errado'. "
        "**Accento regionale** = italiano standard com sotaque e vocabulário local."
    )
}
u['tecnica'] = (
    "**Como reconhecer e lidar com variantes regionais:**\n\n"
    "1. Reconhecer sotaque: Norte = vogais fechadas, ritmo rápido | Sul = vogais abertas, ritmo mais lento\n"
    "2. Si impersonale para generalizar: *in Sicilia si mangia benissimo* | *a Milano si lavora molto*\n"
    "3. Quando não entender: *Scusi, non ho capito. Può ripetere più lentamente?*\n"
    "   ou: *Parla italiano standard? Non capisco bene il dialetto.*\n"
    "4. Expressões regionais comuns no italiano: *casino* (confusão/bagunça) | *ammazzare* (matar, mas também interjeição)\n"
    "5. Para pesquisa: cada região tem portal online com glossário dialetal — útil para turismo"
)
u['exemplos_prc'] = [
    {
        "oracao": "In Italia si parla ancora molto in dialetto, soprattutto tra le generazioni anziane.",
        "pergunta": "O que é o *si* impersonale? Como se forma e o que indica?",
        "resposta": "si + verbo 3ª pessoa = sujeito indeterminado (equivale a 'se fala', 'falam', 'as pessoas falam'). Indica ação sem agente específico",
        "conclusao": "si + verbo (3ª sg.) = impessoal — sujeito genérico/indeterminado"
    },
    {
        "oracao": "Il napoletano non è un italiano scorretto — è una lingua autonoma con una sua grammatica.",
        "pergunta": "Como a estrutura *non è… — è…* funciona argumentativamente?",
        "resposta": "Nega uma definição errada e substitui por uma correta — estratégia retórica de redefinição: 'não é X, é Y'",
        "conclusao": "non è A — è B = estrutura de redefinição/correção de equívoco"
    },
    {
        "oracao": "Si riconosce subito da dove viene: ha una cadenza inconfondibile.",
        "pergunta": "O que é *cadenza* neste contexto? É diferente de *accento*?",
        "resposta": "cadenza = melodia, ritmo da fala (entonação). accento = pronúncia específica de sons. Cadenza é mais sobre o ritmo musical da fala, accento sobre os fonemas",
        "conclusao": "cadenza = melodia/ritmo | accento = pronúncia/fonemas"
    }
]
u['ponte'] = (
    "**Em português:** 'No Brasil se fala português com sotaques muito diferentes do Norte ao Sul.'\n\n"
    "**Em italiano:** *In Italia si parla con accenti molto diversi da Nord a Sud* — paralelo quase perfeito.\n\n"
    "**Diferença importante:** os dialetos italianos têm uma autonomia linguística muito maior "
    "que as variações regionais do português brasileiro — o napoletano e o veneziano são "
    "essencialmente línguas diferentes do italiano, não apenas sotaques."
)
u['coda'] = (
    "Ouça músicas, podcasts e vídeos de diferentes regiões da Itália. "
    "O ouvido se acostuma com a variação regional muito antes do que você pensa."
)

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Módulo B1 atualizado com campos NMA.")
