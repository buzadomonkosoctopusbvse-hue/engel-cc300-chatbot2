import streamlit as st

st.set_page_config(page_title="ENGEL CC300 Szervizes Chatbot", page_icon="🛠")

st.title("🛠 ENGEL CC300 Szervizes Chatbot – Demó")
st.write(
    """
Ez egy **demó célú prototípus**, amely néhány ENGEL CC300 jellegű hibakód alapján
mutatja be, hogyan működhet egy szervizes chatbot. 
Írj be egy hibakódot (pl. `E221`, `E111`) vagy egy jelenséget (pl. `olaj hőmérséklet`, `safety gate`),
és a rendszer megpróbál releváns javítási lépéseket javasolni.
"""
)

KB = [
    {
        "code": "E221",
        "title": "Oil temperature too high",
        "keywords": ["oil", "temperature", "olaj", "hőmérséklet", "overheat", "túlmelegedés"],
        "checks": [
            "Ellenőrizd az olajhűtő átfolyását.",
            "Nézd meg, működik-e a ventilátor.",
            "CC300: Hydraulics → Pump menüben ellenőrizd a pumpaáramot.",
        ],
        "remedy": [
            "Tisztítsd meg az olajhűtőt és a hűtőkört.",
            "Ha a pumpaáram túl magas, csökkentsd a technológiai nyomást.",
        ],
    },
    {
        "code": "E111",
        "title": "Safety gate not closed",
        "keywords": ["safety", "gate", "ajtó", "biztonsági", "retesz", "door"],
        "checks": [
            "Vizsgáld meg a safety gate érzékelőt.",
            "Ellenőrizd a mágnesretesz mechanikus állapotát.",
            "CC300: Diagnostics → Safety → Inputs menüben nézd meg, érkezik-e jel az ajtóérzékelőtől.",
        ],
        "remedy": [
            "Ha nincs jel, állítsd be a helyes kapcsolópozíciót.",
            "Hibás érzékelő esetén cseréld ki az alkatrészt.",
        ],
    },
    {
        "code": "E305",
        "title": "Hydraulic pressure too low",
        "keywords": ["pressure", "nyomás", "hydraulic", "hidraulika", "low", "alacsony"],
        "checks": [
            "Ellenőrizd az aktuális hidraulikus nyomást a CC300 Hydraulics menüjében.",
            "Nézd meg, indul-e megfelelően a szivattyú.",
            "Ellenőrizd, nincs-e szivárgás a fő körben.",
        ],
        "remedy": [
            "Ha a nyomás nem épül fel, ellenőrizd a szivattyú vezérlését.",
            "Szükség esetén légtelenítsd a rendszert.",
        ],
    },
]

def match_entry(user_input: str):
    text = user_input.lower()

    # Exact code match
    for entry in KB:
        if entry["code"].lower() in text:
            return entry

    # Keyword scoring
    best_score = 0
    best_entry = None
    for entry in KB:
        score = sum(1 for kw in entry["keywords"] if kw in text)
        if score > best_score:
            best_score = score
            best_entry = entry

    return best_entry

user_query = st.text_input("Írd be a hibakódot vagy jelenséget:")

if st.button("Diagnosztika") or user_query.strip():
    if not user_query.strip():
        st.warning("Adj meg hibakódot vagy jelenséget.")
    else:
        entry = match_entry(user_query)
        if entry is None:
            st.info(
                "Ehhez a hibához/jelenséghez a demó tudásbázisban nincs még bejegyzés. "
                "Próbáld ki például: `E221`, `E111`, `E305`, `olaj hőmérséklet`, `safety gate`, `hidraulikus nyomás`."
            )
        else:
            st.subheader(f"Talált hiba: {entry['code']} – {entry['title']}")
            st.markdown("### Ellenőrzési lépések")
            for step in entry["checks"]:
                st.markdown(f"- {step}")
            st.markdown("### Javítási javaslatok")
            for step in entry["remedy"]:
                st.markdown(f"- {step}")

st.markdown("---")
st.caption(
    "Ez a prototípus csak szemléltetésre szolgál. "
    "Valós szervizelésnél mindig kövesd a hivatalos ENGEL dokumentációt, "
    "és csak emberi szakember hozzon döntést."
)
