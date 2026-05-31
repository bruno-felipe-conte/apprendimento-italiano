"""
Adiciona campos NMA às 5 unidades do módulo A2.
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

PATH = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"
with open(PATH, encoding='utf-8') as f:
    data = json.load(f)

a2 = next(m for m in data['moduli'] if m['id'] == 'A2')

# ─── a2-i: Al ristorante e al bar ───
u = next(x for x in a2['unidades'] if x['id'] == 'a2-i')
u['alerta'] = (
    "Esta unidade cobre as situações mais comuns da vida cotidiana italiana: "
    "pedir comida, escolher bebidas, pagar a conta. "
    "Dominar essas expressões abre portas — literalmente — em qualquer estabelecimento da Itália."
)
u['inventario'] = [
    "Ordinare: Vorrei / Prendo / Mi porta… per favore",
    "Chiedere il conto: Il conto, per favore / Posso pagare?",
    "Verbo VOLERE (condizionale): vorrei (eu gostaria), vorresti, vorrebbe",
    "Verbo PRENDERE (pres.): prendo, prendi, prende, prendiamo, prendete, prendono",
    "Articolo partitivo: del vino / della birra / degli spaghetti / delle olive",
    "Espressioni tipiche: un tavolo per due / è compreso il servizio? / buon appetito",
    "Differença: bar italiano ≠ bar brasileiro — si va al bar per il caffè, non per la birra",
    "Avverbi di quantità: un po' di / abbastanza / molto / troppo"
]
u['definicao'] = {
    "fenomeno": (
        "Você entra em um ristorante em Roma. O cameriere vem até a sua mesa. "
        "Você quer pedir um prato de pasta e uma água mineral. "
        "O que você diz? Como pede educadamente?"
    ),
    "causa": (
        "Em italiano, pedir algo diretamente (*'voglio la pasta'*) soa brusco. "
        "Qual é a forma educada de pedir? "
        "O que é o *articolo partitivo* e quando se usa *del* vs *della* vs *degli*?"
    ),
    "conceito": (
        "Use **vorrei** (condicional de volere) para pedidos educados. "
        "O **articolo partitivo** (del/della/dello/dei/degli/delle) indica quantidade indefinida, "
        "equivalente a 'um pouco de / alguns'. "
        "Combina artigo determinativo + preposição *di*: *di + il = del*, *di + la = della*."
    )
}
u['tecnica'] = (
    "**Como pedir no ristorante / bar:**\n\n"
    "1. Para pedir educadamente: **vorrei** + artigo + produto → *Vorrei un caffè / Vorrei la pasta al pomodoro*\n"
    "2. Alternativa informal: **prendo** + artigo → *Prendo una pizza margherita*\n"
    "3. Articolo partitivo: *di + il/lo/la/i/gli/le* → del/dello/della/dei/degli/delle\n"
    "   → masculino singular com vowel: **dell'** | masculino -o: **del** | feminino -a: **della**\n"
    "4. Pedir a conta: *Il conto, per favore* — nunca *'voglio il conto'* (brusco)\n"
    "5. Expressão de aprovação: *Buonissimo! / È molto buono* — sempre bem recebido"
)
u['exemplos_prc'] = [
    {
        "oracao": "Vorrei un tavolo per due, per favore.",
        "pergunta": "Por que *vorrei* e não *voglio*? Qual é a diferença de registro?",
        "resposta": "vorrei é o condicional — mais educado e suave; voglio é direto e pode soar brusco",
        "conclusao": "condicional vorrei = forma educada de pedir"
    },
    {
        "oracao": "Prendo degli spaghetti e dell'acqua minerale.",
        "pergunta": "O que são *degli* e *dell'*? Por que não *i* e *l'*?",
        "resposta": "degli e dell' são artigos partitivos — indicam quantidade indefinida ('uns espaguetes', 'um pouco de água')",
        "conclusao": "partitivo di+art = quantidade indefinida"
    },
    {
        "oracao": "È compreso il servizio? — Sì, è già incluso.",
        "pergunta": "Como se pergunta se a gorjeta já está incluída na conta?",
        "resposta": "È compreso il servizio? — literalmente 'o serviço está incluído?'",
        "conclusao": "serviço = gorjeta em contexto de restaurante italiano"
    }
]
u['ponte'] = (
    "**Em português:** 'Quero um café / Pode me trazer a conta?' — direto ao ponto.\n\n"
    "**Em italiano:** o condicional *vorrei* substitui o imperativo em pedidos formais, "
    "assim como em português dizemos 'gostaria de' em vez de 'quero' numa situação elegante.\n\n"
    "**Armadilha:** *un caffè* na Itália = expresso curto (30ml), não café coado. "
    "Se quiser algo maior, diga *caffè americano* ou *caffè lungo*."
)
u['coda'] = (
    "Decorar frases prontas funciona no início, mas a fluência vem de entender "
    "por que *vorrei* soa melhor que *voglio*. Pratique o condicional além do restaurante."
)

# ─── a2-ii: Trasporti e orientamento ───
u = next(x for x in a2['unidades'] if x['id'] == 'a2-ii')
u['alerta'] = (
    "Saber se locomover e perguntar o caminho são habilidades de sobrevivência. "
    "Esta unidade dá as ferramentas para chegar a qualquer lugar na Itália "
    "sem depender de aplicativos — e para entender as respostas que você receber."
)
u['inventario'] = [
    "Meios de transporte: l'autobus, il treno, la metropolitana (il metro), il taxi, la bicicletta",
    "Pedir informações: Scusi, come si arriva a…? / Dov'è la stazione?",
    "Indicar direção: a destra / a sinistra / dritto / sempre dritto / al semaforo",
    "Distância/tempo: È vicino? / È lontano? / ci vogliono 10 minuti a piedi",
    "Comprar bilhete: Un biglietto per… / Un biglietto di andata e ritorno",
    "Verbo ANDARE (pres.): vado, vai, va, andiamo, andate, vanno",
    "Preposizioni di luogo: vicino a, lontano da, davanti a, dietro a, accanto a, di fronte a",
    "CI con andare: ci vado (eu vou lá), ci andiamo (vamos lá)"
]
u['definicao'] = {
    "fenomeno": (
        "Você está em Firenze e precisa chegar ao Duomo. "
        "Para um passante na rua e pergunta o caminho. "
        "Ele responde: *'Vada sempre dritto, poi giri a sinistra al semaforo — è lì davanti.'*"
    ),
    "causa": (
        "Você entendeu *dritto* e *sinistra*, mas o que é *vada*? "
        "Por que não disse *vai*? "
        "Qual é a diferença entre *vicino* e *vicino a*?"
    ),
    "conceito": (
        "**Vada** é o imperativo formal (Lei) de andare — usado quando se dirige a um desconhecido. "
        "Para amigos: *vai dritto*. "
        "**Vicino** é advérbio (está perto), **vicino a** é preposição (perto de + lugar específico)."
    )
}
u['tecnica'] = (
    "**Como dar e entender direções:**\n\n"
    "1. Pedir: *Scusi* (formal) / *Senti* (informal) + *dov'è…?* ou *come si arriva a…?*\n"
    "2. Direções básicas: **dritto** (em frente) | **a destra** (direita) | **a sinistra** (esquerda) | **giri** (vire)\n"
    "3. Referências: *al semaforo* (no semáforo) | *all'angolo* (na esquina) | *dopo la chiesa* (depois da igreja)\n"
    "4. Tempo a pé: *ci vogliono X minuti a piedi* — literalmente 'são precisos X minutos a pé'\n"
    "5. Bilhete: *Un biglietto per [destino], per favore* | *andata e ritorno* = ida e volta"
)
u['exemplos_prc'] = [
    {
        "oracao": "Scusi, dov'è la fermata dell'autobus?",
        "pergunta": "Por que *Scusi* e não *Scusa*? Qual é a regra de uso?",
        "resposta": "Scusi é o imperativo formal (Lei) — usado com desconhecidos adultos; Scusa é informal (tu)",
        "conclusao": "Scusi (formal/desconhecido) ≠ Scusa (informal/amigos)"
    },
    {
        "oracao": "Ci vogliono venti minuti a piedi.",
        "pergunta": "O que significa *ci vogliono*? Por que está no plural?",
        "resposta": "ci vogliono = 'são necessários' — o verbo concorda com 'venti minuti' (plural)",
        "conclusao": "ci vuole (singular) / ci vogliono (plural) = levar X tempo/ser necessário"
    },
    {
        "oracao": "La stazione è di fronte all'albergo.",
        "pergunta": "O que é *all'albergo*? Por que a contração?",
        "resposta": "a + l'albergo = all'albergo — preposição a + artigo l' (elide antes de vogal)",
        "conclusao": "a + il = al | a + l' = all' | a + lo = allo"
    }
]
u['ponte'] = (
    "**Em português:** 'Vá em frente, depois vire à esquerda' — estrutura idêntica.\n\n"
    "**Em italiano:** a ordem é a mesma, mas atenção ao imperativo formal: "
    "*vada* (Lei) vs *vai* (tu). Em situações de rua com desconhecidos, sempre use a forma formal.\n\n"
    "**Diferença cultural:** na Itália é comum os locais acompanharem você um trecho do caminho "
    "se a rua for complicada — *La accompagno fino all'angolo.*"
)
u['coda'] = (
    "Aprenda pelo menos: *Scusi, dov'è…? / sempre dritto / a destra / a sinistra / grazie mille.* "
    "Essas 6 expressões resolvem 80% das situações de orientação."
)

# ─── a2-iii: Lavoro e vita professionale ───
u = next(x for x in a2['unidades'] if x['id'] == 'a2-iii')
u['alerta'] = (
    "O italiano profissional tem registro próprio: mais formal, mais estruturado. "
    "Esta unidade prepara para entrevistas, e-mails e conversas no ambiente de trabalho — "
    "contextos onde um erro de registro pode custar uma oportunidade."
)
u['inventario'] = [
    "Apresentar-se: Mi chiamo… / Sono… / Lavoro come… / Ho esperienza in…",
    "Perguntar sobre trabalho: Che lavoro fai? / Dove lavori? / Da quanto tempo?",
    "Profissioni: il medico, l'avvocato, l'ingegnere, il professore, l'impiegato, il commesso",
    "CV: la formazione scolastica, l'esperienza lavorativa, le competenze, i riferimenti",
    "Verbo LAVORARE (pres.): lavoro, lavori, lavora, lavoriamo, lavorate, lavorano",
    "Da + tempo: lavoro qui da tre anni (faz três anos que trabalho aqui)",
    "Formule email: In riferimento a… / Le scrivo per… / In attesa di una Sua risposta",
    "Registro formal: Lei (você formal) vs tu (informal)"
]
u['definicao'] = {
    "fenomeno": (
        "Você está em um colloquio di lavoro em Milano. "
        "O selezionatore pergunta: *'Da quanto tempo lavora nel settore?'* "
        "Você precisa responder sobre sua experiência."
    ),
    "causa": (
        "Como se expressa duração contínua em italiano? "
        "*'Lavoro qui da tre anni'* — por que *da* e não *per*? "
        "Qual é a diferença entre os dois?"
    ),
    "conceito": (
        "**Da + presente** indica ação que começou no passado e continua agora: "
        "*lavoro qui da tre anni* = faz três anos que trabalho aqui (e ainda trabalho). "
        "**Per + tempo** indica duração completa/passada: *ho lavorato lì per due anni* = trabalhei lá por dois anos. "
        "A diferença é aspectual: continuidade (da) vs conclusão (per)."
    )
}
u['tecnica'] = (
    "**Como falar sobre trabalho e experiência:**\n\n"
    "1. Duração contínua: **da + presente** → *studio italiano da sei mesi* (há 6 meses, ainda estudo)\n"
    "2. Duração passada/concluída: **per + passato prossimo** → *ho lavorato lì per due anni*\n"
    "3. Profissione: *faccio il/la + profissão* ou *sono + profissão* (sem artigo)\n"
    "   → *faccio il medico* / *sono medico* — ambas corretas\n"
    "4. Email formal: início com *In riferimento a* / *Le scrivo per* + infinito\n"
    "5. Colloquio: *Ho esperienza in + área* | *So usare + ferramenta* | *Parlo + idioma*"
)
u['exemplos_prc'] = [
    {
        "oracao": "Lavoro in questa azienda da cinque anni.",
        "pergunta": "Por que o verbo está no presente se a ação começou 5 anos atrás?",
        "resposta": "Em italiano, da + presente indica ação iniciada no passado que AINDA continua — diferente do português 'há 5 anos que trabalho'",
        "conclusao": "da + presente = ação contínua desde o passado até hoje"
    },
    {
        "oracao": "Sono ingegnere / Faccio l'ingegnere.",
        "pergunta": "Por que *sono ingegnere* não tem artigo, mas *faccio l'ingegnere* tem?",
        "resposta": "Com ESSERE + profissão: sem artigo. Com FARE + profissão: com artigo determinativo",
        "conclusao": "essere + profissão (sem artigo) | fare + l'/il/la + profissão (com artigo)"
    },
    {
        "oracao": "In attesa di una Sua risposta, porgo distinti saluti.",
        "pergunta": "Por que *Sua* está com maiúscula? E o que é *porgo distinti saluti*?",
        "resposta": "Sua com maiúscula = pronome formal de cortesia (Lei). 'Porgo distinti saluti' = fórmula de fechamento formal (equivalente a 'atenciosamente')",
        "conclusao": "Lei/Suo com maiúscula = máximo formalidade em e-mails"
    }
]
u['ponte'] = (
    "**Em português:** 'Trabalho aqui há três anos' — presente + 'há'.\n\n"
    "**Em italiano:** *Lavoro qui da tre anni* — mesma estrutura (presente + *da*).\n\n"
    "**Armadilha:** *da* e *per* ambos traduzem 'por', mas *da* = continuidade (ainda em curso), "
    "*per* = duração concluída. Não os confunda em contexto de trabalho."
)
u['coda'] = (
    "O vocabulário profissional italiano é mais formal que o cotidiano. "
    "Invista tempo nos e-mails formais — eles revelam nível de língua de forma imediata."
)

# ─── a2-iv: Casa e quartiere ───
u = next(x for x in a2['unidades'] if x['id'] == 'a2-iv')
u['alerta'] = (
    "Descrever onde você mora, os cômodos da casa e o bairro são "
    "temas de conversa universal. Esta unidade é também uma porta de entrada "
    "para o vocabulário do cotidiano doméstico italiano."
)
u['inventario'] = [
    "Cômodos: la cucina, il bagno, il salotto / il soggiorno, la camera da letto, lo studio, il balcone",
    "Móveis: il divano, il letto, l'armadio, la scrivania, il tavolo, la sedia, lo scaffale",
    "Descritores: spazioso/a, luminoso/a, rumoroso/a, antico/a, moderno/a, accogliente",
    "Affittare/comprare: in affitto / di proprietà / il contratto / il canone mensile / il deposito",
    "Verbo ABITARE: abito, abiti, abita, abitiamo, abitate, abitano",
    "CI come pronome di luogo: ci abito da due anni (moro lá há dois anos)",
    "Preposizioni: al primo piano / al piano terra / in centro / in periferia / vicino al parco",
    "Espressioni: c'è / ci sono / manca / mancano (para descrever o que tem/falta)"
]
u['definicao'] = {
    "fenomeno": (
        "Você está procurando apartamento em Bologna e lê o anúncio: "
        "*'Appartamento luminoso, due camere, cucina abitabile, bagno, balcone, "
        "al terzo piano senza ascensore, zona centrale, 800€/mese + spese.'* "
        "Você entende tudo?"
    ),
    "causa": (
        "O que é *cucina abitabile*? "
        "O que significa *spese*? "
        "Como se diz 'tem elevador?' e como perguntar se os vizinhos são barulhentos?"
    ),
    "conceito": (
        "**Cucina abitabile** = cozinha grande o suficiente para comer (com mesa). "
        "**Spese** = despesas de condomínio. "
        "Para existência: *c'è l'ascensore?* (singular) / *ci sono posti auto?* (plural). "
        "Para falta: *manca il riscaldamento* (falta aquecimento) / *mancano le finestre* (faltam janelas)."
    )
}
u['tecnica'] = (
    "**Como descrever e perguntar sobre moradia:**\n\n"
    "1. Existência: **c'è** + singular | **ci sono** + plural → *c'è il garage? / ci sono due bagni?*\n"
    "2. Falta: **manca** + singular | **mancano** + plural → *manca il riscaldamento*\n"
    "3. Localização no edifício: **al + piano ordinale** → *al primo piano / al terzo piano*\n"
    "   → Atenção: *piano terra* = térreo (sem artigo)\n"
    "4. Aluguel: *in affitto* (alugado) | *di proprietà* (próprio) | *cerco casa in affitto*\n"
    "5. Descrever: **è** + adjetivo → *è luminoso, è grande, è rumoroso*"
)
u['exemplos_prc'] = [
    {
        "oracao": "L'appartamento è al secondo piano con ascensore.",
        "pergunta": "Como se diz 'no terceiro andar' e 'no térreo' em italiano?",
        "resposta": "al terzo piano / al piano terra — note que piano terra não usa número ordinal",
        "conclusao": "piano terra (térreo) | al primo/secondo/terzo piano (1°/2°/3° andar)"
    },
    {
        "oracao": "Ci abito da tre anni e mi trovo molto bene.",
        "pergunta": "O que faz *ci* nessa frase? Pode ser omitido?",
        "resposta": "ci = partícula de lugar que substitui 'lì/là' (lá). Sem ci: 'Abito qui da tre anni' — possível, mas ci evita a repetição",
        "conclusao": "ci di luogo = lá/aqui (pronome locativo que evita repetição)"
    },
    {
        "oracao": "Manca il riscaldamento — fa molto freddo d'inverno.",
        "pergunta": "Por que *manca* e não *non c'è*? São intercambiáveis?",
        "resposta": "manca enfatiza a falta como problema; non c'è é mais neutro (simplesmente não existe)",
        "conclusao": "manca = falta (com nuance de inconveniência) | non c'è = não há (neutro)"
    }
]
u['ponte'] = (
    "**Em português:** 'Moro no segundo andar / Falta aquecimento' — estrutura direta.\n\n"
    "**Em italiano:** *abito al secondo piano / manca il riscaldamento* — paralelo preciso.\n\n"
    "**Diferença cultural:** na Itália o *piano terra* (térreo) = 0, *primo piano* = 1° andar brasileiro. "
    "Cuidado ao combinar apartamentos — o que eles chamam de 'primo piano' é o que chamamos de segundo andar."
)
u['coda'] = (
    "Leia anúncios reais de imóveis italianos online — são o melhor treino para este vocabulário "
    "porque combinam vocabulário, gramática e cultura em situação autêntica."
)

# ─── a2-v: Salute e farmacia ───
u = next(x for x in a2['unidades'] if x['id'] == 'a2-v')
u['alerta'] = (
    "Saber comunicar sintomas e entender instruções médicas pode ser literalmente vital. "
    "Esta unidade cobre o vocabulário de sobrevivência para situações de saúde "
    "— da farmácia à emergência."
)
u['inventario'] = [
    "Sintomas: ho mal di testa/stomaco/gola/schiena / ho la febbre / mi fa male il/la…",
    "Dal medico: ho un appuntamento / mi sento male / da quanto tempo? / ho mal di…",
    "Farmacia: ho bisogno di… / ha qualcosa per…? / posologia / la ricetta / senza ricetta",
    "Parti del corpo: la testa, il collo, la spalla, il braccio, la mano, il petto, la schiena, la gamba, il piede",
    "Verbo FARE MALE: mi fa male la testa / mi fanno male i denti (concorda com a parte do corpo)",
    "Stare + aggettivo: sto bene / sto male / come stai? / non mi sento bene",
    "Dovere + infinito: devo prendere la medicina / deve riposare",
    "Emergência: chiami il 118 / pronto soccorso / ambulanza / urgente"
]
u['definicao'] = {
    "fenomeno": (
        "Você está em Napoli e acorda com dor de cabeça forte e febre. "
        "Vai à farmácia e o farmacista pergunta: *'Come si sente? Che sintomi ha?'* "
        "Você precisa descrever o que sente."
    ),
    "causa": (
        "Como se diz 'estou com dor de cabeça'? "
        "*Ho mal di testa* ou *mi fa male la testa*? São iguais? "
        "E se doer mais de uma coisa ao mesmo tempo?"
    ),
    "conceito": (
        "**Ho mal di + parte** = expressão fixa para dores comuns (di testa, di stomaco, di gola). "
        "**Mi fa male + parte singular** / **mi fanno male + parte plural** = verbo *fare male* "
        "que concorda com a parte do corpo dolorida, não com a pessoa. "
        "Ambas as formas são corretas e intercambiáveis na prática."
    )
}
u['tecnica'] = (
    "**Como descrever sintomas e pedir ajuda:**\n\n"
    "1. Dor fixa: **ho mal di** + parte → *ho mal di testa / gola / schiena / stomaco*\n"
    "2. Dor variável: **mi fa male** + singular | **mi fanno male** + plural\n"
    "   → *mi fa male il ginocchio* | *mi fanno male le gambe*\n"
    "3. Temperatura: **ho la febbre** (tenho febre) | **ho 38 di febbre** (tenho 38 de febre)\n"
    "4. Pedir remédio: **ha qualcosa per** + il/la + sintoma → *ha qualcosa per il mal di testa?*\n"
    "5. Urgência: *chiami il 118* (chame o 118) | *ho bisogno di un medico subito*"
)
u['exemplos_prc'] = [
    {
        "oracao": "Ho mal di stomaco da ieri sera.",
        "pergunta": "Por que *da ieri sera* e não *da* + número? Como indicar 'desde ontem à noite'?",
        "resposta": "da + referência temporal (ieri sera, stamattina, lunedì) indica desde quando a situação persiste",
        "conclusao": "da + momento específico = desde [aquele momento] até agora"
    },
    {
        "oracao": "Mi fanno male i denti — devo andare dal dentista.",
        "pergunta": "Por que *fanno* (plural) e não *fa* (singular)?",
        "resposta": "fare male concorda com a parte do corpo: i denti = plural → fanno",
        "conclusao": "mi FA male il/la (singular) | mi FANNO male i/le (plural)"
    },
    {
        "oracao": "Ha qualcosa senza ricetta per il raffreddore?",
        "pergunta": "O que é *senza ricetta*? E por que *Ha* com maiúscula?",
        "resposta": "senza ricetta = sem receita médica. Ha com maiúscula = forma formal Lei (você formal) — o farmacista é um desconhecido adulto",
        "conclusao": "Ha (Lei formal) = você formal na farmácia/médico"
    }
]
u['ponte'] = (
    "**Em português:** 'Estou com dor de cabeça' — direto.\n\n"
    "**Em italiano:** *ho mal di testa* (literalmente 'tenho mal de cabeça') "
    "— estrutura diferente do português que usa 'estar com'.\n\n"
    "**Armadilha:** nunca diga *sono mal di testa* (erro comum de brasileiros). "
    "Use sempre **ho** (tenho) para dores e sintomas, não **sono** (sou/estou)."
)
u['coda'] = (
    "Memorize pelo menos: *ho mal di testa, ho la febbre, mi fa male, ho bisogno di un medico, chiami il 118.* "
    "Em emergência, essas frases valem mais que todo o resto."
)

with open(PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Módulo A2 atualizado com campos NMA.")
