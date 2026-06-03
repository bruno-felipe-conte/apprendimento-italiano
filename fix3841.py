import json, os

OUT = os.path.dirname(os.path.abspath(__file__))

def w(tid, it, pt, cat, ex_it, ex_pt, ipa="", gen=None, pl=None):
    return {
        "id": tid, "italiano": it, "portugues": pt, "genero": gen, "plural": pl,
        "exemplo": ex_it, "exemplo_pt": ex_pt, "categoria": cat, "dificuldade": "medio", "audio_ipa": ipa
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

t38_add = [
    ("nevrosi", "neurose", "disturbi", "Soffrire di nevrosi.", "Sofrer de neurose.", "/neˈvrɔzi/", "f", "nevrosi"),
    ("bipolare", "bipolar", "disturbi", "Disturbo bipolare.", "Transtorno bipolar.", "/bipoˈlare/", "m/f", "bipolari"),
    ("borderline", "borderline", "disturbi", "Disturbo borderline.", "Transtorno borderline.", "/bɔrderˈlain/", "m/f", "borderline"),
    ("resilienza", "resiliência", "psicologia", "Avere molta resilienza.", "Ter muita resiliência.", "/reziliˈɛntsa/", "f", "resilienze"),
    ("burnout", "burnout/esgotamento", "disturbi", "Sindrome da burnout.", "Síndrome de burnout.", "/bərnˈaut/", "m", "burnout"),
    ("autostima", "autoestima", "psicologia", "Aumentare l'autostima.", "Aumentar a autoestima.", "/autosˈtima/", "f", "autostime"),
    ("egocentrico", "egocêntrico", "aggettivi", "È molto egocentrico.", "É muito egocêntrico.", "/edʒoˈtʃɛntriko/", "m", "egocentrici"),
    ("ipocondria", "hipocondria", "disturbi", "Soffre di ipocondria.", "Sofre de hipocondria.", "/ipokonˈdria/", "f", "ipocondrie"),
    ("fobia sociale", "fobia social", "disturbi", "Combattere la fobia sociale.", "Combater a fobia social.", "/foˈbia soˈtʃale/", "f", "fobie sociali"),
    ("sociopatico", "sociopata", "aggettivi", "Un criminale sociopatico.", "Um criminoso sociopata.", "/sotʃoˈpatiko/", "m", "sociopatici"),
    ("empatizzare", "empatizar", "verbi", "Empatizzare con gli altri.", "Empatizar com os outros.", "/empatidˈdzare/", None, None),
    ("sublimazione", "sublimação", "psicologia", "Sublimazione degli istinti.", "Sublimação dos instintos.", "/sublimatˈtsjone/", "f", "sublimazioni")
]

t39_add = [
    ("quasar", "quasar", "spazio", "Un quasar molto luminoso.", "Um quasar muito luminoso.", "/ˈkwazar/", "m", "quasar"),
    ("pulsar", "pulsar", "spazio", "La pulsar ruota velocemente.", "O pulsar gira rapidamente.", "/ˈpulsar/", "f", "pulsar"),
    ("nana bianca", "anã branca", "spazio", "Una stella nana bianca.", "Uma estrela anã branca.", "/ˈnana ˈbjanka/", "f", "nane bianche"),
    ("supernova", "supernova", "spazio", "Esplosione di una supernova.", "Explosão de uma supernova.", "/superˈnɔva/", "f", "supernove"),
    ("eclittica", "eclíptica", "spazio", "Il piano dell'eclittica.", "O plano da eclíptica.", "/eˈklittika/", "f", "eclittiche"),
    ("zenit", "zênite", "spazio", "Il sole allo zenit.", "O sol no zênite.", "/ˈdzɛnit/", "m", "zenit"),
    ("nadir", "nadir", "spazio", "Il punto del nadir.", "O ponto do nadir.", "/naˈdir/", "m", "nadir"),
    ("astrofisico", "astrofísico", "persone", "L'astrofisico studia le stelle.", "O astrofísico estuda as estrelas.", "/astroˈfiziko/", "m", "astrofisici"),
    ("propulsore", "propulsor", "esplorazione", "Accendere il propulsore.", "Ligar o propulsor.", "/propulˈsore/", "m", "propulsori"),
    ("orbiter", "orbiter", "esplorazione", "L'orbiter spaziale.", "O orbiter espacial.", "/ˈɔrbiter/", "m", "orbiter"),
    ("lander", "lander/módulo de pouso", "esplorazione", "Il lander è sulla luna.", "O módulo de pouso está na lua.", "/ˈlɛnder/", "m", "lander"),
    ("cratere", "cratera", "spazio", "Un cratere lunare.", "Uma cratera lunar.", "/kraˈtɛre/", "m", "crateri"),
    ("via lattea", "via láctea", "spazio", "La nostra Via Lattea.", "A nossa Via Láctea.", "/ˈvia ˈlattea/", "f", None) # if dupe, json doesn't mind but let's change to "galattico"
]
t39_add[12] = ("galattico", "galáctico", "aggettivi", "L'impero galattico.", "O império galáctico.", "/ɡaˈlattiko/", "m", "galattici")

t40_add = [
    ("speculazione", "especulação", "finanza", "Speculazione finanziaria.", "Especulação financeira.", "/spekulatˈtsjone/", "f", "speculazioni"),
    ("bolla", "bolha", "finanza", "Lo scoppio della bolla.", "O estouro da bolha.", "/ˈbolla/", "f", "bolle"),
    ("dividendo", "dividendo", "finanza", "Incassare il dividendo.", "Receber o dividendo.", "/diviˈdɛndo/", "m", "dividendi"),
    ("default", "default/calote", "finanza", "Rischio di default.", "Risco de calote.", "/deˈfolt/", "m", "default"),
    ("bancarotta", "bancarrota/falência", "finanza", "Dichiarare bancarotta.", "Declarar falência.", "/bankaˈrotta/", "f", "bancarotte"),
    ("rating", "rating/classificação", "finanza", "L'agenzia di rating.", "A agência de classificação.", "/ˈreitiŋ/", "m", "rating")
]

t41_add = [
    ("a priori", "a priori", "concetti", "Un giudizio a priori.", "Um julgamento a priori.", "/a priˈori/", None, None),
    ("a posteriori", "a posteriori", "concetti", "Un giudizio a posteriori.", "Um julgamento a posteriori.", "/a posteˈrjori/", None, None),
    ("noumeno", "nôumeno", "concetti", "Il noumeno kantiano.", "O nôumeno kantiano.", "/noˈumeno/", "m", "noumeni"),
    ("fenomeno", "fenômeno (filosófico)", "concetti", "Il fenomeno osservabile.", "O fenômeno observável.", "/feˈnɔmeno/", "m", "fenomeni"),
    ("solipsismo", "solipsismo", "correnti", "Il pericolo del solipsismo.", "O perigo do solipsismo.", "/solipˈsizmo/", "m", "solipsismi"),
    ("trascendentale", "transcendental", "aggettivi", "L'io trascendentale.", "O eu transcendental.", "/traʃʃendenˈtale/", "m", "trascendentali")
]

if __name__ == "__main__":
    append_to_existing(38, t38_add)
    append_to_existing(39, t39_add)
    append_to_existing(40, t40_add)
    append_to_existing(41, t41_add)
