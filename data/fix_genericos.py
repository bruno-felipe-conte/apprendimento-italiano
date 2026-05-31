import json
import re

PATH = r"C:\Users\bruno\Documents\italian-learning-app-pro\data\grammar.json"

# Real content keyed by lezione ID
# Each entry: {"armadilhas": [...], "tabela_visual": "...html..."}
# For B1 lezioni only tabela_visual is provided (armadilhas already correct)

CONTENT = {

    # ─── A1 ───────────────────────────────────────────────────────────────────

    "a1-lez3": {
        "armadilhas": [
            {
                "errado": "Vado a il mercato.",
                "certo": "Vado al mercato.",
                "motivo": "'A' + 'il' se contrai em 'al'. As preposições simples se combinam com os artigos definidos para formar preposições articuladas."
            },
            {
                "errado": "Vengo da la Francia.",
                "certo": "Vengo dalla Francia.",
                "motivo": "'Da' + 'la' = 'dalla'. Toda preposição simples (di, a, da, in, su, con) se contrai com os artigos definidos."
            },
            {
                "errado": "Il libro è su il tavolo.",
                "certo": "Il libro è sul tavolo.",
                "motivo": "'Su' + 'il' = 'sul'. Nunca use a preposição simples sozinha antes de artigo definido — use sempre a forma contraída."
            }
        ],
        "tabela_visual": """<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Prep.</th><th>il</th><th>lo</th><th>la</th><th>i</th><th>gli</th><th>le</th><th>l'</th></tr>
<tr><td><strong>di</strong></td><td>del</td><td>dello</td><td>della</td><td>dei</td><td>degli</td><td>delle</td><td>dell'</td></tr>
<tr><td><strong>a</strong></td><td>al</td><td>allo</td><td>alla</td><td>ai</td><td>agli</td><td>alle</td><td>all'</td></tr>
<tr><td><strong>da</strong></td><td>dal</td><td>dallo</td><td>dalla</td><td>dai</td><td>dagli</td><td>dalle</td><td>dall'</td></tr>
<tr><td><strong>in</strong></td><td>nel</td><td>nello</td><td>nella</td><td>nei</td><td>negli</td><td>nelle</td><td>nell'</td></tr>
<tr><td><strong>su</strong></td><td>sul</td><td>sullo</td><td>sulla</td><td>sui</td><td>sugli</td><td>sulle</td><td>sull'</td></tr>
<tr><td><strong>con</strong></td><td>col*</td><td>—</td><td>—</td><td>coi*</td><td>—</td><td>—</td><td>—</td></tr>
</table>
<br><small>*col/coi são opcionais e menos usados. "Per", "tra/fra" <strong>não</strong> formam preposições articuladas.</small>"""
    },

    "A1-04": {
        "armadilhas": [
            {
                "errado": "Ho andato al cinema.",
                "certo": "Sono andato al cinema.",
                "motivo": "Verbos de movimento (andare, venire, arrivare, partire, tornare) usam ESSERE, não avere, no passato prossimo. Com essere, o participio concorda com o sujeito."
            },
            {
                "errado": "Maria ha venuta tardi.",
                "certo": "Maria è venuta tardi.",
                "motivo": "'Venire' exige ESSERE. O participio 'venuto' concorda com o sujeito feminino → 'venuta'."
            },
            {
                "errado": "Ho mangiato la pizza? No, non ho mangiato.",
                "certo": "Hai mangiato la pizza? No, non ho mangiato.",
                "motivo": "Na pergunta para 'tu', use 'hai' (2ª pessoa), não 'ho' (1ª pessoa). Erro de conjugação de avere."
            }
        ],
        "tabela_visual": """<strong>Passato Prossimo = avere/essere + participio passato</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Com AVERE (transitivos)</th><th>Com ESSERE (intransitivos/movim.)</th></tr>
<tr><td>ho mangiato</td><td>sono andato/a</td></tr>
<tr><td>hai lavorato</td><td>sei venuto/a</td></tr>
<tr><td>ha studiato</td><td>è partito/a</td></tr>
<tr><td>abbiamo visto</td><td>siamo arrivati/e</td></tr>
<tr><td>avete fatto</td><td>siete tornati/e</td></tr>
<tr><td>hanno detto</td><td>sono stati/e</td></tr>
</table>
<br><strong>Participios irregulares frequentes:</strong><br>
fare→fatto | dire→detto | vedere→visto | scrivere→scritto | leggere→letto | aprire→aperto | venire→venuto | essere→stato"""
    },

    "A1-05": {
        "armadilhas": [
            {
                "errado": "Ci vado spesso a Roma.",
                "certo": "Ci vado spesso. / Vado spesso a Roma.",
                "motivo": "'Ci' substitui o lugar já mencionado. Se você menciona 'a Roma' explicitamente, não precisa do 'ci' — seria redundante."
            },
            {
                "errado": "Ci sono due libro sul tavolo.",
                "certo": "Ci sono due libri sul tavolo.",
                "motivo": "'Ci sono' é correto para plural, mas atenção ao plural do substantivo: 'libro' → 'libri'."
            },
            {
                "errado": "Non ci capisco niente di questo.",
                "certo": "Non ci capisco niente. / Non capisco niente di questo.",
                "motivo": "Na expressão 'non ci capisco niente' (não entendo nada disso), 'ci' já indica o assunto. Evite duplicar com 'di questo'."
            }
        ],
        "tabela_visual": """<strong>A partícula CI — usos principais</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Uso</th><th>Exemplo</th><th>Significado</th></tr>
<tr><td>Lugar (lá/aqui)</td><td>Ci vado domani.</td><td>Vou lá amanhã.</td></tr>
<tr><td>Existência</td><td>C'è un problema.</td><td>Há um problema.</td></tr>
<tr><td>Existência plural</td><td>Ci sono molte persone.</td><td>Há muitas pessoas.</td></tr>
<tr><td>Com "volere"</td><td>Ci vuole un'ora.</td><td>Leva uma hora.</td></tr>
<tr><td>Com "mettere"</td><td>Ci metto dieci minuti.</td><td>Levo dez minutos.</td></tr>
<tr><td>Expressão fixa</td><td>Non ci capisco niente.</td><td>Não entendo nada disso.</td></tr>
</table>
<br><small>Posição: antes do verbo conjugado ou após o infinito/gerúndio (andarci, pensarci).</small>"""
    },

    "A1-06": {
        "armadilhas": [
            {
                "errado": "Domani io anderò al mercato.",
                "certo": "Domani vado al mercato. / Domani andrò al mercato.",
                "motivo": "No italiano falado, o presente simples é muito usado para futuro próximo. 'Anderò' está gramaticalmente correto, mas soa formal. Atenção: a raiz é 'andr-', não 'ander-'."
            },
            {
                "errado": "Quando avrò finito, chiamerò.",
                "certo": "Quando avrò finito, ti chiamerò.",
                "motivo": "Esta frase está correta! O futuro anteriore (avrò finito) é usado em orações temporais com 'quando'. Não substitua pelo futuro simples na subordinada."
            },
            {
                "errado": "Lei saperà la risposta.",
                "certo": "Lei saprà la risposta.",
                "motivo": "'Sapere' no futuro tem raiz irregular: 'sapr-'. Assim como dovere→dovrà, potere→potrà, volere→vorrà."
            }
        ],
        "tabela_visual": """<strong>Futuro Semplice — terminações regulares</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pessoa</th><th>-ARE (parl-)</th><th>-ERE (vend-)</th><th>-IRE (part-)</th></tr>
<tr><td>io</td><td>parlerò</td><td>venderò</td><td>partirò</td></tr>
<tr><td>tu</td><td>parlerai</td><td>venderai</td><td>partirai</td></tr>
<tr><td>lui/lei</td><td>parlerà</td><td>venderà</td><td>partirà</td></tr>
<tr><td>noi</td><td>parleremo</td><td>venderemo</td><td>partiremo</td></tr>
<tr><td>voi</td><td>parlerete</td><td>venderete</td><td>partirete</td></tr>
<tr><td>loro</td><td>parleranno</td><td>venderanno</td><td>partiranno</td></tr>
</table>
<br><strong>Raízes irregulares frequentes:</strong><br>
essere→sarà | avere→avrà | fare→farà | andare→andrà | venire→verrà | dovere→dovrà | potere→potrà | volere→vorrà | sapere→saprà<br><br>
<strong>Futuro Anteriore</strong> = futuro di avere/essere + participio passato<br>
Ex: <em>Quando avrò mangiato, uscirò.</em> (Quando tiver comido, saio.)"""
    },

    "a1-lez7": {
        "armadilhas": [
            {
                "errado": "Mio fratello e mia sorella sono simpatici.",
                "certo": "Mio fratello e mia sorella sono simpatici.",
                "motivo": "Esta frase está correta! Com parentes no singular sem artigo: 'mio fratello', 'mia sorella'. MAS com alterazioni: 'il mio fratellino' (artigo obrigatório)."
            },
            {
                "errado": "La mia sorella è avvocata.",
                "certo": "Mia sorella è avvocata.",
                "motivo": "Com parentes próximos no singular (fratello, sorella, madre, padre, figlio), o possessivo NÃO leva artigo. Exceções: loro (sempre com artigo) e aumentativos/diminutivos."
            },
            {
                "errado": "Il suo cappello è bello — di chi è? È mio cappello.",
                "certo": "Il suo cappello è bello — di chi è? È il mio cappello.",
                "motivo": "Quando o possessivo está no predicado (após 'essere'), o artigo é obrigatório: 'È il mio', 'È la tua', etc."
            }
        ],
        "tabela_visual": """<strong>Aggettivi possessivi — concordância com o substantivo</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pessoa</th><th>Masc. sing.</th><th>Fem. sing.</th><th>Masc. plur.</th><th>Fem. plur.</th></tr>
<tr><td>io</td><td>il mio</td><td>la mia</td><td>i miei</td><td>le mie</td></tr>
<tr><td>tu</td><td>il tuo</td><td>la tua</td><td>i tuoi</td><td>le tue</td></tr>
<tr><td>lui/lei</td><td>il suo</td><td>la sua</td><td>i suoi</td><td>le sue</td></tr>
<tr><td>noi</td><td>il nostro</td><td>la nostra</td><td>i nostri</td><td>le nostre</td></tr>
<tr><td>voi</td><td>il vostro</td><td>la vostra</td><td>i vostri</td><td>le vostre</td></tr>
<tr><td>loro</td><td>il loro</td><td>la loro</td><td>i loro</td><td>le loro</td></tr>
</table>
<br><strong>Parentes próximos no singular → sem artigo:</strong> mio padre, mia madre, mio fratello, mia sorella, mio figlio<br>
<strong>Exceções (com artigo):</strong> il loro padre | il mio fratellino | i miei fratelli"""
    },

    "a1-lez8": {
        "armadilhas": [
            {
                "errado": "Lo vedo Maria ogni giorno.",
                "certo": "La vedo ogni giorno. / Vedo Maria ogni giorno.",
                "motivo": "'Maria' é feminino → pronome 'la', não 'lo'. E o pronome vem ANTES do verbo conjugado, sem repetir o nome."
            },
            {
                "errado": "Voglio vederlo domani il film.",
                "certo": "Voglio vederlo domani.",
                "motivo": "Quando o pronome está anexado ao infinito ('vederlo'), não repita o objeto ('il film') — seria redundante."
            },
            {
                "errado": "Non lo vedo mai lui.",
                "certo": "Non lo vedo mai.",
                "motivo": "O pronome 'lo' já substitui 'lui' como objeto. Na língua padrão, não repita o referente ao mesmo tempo que o pronome clítico."
            }
        ],
        "tabela_visual": """<strong>Pronomi diretti (oggetto diretto)</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pessoa</th><th>Pronome</th><th>Exemplo</th></tr>
<tr><td>io</td><td>mi</td><td>Marco mi chiama. (me)</td></tr>
<tr><td>tu</td><td>ti</td><td>Ti aspetto alle 8. (te)</td></tr>
<tr><td>lui</td><td>lo</td><td>Lo vedo spesso. (o/ele)</td></tr>
<tr><td>lei</td><td>la</td><td>La chiamo domani. (a/ela)</td></tr>
<tr><td>noi</td><td>ci</td><td>Il prof ci saluta. (nos)</td></tr>
<tr><td>voi</td><td>vi</td><td>Vi invito alla festa. (vos)</td></tr>
<tr><td>loro (m.)</td><td>li</td><td>Li conosco bene. (os)</td></tr>
<tr><td>loro (f.)</td><td>le</td><td>Le aspetto fuori. (as)</td></tr>
</table>
<br><strong>Posição:</strong> antes do verbo conjugado | anexado ao infinito/imperativo/gerúndio<br>
<em>Lo mangio. / Voglio mangiarlo. / Mangiatelo!</em>"""
    },

    "a1-lez9": {
        "armadilhas": [
            {
                "errado": "Quando ero piccolo, ho giocato ogni giorno.",
                "certo": "Quando ero piccolo, giocavo ogni giorno.",
                "motivo": "O imperfetto descreve ações habituais ou situações contínuas no passado. 'Ho giocato' (passato prossimo) indica ação concluída pontual — errado aqui."
            },
            {
                "errado": "Ieri ho lavorato mentre mangiavo.",
                "certo": "Ieri lavoravo mentre mangiavo. / Ieri, mentre mangiavo, ho ricevuto una chiamata.",
                "motivo": "O imperfetto descreve o 'pano de fundo' (o que estava acontecendo), e o passato prossimo a ação que interrompe. Use os dois em contraste."
            },
            {
                "errado": "Da bambino, io essere molto timido.",
                "certo": "Da bambino, ero molto timido.",
                "motivo": "O imperfetto de 'essere' é: ero, eri, era, eravamo, eravate, erano. Nunca use o infinito no lugar da forma conjugada."
            }
        ],
        "tabela_visual": """<strong>Imperfetto Indicativo — quando usar e como formar</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pessoa</th><th>parlare</th><th>leggere</th><th>capire</th><th>essere</th></tr>
<tr><td>io</td><td>parlavo</td><td>leggevo</td><td>capivo</td><td>ero</td></tr>
<tr><td>tu</td><td>parlavi</td><td>leggevi</td><td>capivi</td><td>eri</td></tr>
<tr><td>lui/lei</td><td>parlava</td><td>leggeva</td><td>capiva</td><td>era</td></tr>
<tr><td>noi</td><td>parlavamo</td><td>leggevamo</td><td>capivamo</td><td>eravamo</td></tr>
<tr><td>voi</td><td>parlavate</td><td>leggevate</td><td>capivate</td><td>eravate</td></tr>
<tr><td>loro</td><td>parlavano</td><td>leggevano</td><td>capivano</td><td>erano</td></tr>
</table>
<br><strong>Usos do imperfetto:</strong> hábito passado | estado/descrição | ação em progresso | cortesia (Volevo un caffè.)"""
    },

    "a1-lez10": {
        "armadilhas": [
            {
                "errado": "Ti do il libro a tu.",
                "certo": "Ti do il libro.",
                "motivo": "'Ti' já é o pronome indireto de 'tu' (a te). Não repita 'a tu' — além de redundante, 'tu' não é forma tônica correta isolada; seria 'a te'."
            },
            {
                "errado": "Gli telefono a lei ogni sera.",
                "certo": "Le telefono ogni sera.",
                "motivo": "'Gli' é pronome indireto de 'lui' (a lui). Para 'lei' (feminino), use 'le'. 'Telefonare' rege objeto indireto."
            },
            {
                "errado": "Ho detto lui la verità.",
                "certo": "Gli ho detto la verità.",
                "motivo": "O pronome indireto vem ANTES do verbo auxiliar no passato prossimo. 'Lui' não pode ser usado como objeto indireto sem preposição 'a'."
            }
        ],
        "tabela_visual": """<strong>Pronomi indiretti (oggetto indiretto = a + persona)</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pessoa</th><th>Pronome</th><th>Exemplo</th></tr>
<tr><td>a me</td><td>mi</td><td>Mi scrivi spesso? (para mim)</td></tr>
<tr><td>a te</td><td>ti</td><td>Ti mando un messaggio. (para você)</td></tr>
<tr><td>a lui</td><td>gli</td><td>Gli parlo domani. (para ele)</td></tr>
<tr><td>a lei</td><td>le</td><td>Le ho dato il libro. (para ela)</td></tr>
<tr><td>a noi</td><td>ci</td><td>Ci hanno risposto. (para nós)</td></tr>
<tr><td>a voi</td><td>vi</td><td>Vi spiego tutto. (para vocês)</td></tr>
<tr><td>a loro</td><td>gli / loro</td><td>Gli scrivo. / Scrivo loro. (para eles)</td></tr>
</table>
<br><strong>Verbos comuns com indireto:</strong> dare, dire, scrivere, mandare, telefonare, rispondere, chiedere, spiegare, piacere"""
    },

    "a1-lez11": {
        "armadilhas": [
            {
                "errado": "Te lo dò a tu.",
                "certo": "Te lo do.",
                "motivo": "O pronome combinado 'te lo' já expressa 'a te + lo'. Não adicione 'a tu' — é redundante e agramatical."
            },
            {
                "errado": "Mi lo dai?",
                "certo": "Me lo dai?",
                "motivo": "Quando 'mi' precede um pronome direto (lo, la, li, le), transforma-se em 'me': me lo, me la, me li, me le."
            },
            {
                "errado": "Glielo ho dato ieri lei.",
                "certo": "Gliel'ho dato ieri. / Glielo ho dato ieri.",
                "motivo": "'Glielo' já combina 'gli/le + lo'. Não repita o referente. Antes de 'ho', 'glielo' pode elidir: 'gliel'ho'."
            }
        ],
        "tabela_visual": """<strong>Pronomi combinati (indiretto + diretto)</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Indiretto</th><th>+ lo</th><th>+ la</th><th>+ li</th><th>+ le</th><th>+ ne</th></tr>
<tr><td>mi → <strong>me</strong></td><td>me lo</td><td>me la</td><td>me li</td><td>me le</td><td>me ne</td></tr>
<tr><td>ti → <strong>te</strong></td><td>te lo</td><td>te la</td><td>te li</td><td>te le</td><td>te ne</td></tr>
<tr><td>gli/le → <strong>glie</strong></td><td>glielo</td><td>gliela</td><td>glieli</td><td>gliele</td><td>gliene</td></tr>
<tr><td>ci → <strong>ce</strong></td><td>ce lo</td><td>ce la</td><td>ce li</td><td>ce le</td><td>ce ne</td></tr>
<tr><td>vi → <strong>ve</strong></td><td>ve lo</td><td>ve la</td><td>ve li</td><td>ve le</td><td>ve ne</td></tr>
<tr><td>gli(loro) → <strong>glie</strong></td><td>glielo</td><td>gliela</td><td>glieli</td><td>gliele</td><td>gliene</td></tr>
</table>
<br><strong>Posição:</strong> antes do verbo conjugado, ou anexado ao infinito/imperativo.<br>
<em>Te lo mando. / Voglio mandartelo. / Mandamelo!</em>"""
    },

    "a1-lez12": {
        "armadilhas": [
            {
                "errado": "Io mi sveglio e poi lavo le mani.",
                "certo": "Io mi sveglio e poi mi lavo le mani.",
                "motivo": "'Lavarsi le mani' é verbo reflexivo — o pronome 'mi' é obrigatório antes do verbo. Sem ele, a frase é incompleta ou muda de sentido."
            },
            {
                "errado": "Ieri ho alzato alle sette.",
                "certo": "Ieri mi sono alzato alle sette.",
                "motivo": "Verbos reflexivos no passato prossimo usam ESSERE (não avere) + pronome reflexivo. O participio concorda com o sujeito: alzato (m.) / alzata (f.)."
            },
            {
                "errado": "Loro si chiamano Marco e Anna — loro si piacciono.",
                "certo": "Loro si chiamano Marco e Anna — si vogliono bene.",
                "motivo": "'Piacersi' existe, mas 'si piacciono' significa 'eles se acham atraentes'. Para 'eles se gostam (se dão bem)' use 'si vogliono bene' ou 'vanno d'accordo'."
            }
        ],
        "tabela_visual": """<strong>Verbi riflessivi — presente e passato prossimo</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pessoa</th><th>Presente (alzarsi)</th><th>Passato prossimo</th></tr>
<tr><td>io</td><td>mi alzo</td><td>mi sono alzato/a</td></tr>
<tr><td>tu</td><td>ti alzi</td><td>ti sei alzato/a</td></tr>
<tr><td>lui/lei</td><td>si alza</td><td>si è alzato/a</td></tr>
<tr><td>noi</td><td>ci alziamo</td><td>ci siamo alzati/e</td></tr>
<tr><td>voi</td><td>vi alzate</td><td>vi siete alzati/e</td></tr>
<tr><td>loro</td><td>si alzano</td><td>si sono alzati/e</td></tr>
</table>
<br><strong>Verbos reflexivos comuns:</strong> alzarsi, svegliarsi, lavarsi, vestirsi, pettinarsi, addormentarsi, sentirsi, chiamarsi, sposarsi, divertirsi"""
    },

    "a1-lez13": {
        "armadilhas": [
            {
                "errado": "Se potrei, viaggerei di più.",
                "certo": "Se potessi, viaggerei di più.",
                "motivo": "No período hipotético irreal, a oração com 'se' usa o congiuntivo imperfetto (potessi), nunca o condizionale (potrei)."
            },
            {
                "errado": "Vorrebbe un caffè, per favore?",
                "certo": "Vorrei un caffè, per favore.",
                "motivo": "'Vorrei' (1ª pessoa) é usado para pedir educadamente. 'Vorrebbe' é 3ª pessoa — seria usado para pedir em nome de outra pessoa."
            },
            {
                "errado": "Avrei voluto andare, ma non ho potuto.",
                "certo": "Avrei voluto andare, ma non ho potuto. ✓",
                "motivo": "Esta frase está correta! O condizionale composto (avrei voluto) expressa algo que se teria desejado no passado mas não aconteceu."
            }
        ],
        "tabela_visual": """<strong>Condizionale Presente — terminações</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pessoa</th><th>parlare</th><th>avere</th><th>essere</th></tr>
<tr><td>io</td><td>parlerei</td><td>avrei</td><td>sarei</td></tr>
<tr><td>tu</td><td>parleresti</td><td>avresti</td><td>saresti</td></tr>
<tr><td>lui/lei</td><td>parlerebbe</td><td>avrebbe</td><td>sarebbe</td></tr>
<tr><td>noi</td><td>parleremmo</td><td>avremmo</td><td>saremmo</td></tr>
<tr><td>voi</td><td>parlereste</td><td>avreste</td><td>sareste</td></tr>
<tr><td>loro</td><td>parlerebbero</td><td>avrebbero</td><td>sarebbero</td></tr>
</table>
<br><strong>Condizionale Composto</strong> = condizionale di avere/essere + participio<br>
<em>Avrei mangiato. / Sarei andato/a.</em><br><br>
<strong>Usos:</strong> pedidos educados (vorrei) | hipóteses (se potessi, viaggerei) | desejo no passado (avrei voluto)"""
    },

    "a1-lez14": {
        "armadilhas": [
            {
                "errado": "La persona che ho parlato è simpatica.",
                "certo": "La persona con cui ho parlato è simpatica.",
                "motivo": "'Parlare' rege 'con' → o relativo deve incluir a preposição: 'con cui'. 'Che' só substitui sujeito ou objeto direto."
            },
            {
                "errado": "Chi è quella ragazza? È la ragazza che il suo nome è Sofia.",
                "certo": "Chi è quella ragazza? È la ragazza il cui nome è Sofia.",
                "motivo": "Para expressar posse na oração relativa, use 'il cui / la cui / i cui / le cui' (= cujo/cuja). Nunca 'che + possessivo'."
            },
            {
                "errado": "Dove abiti? Abito in Roma.",
                "certo": "Dove abiti? Abito a Roma.",
                "motivo": "Cidades usam a preposição 'a' (a Roma, a Firenze). 'In' é para países, regiões e lugares maiores (in Italia, in Toscana)."
            }
        ],
        "tabela_visual": """<strong>Pronomi relativi</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pronome</th><th>Uso</th><th>Exemplo</th></tr>
<tr><td><strong>che</strong></td><td>sujeito ou obj. direto</td><td>Il libro che leggo è bello.</td></tr>
<tr><td><strong>cui</strong></td><td>com preposição</td><td>La persona a cui scrivo. / con cui parlo.</td></tr>
<tr><td><strong>il cui / la cui</strong></td><td>posse (cujo/cuja)</td><td>Lo studente il cui padre è medico.</td></tr>
<tr><td><strong>quello che / ciò che</strong></td><td>o que (neutro)</td><td>Quello che dici è vero.</td></tr>
</table>
<br><strong>Pronomi interrogativi:</strong><br>
chi? (quem) | che cosa? / cosa? (o quê) | quale/i? (qual/quais) | quanto/a/i/e? (quanto/a/os/as)<br>
<em>Chi sei? Cosa vuoi? Quale preferisci? Quanti anni hai?</em>"""
    },

    "a1-lez15": {
        "armadilhas": [
            {
                "errado": "Marco è più alto di quanto Luigi.",
                "certo": "Marco è più alto di Luigi.",
                "motivo": "Comparação entre dois substantivos/pronomes: use 'di' simples. 'Di quanto' é usado antes de verbo: 'È più intelligente di quanto pensassi'."
            },
            {
                "errado": "Questa pizza è la più buona del mondo.",
                "certo": "Questa pizza è la migliore del mondo.",
                "motivo": "'Buono' tem superlativo irregular: buono→migliore (relativo) / ottimo (absoluto). Evite 'il più buono' em contextos formais."
            },
            {
                "errado": "Roma è tanto bella che Firenze.",
                "certo": "Roma è tanto bella quanto Firenze.",
                "motivo": "Na comparação de igualdade com adjetivo: 'tanto...quanto' ou 'così...come'. 'Tanto...che' indica consequência (talmente... que)."
            }
        ],
        "tabela_visual": """<strong>Comparativo e Superlativo</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Tipo</th><th>Estrutura</th><th>Exemplo</th></tr>
<tr><td>Comp. maioria</td><td>più + agg. + di/che</td><td>Marco è più alto di Luca.</td></tr>
<tr><td>Comp. minoria</td><td>meno + agg. + di/che</td><td>È meno caro che in centro.</td></tr>
<tr><td>Comp. igualdade</td><td>tanto...quanto / così...come</td><td>È tanto brava quanto lui.</td></tr>
<tr><td>Superlat. relativo</td><td>il/la più + agg. + di</td><td>È il più bello della classe.</td></tr>
<tr><td>Superlat. assoluto</td><td>agg. + -issimo/a</td><td>Questa torta è buonissima!</td></tr>
</table>
<br><strong>Irregulari:</strong><br>
buono → migliore / ottimo | cattivo → peggiore / pessimo<br>
grande → maggiore / massimo | piccolo → minore / minimo"""
    },

    "a1-lez16": {
        "armadilhas": [
            {
                "errado": "Garibaldi ha unificato l'Italia.",
                "certo": "Garibaldi unificò l'Italia. (registro histórico formal)",
                "motivo": "O passato remoto é preferido na língua escrita e no sul da Itália para fatos históricos distantes. No norte, o passato prossimo é mais comum mesmo para eventos remotos."
            },
            {
                "errado": "Ieri io andai al cinema.",
                "certo": "Ieri sono andato/a al cinema.",
                "motivo": "No italiano do norte e falado, 'ieri' (ontem) usa passato prossimo. O passato remoto para 'ieri' é aceitável apenas no sul da Itália."
            },
            {
                "errado": "Lui nascì a Roma.",
                "certo": "Lui nacque a Roma.",
                "motivo": "'Nascere' tem passato remoto irregular: nacqui, nascesti, nacque, nascemmo, nasceste, nacquero."
            }
        ],
        "tabela_visual": """<strong>Passato Remoto — terminações regulares</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pessoa</th><th>parlare</th><th>credere</th><th>finire</th></tr>
<tr><td>io</td><td>parlai</td><td>credei/credetti</td><td>finii</td></tr>
<tr><td>tu</td><td>parlasti</td><td>credesti</td><td>finisti</td></tr>
<tr><td>lui/lei</td><td>parlò</td><td>credé/credette</td><td>finì</td></tr>
<tr><td>noi</td><td>parlammo</td><td>credemmo</td><td>finimmo</td></tr>
<tr><td>voi</td><td>parlaste</td><td>credeste</td><td>finiste</td></tr>
<tr><td>loro</td><td>parlarono</td><td>crederono/credettero</td><td>finirono</td></tr>
</table>
<br><strong>Irregolari comuni:</strong> essere→fu | avere→ebbe | fare→fece | dire→disse | venire→venne | vedere→vide | scrivere→scrisse | nascere→nacque | prendere→prese"""
    },

    "a1-lez17": {
        "armadilhas": [
            {
                "errado": "Quando arrivai, lui partiva già.",
                "certo": "Quando arrivai, lui era già partito.",
                "motivo": "O trapassato prossimo (era partito) indica uma ação anterior a outra ação no passado. O imperfetto 'partiva' não expressa anterioridade concluída."
            },
            {
                "errado": "Non avevo mai visto questo film prima.",
                "certo": "Non avevo mai visto questo film prima. ✓",
                "motivo": "Frase correta! O trapassato com 'mai' expressa experiência (ou falta dela) até um momento passado. Compare com 'Non ho mai visto' (até agora)."
            },
            {
                "errado": "Dopo che ho mangiato, uscii.",
                "certo": "Dopo che ebbi mangiato, uscii. / Dopo aver mangiato, uscii.",
                "motivo": "Após 'dopo che' em contexto narrativo formal com passato remoto, usa-se o trapassato remoto (ebbi mangiato). Na língua moderna, prefira 'dopo aver + participio'."
            }
        ],
        "tabela_visual": """<strong>Trapassato Prossimo = imperfetto di avere/essere + participio</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pessoa</th><th>Con AVERE (mangiare)</th><th>Con ESSERE (andare)</th></tr>
<tr><td>io</td><td>avevo mangiato</td><td>ero andato/a</td></tr>
<tr><td>tu</td><td>avevi mangiato</td><td>eri andato/a</td></tr>
<tr><td>lui/lei</td><td>aveva mangiato</td><td>era andato/a</td></tr>
<tr><td>noi</td><td>avevamo mangiato</td><td>eravamo andati/e</td></tr>
<tr><td>voi</td><td>avevate mangiato</td><td>eravate andati/e</td></tr>
<tr><td>loro</td><td>avevano mangiato</td><td>erano andati/e</td></tr>
</table>
<br><strong>Uso:</strong> ação passada anterior a outra ação passada.<br>
<em>Quando sono arrivato, loro avevano già mangiato.</em><br>
(Quando cheguei, eles já tinham comido.)"""
    },

    "a1-lez18": {
        "armadilhas": [
            {
                "errado": "Abito in via Roma, 5.",
                "certo": "Abito in via Roma, 5. ✓ / Abito a via Roma, 5.",
                "motivo": "'In via' é o mais comum para endereços (in via Roma, in piazza Navona). 'A' também existe regionalmente, mas 'in' é preferido."
            },
            {
                "errado": "Vado in farmacia a comprare medicine.",
                "certo": "Vado in farmacia a comprare medicine. ✓",
                "motivo": "Correto! Com lugares sem artigo (in farmacia, in banca, in ufficio, in centro), usa-se 'in'. Com artigo definido, usa-se 'a': vado al supermercato."
            },
            {
                "errado": "Ho studiato per tre anni fa.",
                "certo": "Ho studiato tre anni fa.",
                "motivo": "'Fa' significa 'atrás' (há X tempo). Não usa 'per' antes: 'tre anni fa' (três anos atrás). 'Per' indica duração: 'ho studiato per tre anni'."
            }
        ],
        "tabela_visual": """<strong>Preposizioni — usos essenciais</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Prep.</th><th>Uso principal</th><th>Exemplos</th></tr>
<tr><td><strong>di</strong></td><td>posse, matéria, origem</td><td>il libro di Marco | un bicchiere di vino | sono di Roma</td></tr>
<tr><td><strong>a</strong></td><td>lugar (cidade), destino, hora</td><td>a Roma | vado a casa | alle tre</td></tr>
<tr><td><strong>da</strong></td><td>origem, desde, duração, finalidade</td><td>vengo da Milano | da tre anni | da bere</td></tr>
<tr><td><strong>in</strong></td><td>país/região, lugar sem art., meio</td><td>in Italia | in ufficio | in treno</td></tr>
<tr><td><strong>con</strong></td><td>companhia, instrumento</td><td>con Marco | con il coltello</td></tr>
<tr><td><strong>su</strong></td><td>em cima de, sobre (tema)</td><td>sul tavolo | un libro su Roma</td></tr>
<tr><td><strong>per</strong></td><td>destino, duração, finalidade</td><td>parto per Roma | per tre ore | studio per imparare</td></tr>
<tr><td><strong>tra/fra</strong></td><td>entre, daqui a (tempo)</td><td>tra amici | tra due ore</td></tr>
</table>"""
    },

    "a1-lez19": {
        "armadilhas": [
            {
                "errado": "Penso che lui è stanco.",
                "certo": "Penso che lui sia stanco.",
                "motivo": "Após verbos de opinião, sentimento e dúvida (pensare, credere, sperare), usa-se o congiuntivo presente na oração subordinada."
            },
            {
                "errado": "Dopo che mangio, guarderei la TV.",
                "certo": "Dopo che mangio, guardo la TV. / Dopo aver mangiato, guardo la TV.",
                "motivo": "A concordância exige coerência temporal. Se a principal está no presente, a subordinada também usa presente ou infinito perfeito."
            },
            {
                "errado": "Speravo che veniva.",
                "certo": "Speravo che venisse.",
                "motivo": "Com o verbo principal no passado (speravo), a oração com 'che' usa o congiuntivo imperfetto (venisse), não l'imperfetto indicativo."
            }
        ],
        "tabela_visual": """<strong>Concordanza dei tempi — regra geral</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Verbo principale</th><th>Azione contemporanea</th><th>Azione anteriore</th></tr>
<tr><td>Presente / Futuro</td><td>Congiuntivo presente<br><em>Penso che venga.</em></td><td>Congiuntivo passato<br><em>Penso che sia venuto.</em></td></tr>
<tr><td>Passato / Condizionale</td><td>Congiuntivo imperfetto<br><em>Pensavo che venisse.</em></td><td>Congiuntivo trapassato<br><em>Pensavo che fosse venuto.</em></td></tr>
</table>
<br><strong>Verbos que regem congiuntivo:</strong> pensare, credere, sperare, temere, volere, preferire, è necessario che, è possibile che, benché, sebbene, affinché, prima che"""
    },

    "a1-lez20": {
        "armadilhas": [
            {
                "errado": "Se avrei tempo, viaggerei.",
                "certo": "Se avessi tempo, viaggerei.",
                "motivo": "No período hipotético irreal (presente/futuro), a condição usa il congiuntivo imperfetto (avessi), nunca il condizionale. A consequência usa il condizionale presente."
            },
            {
                "errado": "Se avrei saputo, sarei venuto.",
                "certo": "Se avessi saputo, sarei venuto.",
                "motivo": "No período hipotético irreal passado, a condição usa il congiuntivo trapassato (avessi saputo) e a consequência il condizionale composto (sarei venuto)."
            },
            {
                "errado": "Se studi, passeresti l'esame.",
                "certo": "Se studi, passerai l'esame.",
                "motivo": "No período hipotético reale (situação possível), a condição usa l'indicativo presente e a consequência usa il futuro simples (ou presente). O condizionale é para situações ipotetiche."
            }
        ],
        "tabela_visual": """<strong>Periodo Ipotetico — três tipos</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Tipo</th><th>Condição (se...)</th><th>Consequência</th><th>Exemplo</th></tr>
<tr><td><strong>Reale</strong> (possível)</td><td>Indicativo presente</td><td>Futuro / Presente</td><td>Se studi, passerai l'esame.</td></tr>
<tr><td><strong>Ipotetico</strong> (improvável)</td><td>Congiuntivo imperfetto</td><td>Condizionale presente</td><td>Se studiassi, passeresti.</td></tr>
<tr><td><strong>Irreale</strong> (impossível)</td><td>Congiuntivo trapassato</td><td>Condizionale composto</td><td>Se avessi studiato, avresti passato.</td></tr>
</table>
<br><strong>Regra de ouro:</strong> nunca use il condizionale após 'se'. Sempre use il congiuntivo ou l'indicativo."""
    },

    "a1-lez21": {
        "armadilhas": [
            {
                "errado": "Essendo stanco, ho andato a letto.",
                "certo": "Essendo stanco, sono andato a letto.",
                "motivo": "'Andare' usa sempre ESSERE no passato prossimo. O gerúndio 'essendo stanco' está correto, mas o verbo principal mantém seu auxiliar normal."
            },
            {
                "errado": "Ho visto lui correndo in via.",
                "certo": "L'ho visto correre in via.",
                "motivo": "Com verbos di percezione (vedere, sentire, ascoltare), a estrutura correta é verbo + oggetto + infinito, não gerúndio."
            },
            {
                "errado": "Il bambino dormito è tranquillo.",
                "certo": "Il bambino che dorme è tranquillo. / Il bambino addormentato è tranquillo.",
                "motivo": "'Dormito' é participio passato, não presente. Para função adjetivale ativa, use una proposizione relativa ou um participio adjetivale como 'addormentato'."
            }
        ],
        "tabela_visual": """<strong>Gerundio e Participio — usi principali</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Forma</th><th>Come si forma</th><th>Uso</th><th>Esempio</th></tr>
<tr><td><strong>Gerundio presente</strong></td><td>-ando / -endo</td><td>Ação simultânea / modo</td><td>Studiando, impari. / Sto mangiando.</td></tr>
<tr><td><strong>Gerundio passato</strong></td><td>avendo/essendo + part.</td><td>Ação anterior</td><td>Avendo mangiato, uscì.</td></tr>
<tr><td><strong>Participio presente</strong></td><td>-ante / -ente</td><td>Adjetivo / nome</td><td>un libro interessante | un insegnante</td></tr>
<tr><td><strong>Participio passato</strong></td><td>-ato / -uto / -ito</td><td>Tempos compostos / adj.</td><td>Ho mangiato. / la porta aperta</td></tr>
</table>
<br><strong>Stare + gerundio</strong> = ação em progresso: <em>Sto studiando.</em> / <em>Stava dormendo.</em>"""
    },

    "a1-lez22": {
        "armadilhas": [
            {
                "errado": "Il problema è risolvuto.",
                "certo": "Il problema è risolto.",
                "motivo": "'Risolvere' tem participio passato irregular: risolto. Muitos verbos em -ere têm participios irregulares que devem ser memorizados."
            },
            {
                "errado": "La lettera è scritta da me ieri.",
                "certo": "La lettera è stata scritta da me ieri.",
                "motivo": "Para ação passada na voz passiva, use 'essere' + 'stato/a' + participio. 'È scritta' indica um estado atual, não uma ação passada."
            },
            {
                "errado": "Il film ha visto da molti.",
                "certo": "Il film è stato visto da molti.",
                "motivo": "A voz passiva em italiano usa ESSERE (não avere) + participio passato. O participio concorda com o sujeito (film = masc. sing. → visto)."
            }
        ],
        "tabela_visual": """<strong>Forma Passiva — struttura e tempi</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Tempo</th><th>Struttura</th><th>Esempio</th></tr>
<tr><td>Presente</td><td>essere (pres.) + part.</td><td>Il libro è letto da tutti.</td></tr>
<tr><td>Imperfetto</td><td>essere (imperf.) + part.</td><td>La porta era aperta.</td></tr>
<tr><td>Passato prossimo</td><td>essere stato/a + part.</td><td>Il film è stato visto.</td></tr>
<tr><td>Futuro</td><td>essere (fut.) + part.</td><td>La lettera sarà spedita.</td></tr>
<tr><td>Condizionale</td><td>essere (cond.) + part.</td><td>Sarebbe fatto meglio.</td></tr>
</table>
<br><strong>Alternativa con "venire"</strong> (somente tempi semplici):<br>
<em>Il pacco viene consegnato domani.</em> (mais dinâmico)<br><br>
<strong>Alternativa con "si" passivante:</strong><br>
<em>Si vende casa. / Si parlano molte lingue.</em>"""
    },

    "a1-lez23": {
        "armadilhas": [
            {
                "errado": "Devo di andare adesso.",
                "certo": "Devo andare adesso.",
                "motivo": "Os verbos modais (dovere, potere, volere, sapere) são seguidos diretamente pelo infinito, SEM preposição."
            },
            {
                "errado": "Non posso venire — non voglio.",
                "certo": "Non posso venire — non voglio venire. / Non posso venire, e non voglio.",
                "motivo": "Quando o segundo modal tem o mesmo infinito, pode-se omitir. Mas 'non voglio' sozinho, sem contexto, deixa a frase incompleta numa negativa formal."
            },
            {
                "errado": "Ho dovuto di finire il lavoro.",
                "certo": "Ho dovuto finire il lavoro.",
                "motivo": "Mesmo no passato prossimo, os modais são seguidos pelo infinito sem preposição. O auxiliar (avere/essere) depende do verbo principal: 'sono potuto andare' ou 'ho potuto andare' (ambos aceitos)."
            }
        ],
        "tabela_visual": """<strong>Verbi modali — presente indicativo</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Pessoa</th><th>dovere</th><th>potere</th><th>volere</th><th>sapere</th></tr>
<tr><td>io</td><td>devo</td><td>posso</td><td>voglio</td><td>so</td></tr>
<tr><td>tu</td><td>devi</td><td>puoi</td><td>vuoi</td><td>sai</td></tr>
<tr><td>lui/lei</td><td>deve</td><td>può</td><td>vuole</td><td>sa</td></tr>
<tr><td>noi</td><td>dobbiamo</td><td>possiamo</td><td>vogliamo</td><td>sappiamo</td></tr>
<tr><td>voi</td><td>dovete</td><td>potete</td><td>volete</td><td>sapete</td></tr>
<tr><td>loro</td><td>devono</td><td>possono</td><td>vogliono</td><td>sanno</td></tr>
</table>
<br><strong>dovere</strong> = dever/ter que | <strong>potere</strong> = poder | <strong>volere</strong> = querer | <strong>sapere</strong> = saber (fazer algo)<br>
<em>Tutti i modali + infinito senza preposizione.</em>"""
    },

    "a1-lez24": {
        "armadilhas": [
            {
                "errado": "Mi lo dai?",
                "certo": "Me lo dai?",
                "motivo": "Quando 'mi' precede um pronome diretto (lo, la, li, le, ne), transforma-se em 'me'. Mesma regra para ti→te, ci→ce, vi→ve."
            },
            {
                "errado": "Glielo do a lei.",
                "certo": "Glielo do.",
                "motivo": "'Glielo' já combina o indiretto (le = a lei) e o diretto (lo). Não repita 'a lei' — seria redundante."
            },
            {
                "errado": "Voglio darlo gli.",
                "certo": "Voglio darglielo.",
                "motivo": "Quando o pronome é anexado ao infinito, o indiretto e o diretto se combinam como único pronome. 'Dargli' + 'lo' = 'darglielo'."
            }
        ],
        "tabela_visual": """<strong>Pronomi combinati — tabela completa</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Indiretto</th><th>+lo</th><th>+la</th><th>+li</th><th>+le</th><th>+ne</th></tr>
<tr><td>mi → me</td><td>me lo</td><td>me la</td><td>me li</td><td>me le</td><td>me ne</td></tr>
<tr><td>ti → te</td><td>te lo</td><td>te la</td><td>te li</td><td>te le</td><td>te ne</td></tr>
<tr><td>gli/le → glie</td><td>glielo</td><td>gliela</td><td>glieli</td><td>gliele</td><td>gliene</td></tr>
<tr><td>ci → ce</td><td>ce lo</td><td>ce la</td><td>ce li</td><td>ce le</td><td>ce ne</td></tr>
<tr><td>vi → ve</td><td>ve lo</td><td>ve la</td><td>ve li</td><td>ve le</td><td>ve ne</td></tr>
<tr><td>loro → glie</td><td>glielo</td><td>gliela</td><td>glieli</td><td>gliele</td><td>gliene</td></tr>
</table>
<br><strong>Com verbo modale + infinito:</strong> pronomi antes do modale <em>o</em> anexados ao infinito.<br>
<em>Te lo voglio dare. = Voglio dartelo.</em>"""
    },

    "a1-lez25": {
        "armadilhas": [
            {
                "errado": "Ha detto: «Sono stanco» → Ha detto che era stanco.",
                "certo": "Ha detto che era stanco. ✓",
                "motivo": "Correto! No discorso indiretto, o presente vira imperfetto quando o verbo introdutório está no passato."
            },
            {
                "errado": "Mi ha chiesto: «Dove vai?» → Mi ha chiesto dove andavo.",
                "certo": "Mi ha chiesto dove andavo. ✓",
                "motivo": "Correto! Perguntas indiretas com parola interrogativa (dove, come, quando) usam l'ordine normale (non invertito) e concordância temporal."
            },
            {
                "errado": "Ha detto: «Vieni domani!» → Ha detto di venire ieri.",
                "certo": "Ha detto di venire il giorno dopo. / Ha detto che dovevo venire il giorno dopo.",
                "motivo": "No discorso indiretto, os advérbios de tempo mudam: domani → il giorno dopo | ieri → il giorno prima | oggi → quel giorno | qui → lì."
            }
        ],
        "tabela_visual": """<strong>Discorso Indiretto — trasformazioni principali</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Discorso diretto</th><th>Discorso indiretto</th></tr>
<tr><td>Presente → «parlo»</td><td>Imperfetto → diceva che parlava</td></tr>
<tr><td>Passato prossimo → «ho parlato»</td><td>Trapassato → disse che aveva parlato</td></tr>
<tr><td>Futuro → «parlerò»</td><td>Condizionale → disse che avrebbe parlato</td></tr>
<tr><td>Imperativo → «vieni!»</td><td>Infinito → disse di venire</td></tr>
<tr><td>Domanda sì/no → «Vieni?»</td><td>se → chiese se venivo</td></tr>
</table>
<br><strong>Advérbios que mudam:</strong><br>
oggi → quel giorno | ieri → il giorno prima | domani → il giorno dopo | qui/qua → lì/là | questo → quello"""
    },

    "a1-lez26": {
        "armadilhas": [
            {
                "errado": "Sono le tre e mezzo.",
                "certo": "Sono le tre e mezza.",
                "motivo": "'Mezza' (metade) concorda com 'ora' (feminino). Diz-se 'le tre e mezza', não 'mezzo'. Exceção: 'mezzogiorno e mezzo' (o 'mezzo' é adjetivo de 'mezzogiorno', masculino)."
            },
            {
                "errado": "Ho nato il 5 marzo 1990.",
                "certo": "Sono nato il 5 marzo 1990.",
                "motivo": "'Nascere' usa sempre ESSERE, como todos os verbi di moto ou cambiamento di stato. 'Sono nato/a' = nasci."
            },
            {
                "errado": "Il mio compleanno è nel 15 aprile.",
                "certo": "Il mio compleanno è il 15 aprile.",
                "motivo": "Para datas, use o artigo determinativo 'il' (masc.) direto, sem preposição 'in'. Ex: il 3 maggio, l'8 marzo, il 25 dicembre."
            }
        ],
        "tabela_visual": """<strong>Numeri, Data e Ora</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Tema</th><th>Struttura</th><th>Esempi</th></tr>
<tr><td><strong>Ora</strong></td><td>Sono le + numero<br>È l'una / È mezzogiorno</td><td>Sono le otto e un quarto.<br>Sono le dieci meno venti.</td></tr>
<tr><td><strong>Data</strong></td><td>il + giorno + mese (+ anno)</td><td>Oggi è il 15 marzo 2025.<br>L'8 settembre 1943.</td></tr>
<tr><td><strong>Anno</strong></td><td>nel + anno</td><td>Nel 1861 (l'Italia si unificò).</td></tr>
<tr><td><strong>Secolo</strong></td><td>nel + ordinale + secolo</td><td>Nel ventunesimo secolo.</td></tr>
</table>
<br><strong>Numeri ordinali 1-10:</strong> primo, secondo, terzo, quarto, quinto, sesto, settimo, ottavo, nono, decimo<br>
<strong>Mesi:</strong> gennaio, febbraio, marzo, aprile, maggio, giugno, luglio, agosto, settembre, ottobre, novembre, dicembre"""
    },

    "a1-lez27": {
        "armadilhas": [
            {
                "errado": "Non ho visto nessuno persona.",
                "certo": "Non ho visto nessuno. / Non ho visto nessuna persona.",
                "motivo": "'Nessuno' como pronome não leva substantivo. Come aggettivo, concorda com il sostantivo: nessuna persona (f.), nessun problema (m.)."
            },
            {
                "errado": "Qualcuno studenti sono arrivati.",
                "certo": "Alcuni studenti sono arrivati.",
                "motivo": "'Qualcuno' é pronome singular (alguém). Para modificar um substantivo plural, use 'alcuni/alcune' (alguns/algumas)."
            },
            {
                "errado": "Ho mangiato tutto le torte.",
                "certo": "Ho mangiato tutta la torta. / Ho mangiato tutte le torte.",
                "motivo": "'Tutto' concorda com o substantivo: tutto il pane | tutta la torta | tutti i biscotti | tutte le torte."
            }
        ],
        "tabela_visual": """<strong>Indefiniti — pronomi e aggettivi comuni</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Indefinito</th><th>Uso</th><th>Esempio</th></tr>
<tr><td>qualcuno</td><td>pronome sing. (alguém)</td><td>Qualcuno ha chiamato.</td></tr>
<tr><td>qualcosa</td><td>pronome neutro (algo)</td><td>Vuoi qualcosa da mangiare?</td></tr>
<tr><td>alcuni/alcune</td><td>aggettivo/pronome plur.</td><td>Alcuni studenti sono bravi.</td></tr>
<tr><td>nessuno/a</td><td>ninguém / nenhum/a</td><td>Non è venuto nessuno.</td></tr>
<tr><td>ogni</td><td>cada (invariável + sing.)</td><td>Ogni giorno studio.</td></tr>
<tr><td>tutto/a/i/e</td><td>todo/a/os/as</td><td>Tutti i ragazzi / Tutta la classe.</td></tr>
<tr><td>tanto/a/i/e</td><td>muito/a/os/as</td><td>Ho tanti amici.</td></tr>
<tr><td>poco/a, pochi/e</td><td>pouco/a/os/as</td><td>Ho pochi soldi.</td></tr>
</table>"""
    },

    "a1-lez28": {
        "armadilhas": [
            {
                "errado": "Studio italiano perché voglio viaggiare l'Italia.",
                "certo": "Studio italiano perché voglio viaggiare in Italia.",
                "motivo": "'Viaggiare in Italia' (viajar pela Itália). 'In' é a preposição correta com países. E 'perché' com indicativo = porque (causa); com congiuntivo = affinché (para que)."
            },
            {
                "errado": "Sebbene sia stanco, ma continuo a lavorare.",
                "certo": "Sebbene sia stanco, continuo a lavorare.",
                "motivo": "'Sebbene' (embora) já é uma conjunção concessiva — não adicione 'ma'. A estrutura é: sebbene/benché + congiuntivo, [consequência]."
            },
            {
                "errado": "Prima che lui parte, salutalo.",
                "certo": "Prima che lui parta, salutalo.",
                "motivo": "'Prima che' exige o congiuntivo (parta), não l'indicativo (parte). Conjunções temporais que regem congiuntivo: prima che, affinché, benché, sebbene, nonostante."
            }
        ],
        "tabela_visual": """<strong>Congiunzioni e proposizioni subordinate</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Tipo</th><th>Congiunzione</th><th>Modo verbale</th></tr>
<tr><td>Causale</td><td>perché, poiché, dato che, siccome</td><td>Indicativo</td></tr>
<tr><td>Finale</td><td>perché, affinché, in modo che</td><td>Congiuntivo</td></tr>
<tr><td>Temporale</td><td>quando, mentre, dopo che, prima che</td><td>Indic. / prima che→Cong.</td></tr>
<tr><td>Concessiva</td><td>benché, sebbene, nonostante</td><td>Congiuntivo</td></tr>
<tr><td>Condizionale</td><td>se, a condizione che, purché</td><td>Indic. / Cong. imperfetto</td></tr>
<tr><td>Consecutiva</td><td>così...che, talmente...che</td><td>Indicativo</td></tr>
<tr><td>Relativa</td><td>che, cui, il quale</td><td>Indicativo (di norma)</td></tr>
</table>"""
    },

    "a1-lez29": {
        "armadilhas": [
            {
                "errado": "Lui parla italiano buono.",
                "certo": "Lui parla italiano bene.",
                "motivo": "Para modificar um verbo, use l'avverbio 'bene' (bem), não l'aggettivo 'buono' (bom). 'Buono' modifica substantivos: un buono studente."
            },
            {
                "errado": "Ho molto fame.",
                "certo": "Ho molta fame.",
                "motivo": "'Fame' é substantivo feminino → il modificatore deve concordar: 'molta fame'. 'Molto' como avverbio (antes de aggettivo/avverbio) é invariável: molto bello, molto bene."
            },
            {
                "errado": "Cammina lentamente e abile.",
                "certo": "Cammina lentamente e abilmente.",
                "motivo": "Quando dois avverbi in -mente são usados juntos, spesso il primo perde -mente: 'lentamente e abilmente' → 'lentamente e abilmente' (ambos com -mente é correto)."
            }
        ],
        "tabela_visual": """<strong>Avverbi — formazione e categorie</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Categoria</th><th>Esempi</th></tr>
<tr><td>Modo</td><td>bene, male, così, insieme, volentieri, lentamente, facilmente</td></tr>
<tr><td>Tempo</td><td>oggi, ieri, domani, ora, già, ancora, sempre, mai, spesso, presto, tardi</td></tr>
<tr><td>Luogo</td><td>qui, qua, lì, là, dentro, fuori, sopra, sotto, vicino, lontano, ovunque</td></tr>
<tr><td>Quantità</td><td>molto, poco, troppo, abbastanza, quasi, appena, più, meno</td></tr>
<tr><td>Affermazione</td><td>sì, certo, davvero, sicuro, anche</td></tr>
<tr><td>Negazione</td><td>no, non, mai, niente, mica, neanche, nemmeno</td></tr>
</table>
<br><strong>Formazione in -mente:</strong> aggettivo femm. + -mente<br>
lenta→lentamente | veloce→velocemente | facile→facilmente<br>
<em>Eccezioni: buono→bene | cattivo→male | molto→molto (invariabile come avv.)</em>"""
    },

    "a1-lez30": {
        "armadilhas": [
            {
                "errado": "Sono stata in Roma per una settimana fa.",
                "certo": "Sono stata a Roma una settimana fa.",
                "motivo": "Cidades usam 'a' (a Roma). 'Fa' indica tempo decorrido sem preposição: 'una settimana fa'. 'Per' indica duração: 'per una settimana'."
            },
            {
                "errado": "Se sarò ricco, comprerò una villa.",
                "certo": "Se fossi ricco, comprerei una villa. (ipotetico) / Se sarò ricco, comprerò una villa. (reale futuro)",
                "motivo": "Ambas as frases podem estar corretas dependendo do contexto. 'Se + futuro' (reale) e 'se + congiuntivo imperf.' (ipotetico). A distinção é o grau de probabilidade."
            },
            {
                "errado": "Mi piacciono la pizza e il gelato.",
                "certo": "Mi piacciono la pizza e il gelato. ✓",
                "motivo": "Correto! 'Piacere' concorda com o sujeito gramatical (la pizza e il gelato = plurale), não com 'mi'. 'Mi piace il gelato' (sing.) / 'Mi piacciono i dolci' (plur.)."
            }
        ],
        "tabela_visual": """<strong>Ripasso Generale A1 — strutture chiave</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#27AE60;color:#fff"><th>Struttura</th><th>Esempio</th></tr>
<tr><td>Articoli + genere</td><td>il libro / la penna / lo studente / l'amica</td></tr>
<tr><td>Passato prossimo</td><td>Ho mangiato / Sono andato/a</td></tr>
<tr><td>Imperfetto vs. pass. pross.</td><td>Mentre leggevo, ha squillato il telefono.</td></tr>
<tr><td>Futuro semplice</td><td>Domani andrò al mare.</td></tr>
<tr><td>Condizionale</td><td>Vorrei un caffè, per favore.</td></tr>
<tr><td>Periodo ipotetico</td><td>Se avessi tempo, viaggerei.</td></tr>
<tr><td>Pronomi combinati</td><td>Me lo dai? / Glielo mando domani.</td></tr>
<tr><td>Piacere</td><td>Mi piace / Mi piacciono</td></tr>
<tr><td>Passiva</td><td>Il libro è stato scritto da Calvino.</td></tr>
<tr><td>Congiuntivo</td><td>Penso che venga. / Speravo che venisse.</td></tr>
</table>"""
    },

    # ─── B1 — tabela_visual only ──────────────────────────────────────────────

    "b1-i": {
        "tabela_visual": """<strong>Vocabolario digitale essenziale</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Italiano</th><th>Português</th><th>Uso</th></tr>
<tr><td>il profilo</td><td>o perfil</td><td>il mio profilo Instagram</td></tr>
<tr><td>condividere</td><td>compartilhar</td><td>condividere un post</td></tr>
<tr><td>taggare</td><td>marcar (tag)</td><td>Mi ha taggato in una foto.</td></tr>
<tr><td>seguire / seguirsi</td><td>seguir</td><td>Ti seguo su Instagram.</td></tr>
<tr><td>il like / mettere like</td><td>curtir</td><td>Ha messo like alla mia foto.</td></tr>
<tr><td>commentare</td><td>comentar</td><td>Commenta il mio post!</td></tr>
<tr><td>andare viral</td><td>viralizar</td><td>Il video è andato virale.</td></tr>
<tr><td>il contenuto</td><td>o conteúdo</td><td>creare contenuti di qualità</td></tr>
<tr><td>la diretta</td><td>a live</td><td>fare una diretta su TikTok</td></tr>
<tr><td>la privacy</td><td>a privacidade</td><td>impostazioni sulla privacy</td></tr>
</table>
<br><strong>Espressioni utili:</strong><br>
<em>Sei su Instagram? — Mi segui? — Ho cambiato le impostazioni. — Il segnale è scarso. — Carica lentamente.</em>"""
    },

    "b1-ii": {
        "tabela_visual": """<strong>Linguaggio professionale — formule essenziali</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Situazione</th><th>Formula formale</th></tr>
<tr><td>Iniziare email</td><td>Gentile Sig./Sig.ra [cognome], / Egregio Dott. [cognome],</td></tr>
<tr><td>Riferirsi a email ricevuta</td><td>In riferimento alla Sua email del [data]...</td></tr>
<tr><td>Chiedere informazioni</td><td>Vorrei richiedere informazioni riguardo a...</td></tr>
<tr><td>Confermare</td><td>Con la presente confermo / Le confermo che...</td></tr>
<tr><td>Scusarsi</td><td>Mi scuso per il ritardo / l'inconveniente.</td></tr>
<tr><td>Allegare documento</td><td>In allegato troverà il documento richiesto.</td></tr>
<tr><td>Chiudere email</td><td>In attesa di una Sua risposta, porgo cordiali saluti.</td></tr>
<tr><td>Firma</td><td>[Nome] [Cognome] | [Ruolo] | [Azienda]</td></tr>
</table>
<br><strong>Vocabolario HR/ufficio:</strong> il colloquio (entrevista) | il curriculum vitae | il contratto | la retribuzione (salário) | le ferie (férias) | il permesso (folga) | la riunione (reunião) | il progetto (projeto)"""
    },

    "b1-iii": {
        "tabela_visual": """<strong>Cultura e società italiana — riferimenti chiave</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Tema</th><th>Concetto</th><th>Esempio/Nota</th></tr>
<tr><td>Famiglia</td><td>La famiglia allargata</td><td>Nonni, zii spesso coinvolti nella crescita dei figli.</td></tr>
<tr><td>Cibo</td><td>La cucina regionale</td><td>Ogni regione ha piatti tipici; il cibo è identità culturale.</td></tr>
<tr><td>Lavoro</td><td>Il posto fisso</td><td>Tradizionalmente ambito, ma la gig economy cambia tutto.</td></tr>
<tr><td>Nord/Sud</td><td>Il divario</td><td>Differenze economiche, culturali e linguistiche persistono.</td></tr>
<tr><td>Calcio</td><td>Lo sport nazionale</td><td>Le partite della Nazionale uniscono il paese.</td></tr>
<tr><td>Moda</td><td>Il Made in Italy</td><td>Armani, Gucci, Ferrari — simboli di eccellenza italiana.</td></tr>
<tr><td>Politica</td><td>I partiti</td><td>Sistema multipartitico; governi di coalizione frequenti.</td></tr>
</table>
<br><strong>Espressioni culturali:</strong><br>
<em>bella figura</em> (boa impressão) | <em>arrangiarsi</em> (se virar) | <em>dolce far niente</em> (prazer em não fazer nada) | <em>campanilismo</em> (orgulho local)"""
    },

    "b1-iv": {
        "tabela_visual": """<strong>Esprimere opinioni e argomentare</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Funzione</th><th>Espressioni</th></tr>
<tr><td>Dare opinione</td><td>Secondo me... / A mio avviso... / Dal mio punto di vista... / Penso che + congiuntivo</td></tr>
<tr><td>Essere d'accordo</td><td>Sono d'accordo. / Hai ragione. / Esatto. / Certamente. / Condivido questa opinione.</td></tr>
<tr><td>Non essere d'accordo</td><td>Non sono d'accordo. / Non mi convince. / Al contrario... / Invece, secondo me...</td></tr>
<tr><td>Aggiungere argomento</td><td>Inoltre... / Tra l'altro... / Bisogna anche considerare che... / Non solo... ma anche...</td></tr>
<tr><td>Concedere</td><td>È vero che..., però... / Capisco il tuo punto, ma... / Anche se hai ragione su X, tuttavia...</td></tr>
<tr><td>Concludere</td><td>In conclusione... / Per riassumere... / In definitiva... / Quindi...</td></tr>
</table>
<br><strong>Struttura argomentativa:</strong><br>
Tesi → Argomento 1 (+ esempio) → Argomento 2 (+ esempio) → Concessione → Conclusione"""
    },

    "b1-v": {
        "tabela_visual": """<strong>L'italiano regionale — caratteristiche principali</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Regione</th><th>Caratteristica</th><th>Esempio</th></tr>
<tr><td>Toscana</td><td>«gorgia toscana» (aspirazione delle occlusive)</td><td>«la [h]asa» per «la casa»</td></tr>
<tr><td>Roma/Lazio</td><td>Raddoppiamento, vocalismo aperto</td><td>«bbe» per «bene»; «a Roma» detto «a Rrroma»</td></tr>
<tr><td>Napoli/Sud</td><td>Vocali finali ridotte, ritmo diverso</td><td>uso del passato remoto per eventi recenti</td></tr>
<tr><td>Milano/Nord</td><td>Influenza del dialetto lombardo, ritmo più rapido</td><td>«ghe» → «c'è» nel dialetto; italiano senza cadenza meridionale</td></tr>
<tr><td>Sicilia</td><td>Consonanti intense, vocali chiuse</td><td>doppia pronuncia di consonanti intervocaliche</td></tr>
<tr><td>Veneto</td><td>Intonazione cantata, influenza veneta</td><td>«el» per «il» nel dialetto locale</td></tr>
</table>
<br><strong>Dialetti vs. italiano regionale:</strong> I dialetti sono lingue distinte (veneziano, napoletano, siciliano). L'italiano regionale è l'italiano standard con accento e alcune forme locali."""
    },

    "b1-vi": {
        "tabela_visual": """<strong>Congiuntivo Presente — coniugazione e usi</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Persona</th><th>parlare</th><th>leggere</th><th>finire</th><th>essere</th><th>avere</th></tr>
<tr><td>io/tu/lui/lei</td><td>parli</td><td>legga</td><td>finisca</td><td>sia</td><td>abbia</td></tr>
<tr><td>noi</td><td>parliamo</td><td>leggiamo</td><td>finiamo</td><td>siamo</td><td>abbiamo</td></tr>
<tr><td>voi</td><td>parliate</td><td>leggiate</td><td>finiate</td><td>siate</td><td>abbiate</td></tr>
<tr><td>loro</td><td>parlino</td><td>leggano</td><td>finiscano</td><td>siano</td><td>abbiano</td></tr>
</table>
<br><strong>Quando usare il congiuntivo:</strong><br>
Penso/Credo/Spero <strong>che</strong> + cong. | Benché/Sebbene/Nonostante + cong. | Affinché/Prima che + cong. | Bisogna che + cong.<br><br>
<strong>Nota:</strong> Le prime tre persone singolari sono identiche → il contesto chiarisce il soggetto."""
    },

    "b1-vii": {
        "tabela_visual": """<strong>Condizionale Presente — coniugazione e usi</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Persona</th><th>parlare</th><th>avere</th><th>essere</th><th>andare</th></tr>
<tr><td>io</td><td>parlerei</td><td>avrei</td><td>sarei</td><td>andrei</td></tr>
<tr><td>tu</td><td>parleresti</td><td>avresti</td><td>saresti</td><td>andresti</td></tr>
<tr><td>lui/lei</td><td>parlerebbe</td><td>avrebbe</td><td>sarebbe</td><td>andrebbe</td></tr>
<tr><td>noi</td><td>parleremmo</td><td>avremmo</td><td>saremmo</td><td>andremmo</td></tr>
<tr><td>voi</td><td>parlereste</td><td>avreste</td><td>sareste</td><td>andreste</td></tr>
<tr><td>loro</td><td>parlerebbero</td><td>avrebbero</td><td>sarebbero</td><td>andrebbero</td></tr>
</table>
<br><strong>Usi del condizionale presente:</strong><br>
• Pedido educado: <em>Vorrei un'informazione.</em><br>
• Ipotesi: <em>Al posto tuo, studierei di più.</em><br>
• Notizia non confermata: <em>Il presidente sarebbe dimissionario.</em><br>
• Desiderio: <em>Mi piacerebbe vivere in Italia.</em>"""
    },

    "b1-viii": {
        "tabela_visual": """<strong>Pronomi Relativi — uso completo</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Pronome</th><th>Funzione</th><th>Esempio</th></tr>
<tr><td><strong>che</strong></td><td>sogg. / ogg. diretto</td><td>Il libro che leggo è interessante.</td></tr>
<tr><td><strong>cui</strong></td><td>con preposizione</td><td>La città in cui vivo è bella. / L'amico con cui parlo.</td></tr>
<tr><td><strong>il quale / la quale</strong></td><td>alternativa formale a che/cui</td><td>Il professore il quale insegna qui.</td></tr>
<tr><td><strong>il cui / la cui</strong></td><td>posse (cujo/cuja)</td><td>Lo studente il cui padre è famoso.</td></tr>
<tr><td><strong>quello che / ciò che</strong></td><td>o que (senza antecedente)</td><td>Quello che dici è vero.</td></tr>
<tr><td><strong>chi</strong></td><td>colui che / quem (senza antec.)</td><td>Chi studia, impara. / Ho trovato chi cercavo.</td></tr>
<tr><td><strong>quanto</strong></td><td>tutto ciò che</td><td>Quanto ha detto è importante.</td></tr>
</table>
<br><strong>Atenção:</strong> 'che' não pode ser precedido de preposição. Use 'cui': <em>il motivo per cui</em> (não: *il motivo per che)."""
    },

    "b1-ix": {
        "tabela_visual": """<strong>Forma Passiva — tutti i tempi principali</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Tempo</th><th>Struttura</th><th>Esempio</th></tr>
<tr><td>Presente</td><td>essere (pres.) + p.p.</td><td>La lettera è scritta.</td></tr>
<tr><td>Imperfetto</td><td>essere (imp.) + p.p.</td><td>La lettera era scritta.</td></tr>
<tr><td>Passato prossimo</td><td>essere stato + p.p.</td><td>La lettera è stata scritta.</td></tr>
<tr><td>Trapassato</td><td>essere stato (imp.) + p.p.</td><td>La lettera era stata scritta.</td></tr>
<tr><td>Futuro</td><td>essere (fut.) + p.p.</td><td>La lettera sarà scritta.</td></tr>
<tr><td>Condizionale</td><td>essere (cond.) + p.p.</td><td>La lettera sarebbe scritta.</td></tr>
<tr><td>Congiuntivo pres.</td><td>sia + p.p.</td><td>Penso che sia già scritta.</td></tr>
</table>
<br><strong>Alternative alla passiva:</strong><br>
• <strong>venire</strong> + p.p. (tempi semplici, azione dinamica): <em>Il pacco viene consegnato.</em><br>
• <strong>si passivante</strong>: <em>Si parla italiano. / Si vendono case.</em><br>
• <strong>andare</strong> + p.p. (obbligo): <em>Va fatto subito.</em>"""
    },

    "b1-x": {
        "tabela_visual": """<strong>Il Gerundio — formazione e usi</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Tipo</th><th>Formazione</th><th>Esempio</th></tr>
<tr><td>Gerundio presente</td><td>-are → -ando<br>-ere/-ire → -endo</td><td>parlando | leggendo | finendo</td></tr>
<tr><td>Gerundio passato</td><td>avendo/essendo + p.p.</td><td>avendo mangiato | essendo arrivato</td></tr>
</table>
<br><strong>Usi del gerundio:</strong><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Funzione</th><th>Esempio</th></tr>
<tr><td>Modo (come?)</td><td>Ha risposto sorridendo. (sorriu ao responder)</td></tr>
<tr><td>Causa</td><td>Essendo stanco, è andato a letto presto.</td></tr>
<tr><td>Tempo (mentre)</td><td>Studiando, ascolto musica.</td></tr>
<tr><td>Concessione</td><td>Pur sapendo la verità, non ha parlato.</td></tr>
<tr><td>Stare + gerundio</td><td>Sto mangiando. / Stava leggendo.</td></tr>
</table>
<br><strong>Atenção:</strong> O sujeito do gerúndio deve ser o mesmo da oração principal."""
    },

    "b1-xi": {
        "tabela_visual": """<strong>Congiuntivo Imperfetto — coniugazione</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Persona</th><th>parlare</th><th>leggere</th><th>finire</th><th>essere</th><th>avere</th></tr>
<tr><td>io</td><td>parlassi</td><td>leggessi</td><td>finissi</td><td>fossi</td><td>avessi</td></tr>
<tr><td>tu</td><td>parlassi</td><td>leggessi</td><td>finissi</td><td>fossi</td><td>avessi</td></tr>
<tr><td>lui/lei</td><td>parlasse</td><td>leggesse</td><td>finisse</td><td>fosse</td><td>avesse</td></tr>
<tr><td>noi</td><td>parlassimo</td><td>leggessimo</td><td>finissimo</td><td>fossimo</td><td>avessimo</td></tr>
<tr><td>voi</td><td>parlaste</td><td>leggeste</td><td>finiste</td><td>foste</td><td>aveste</td></tr>
<tr><td>loro</td><td>parlassero</td><td>leggessero</td><td>finissero</td><td>fossero</td><td>avessero</td></tr>
</table>
<br><strong>Quando usare il congiuntivo imperfetto:</strong><br>
• Verbo principale al passato: <em>Pensavo che venisse.</em><br>
• Periodo ipotetico irreal: <em>Se fossi ricco, viaggerei.</em><br>
• Desiderio irreale: <em>Magari avessi più tempo!</em><br>
• Come se: <em>Parla come se sapesse tutto.</em>"""
    },

    "b1-xii": {
        "tabela_visual": """<strong>Modali al Passato — dovere, potere, volere</strong><br><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Modale</th><th>Con AVERE</th><th>Con ESSERE</th><th>Significado</th></tr>
<tr><td>dovere</td><td>ho dovuto lavorare</td><td>sono dovuto/a andare</td><td>tive que (e fui)</td></tr>
<tr><td>potere</td><td>ho potuto parlare</td><td>sono potuto/a uscire</td><td>pude (e o fiz)</td></tr>
<tr><td>volere</td><td>ho voluto restare</td><td>sono voluto/a venire</td><td>quis (e o fiz)</td></tr>
</table>
<br><strong>Condizionale composto dei modali:</strong><br>
<table border="1" cellpadding="6" style="border-collapse:collapse;width:100%;font-size:0.93em">
<tr style="background:#2980B9;color:#fff"><th>Forma</th><th>Significado</th><th>Esempio</th></tr>
<tr><td>avrei dovuto</td><td>deveria ter</td><td>Avrei dovuto studiare di più.</td></tr>
<tr><td>avrei potuto</td><td>poderia ter</td><td>Avresti potuto avvisarmi!</td></tr>
<tr><td>avrei voluto</td><td>teria querido</td><td>Avrei voluto venire, ma non potevo.</td></tr>
</table>
<br><strong>Regra do auxiliare:</strong> O auxiliar (avere/essere) é determinado pelo verbo no infinito. Se o infinito usa essere (andare, venire...), o modal usa essere. Ambas as formas são aceitas na língua moderna."""
    },
}


def is_placeholder_armadilhas(arr):
    if not arr:
        return False
    for item in arr:
        errado = item.get("errado", "")
        if "Erro comum" in errado or "Forma errada" in errado or errado.startswith("Frase errada"):
            return True
    return False


def is_placeholder_tabela(html):
    if not html:
        return False
    return "Regra 1" in html or "Tabela de consulta rapida" in html or "Regra 2" in html


def main():
    with open(PATH, encoding="utf-8") as f:
        data = json.load(f)

    arm_updated = 0
    tab_updated = 0

    for modulo in data["moduli"]:
        for lez in modulo["lezioni"]:
            lid = lez.get("id", "")
            if lid not in CONTENT:
                continue
            patch = CONTENT[lid]

            # Update armadilhas if placeholder and patch has it
            if "armadilhas" in patch and is_placeholder_armadilhas(lez.get("armadilhas", [])):
                lez["armadilhas"] = patch["armadilhas"]
                arm_updated += 1
                print(f"  [armadilhas] updated: {lid}")

            # Update tabela_visual if placeholder
            if "tabela_visual" in patch and is_placeholder_tabela(lez.get("tabela_visual", "")):
                lez["tabela_visual"] = patch["tabela_visual"]
                tab_updated += 1
                print(f"  [tabela_visual] updated: {lid}")

    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nDone! armadilhas updated: {arm_updated} | tabela_visual updated: {tab_updated}")
    print(f"Total fields updated: {arm_updated + tab_updated}")


if __name__ == "__main__":
    main()
