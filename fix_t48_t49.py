import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "difficile", "audio_ipa": ipa
    }

def append_to_existing(templo_num, new_words_data):
    path = os.path.join(OUT, "data", f"templo-{templo_num}.json")
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    
    current_count = len(obj["palavras"])
    for i, (it, pt, cat, ex_it, ex_pt, ipa, gen, pl) in enumerate(new_words_data, current_count + 1):
        tid = f"t{templo_num}_{i:03d}"
        obj["palavras"].append(w(tid, it, pt, cat, ex_it, ex_pt, ipa, gen, pl))
        
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"APPENDED templo-{templo_num}.json -- now has {len(obj['palavras'])} parole")

t48_add = [
    ("incalzare", "pressionar (com argumentos)", "verbi", "Incalzare l'avversario.", "Pressionar o adversário.", "/inkalˈtsare/", None, None),
    ("divagare", "divagar", "verbi", "Non divagare troppo.", "Não divague muito.", "/divaˈɡare/", None, None),
    ("sintetizzare", "sintetizar", "verbi", "Sintetizzare il discorso.", "Sintetizar o discurso.", "/sintetidˈdzare/", None, None),
    ("chiarire", "esclarecer", "verbi", "Chiarire un punto oscuro.", "Esclarecer um ponto obscuro.", "/kjaˈrire/", None, None),
    ("elencare", "listar", "verbi", "Elencare i motivi.", "Listar os motivos.", "/elenˈkare/", None, None),
    ("ribattere", "rebater", "verbi", "Ribattere a un'accusa.", "Rebater uma acusação.", "/riˈbattere/", None, None),
    ("esordire", "começar (discurso)", "verbi", "Esordire con una battuta.", "Começar com uma piada.", "/ezorˈdire/", None, None),
    ("ringraziare", "agradecer", "verbi", "Ringraziare il pubblico.", "Agradecer ao público.", "/rinɡratˈtsjare/", None, None),
    ("elogiare", "elogiar", "verbi", "Elogiare l'ospite.", "Elogiar o convidado.", "/eloˈdʒare/", None, None),
    ("denigrare", "denegrir", "verbi", "Denigrare l'avversario.", "Denegrir o adversário.", "/deniˈɡrare/", None, None),
    ("lusingare", "lisonjear", "verbi", "Lusingare la folla.", "Lisonjear a multidão.", "/luzinˈɡare/", None, None),
    ("adulare", "adular", "verbi", "Adulare il capo.", "Adular o chefe.", "/aduˈlare/", None, None),
    ("infiammare", "inflamar", "verbi", "Infiammare gli animi.", "Inflamar os ânimos.", "/infjamˈmare/", None, None),
    ("rassicurare", "tranquilizar", "verbi", "Rassicurare i cittadini.", "Tranquilizar os cidadãos.", "/rassikuˈrare/", None, None),
    ("interrompere", "interromper", "verbi", "Interrompere l'oratore.", "Interromper o orador.", "/interˈrompere/", None, None),
    ("gesticolare", "gesticular", "verbi", "Gesticolare mentre si parla.", "Gesticular enquanto se fala.", "/dʒestikoˈlare/", None, None),
    ("inveire", "esbravejar", "verbi", "Inveire contro qualcuno.", "Esbravejar contra alguém.", "/inveˈire/", None, None),
    ("smentire", "desmentir", "verbi", "Smentire una voce.", "Desmentir um boato.", "/zmenˈtire/", None, None),
    ("concludere", "concluir", "verbi", "Concludere in bellezza.", "Concluir com chave de ouro.", "/konˈkludere/", None, None)
]

t49_add = [
    ("aum", "om (sílaba)", "spiritualità", "Il suono dell'Aum.", "O som do Om.", "/aum/", "m", "aum"),
    ("sutra", "sutra", "spiritualità", "Il sutra del loto.", "O sutra de lótus.", "/ˈsutra/", "m", "sutra"),
    ("mudra", "mudra (gesto)", "spiritualità", "Fare un mudra.", "Fazer um mudra.", "/ˈmudra/", "m", "mudra"),
    ("pranayama", "pranayama (respiração)", "spiritualità", "Praticare pranayama.", "Praticar pranayama.", "/pranaˈjama/", "m", "pranayama"),
    ("kundalini", "kundalini", "spiritualità", "Risvegliare la kundalini.", "Despertar a kundalini.", "/kundaˈlini/", "f", "kundalini"),
    ("shakra", "shakra (ruota)", "spiritualità", "Il primo chakra.", "O primeiro chakra.", "/ˈtʃakra/", "m", "shakra"),
    ("bodhisattva", "bodhisattva", "spiritualità", "Un compassionevole bodhisattva.", "Um bodhisattva compassivo.", "/bodhiˈsattva/", "m", "bodhisattva"),
    ("samsara", "samsara", "spiritualità", "Il ciclo del samsara.", "O ciclo do samsara.", "/samˈsara/", "m", "samsara"),
    ("chi", "chi (energia)", "spiritualità", "Il flusso del chi.", "O fluxo do chi.", "/tʃi/", "m", "chi"),
    ("prana", "prana (energia vitale)", "spiritualità", "Respirare prana.", "Respirar prana.", "/ˈprana/", "m", "prana"),
    ("satori", "satori", "spiritualità", "Un'esperienza di satori.", "Uma experiência de satori.", "/saˈtɔri/", "m", "satori"),
    ("tantra", "tantra", "spiritualità", "Lo yoga del tantra.", "O yoga do tantra.", "/ˈtantra/", "m", "tantra"),
    ("shanti", "shanti (paz)", "spiritualità", "Om shanti shanti.", "Om shanti shanti.", "/ˈʃanti/", "f", "shanti"),
    ("lama", "lama (monge)", "persone", "Il Dalai Lama.", "O Dalai Lama.", "/ˈlama/", "m", "lama"),
    ("yogi", "yogi/iogue", "persone", "Un grande yogi.", "Um grande iogue.", "/ˈjɔdʒi/", "m", "yogi"),
    ("samadhi", "samadhi", "spiritualità", "Raggiungere il samadhi.", "Alcançar o samadhi.", "/saˈmadi/", "m", "samadhi"),
    ("kirtan", "kirtan (canto)", "spiritualità", "Cantare nel kirtan.", "Cantar no kirtan.", "/ˈkirtan/", "m", "kirtan"),
    ("bija", "bija (semente)", "spiritualità", "Un mantra bija.", "Um mantra semente.", "/ˈbidʒa/", "m", "bija"),
    ("ayurveda", "ayurveda", "disciplina", "Medicina ayurveda.", "Medicina ayurvédica.", "/ajurˈvɛda/", "f", "ayurveda"),
    ("koan", "koan", "spiritualità", "Risolvere un koan.", "Resolver um koan.", "/ˈkoan/", "m", "koan")
]

if __name__ == "__main__":
    append_to_existing(48, t48_add)
    append_to_existing(49, t49_add)
