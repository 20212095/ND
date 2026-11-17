# Python kodo peržiūros asistentas

Martynas Zakrys · 2026 m. lapkričio 17 d.

Darbo tikslas – sukurti vieną AI agentą, kuris gauna Python kodo fragmentą ir jo elgesio sutartį, nustato galimą problemą ir grąžina struktūrizuotą paaiškinimą bei siūlomą pataisą. Generavimui naudojamas Gemini, o 1.6 dalyje užklausa papildoma iš ChromaDB atrinktais pavyzdžiais.

Pateiktas projektas apima duomenis, užklausas, agento kodą, UML šaltinius ir dvi vykdomas Colab užrašines. API demonstravimas, matavimai ir asmeninių nuorodų įrašymas atliekami paleidus užrašines savo paskyroje.

| Dalis | Parengta | Dar atlikti |
| --- | --- | --- |
| 1.1 | NotebookLM pradžia matoma pateiktoje nuotraukoje | Patikrinti produktus ir įrašyti nuorodas |
| 1.2 | X ir y, proceso aprašas, duomenų failai | Rankinis brėžinys ir dviejų originalių Colab analizė |
| 1.3 | Ericsson pagrindimas ir trys UML šaltiniai | Atvaizduoti PlantUML diagramas |
| 1.4 | Zero-shot ir few-shot užklausos | Įkelti į GitHub /prompts/ |
| 1.5 | Agentas ir Gemini Colab užrašinė | Paleisti ir papildyti refleksiją |
| 1.6 | 1200 porų, sukurta ChromaDB ir RAG užrašinė | Colab atkurti DB, paleisti Gemini ir įvertinti rezultatus |

### Nuo ko pradėti

Pirmiausia įkelkite Lab_1_5_Gemini.ipynb į Google Colab, sukurkite GEMINI_KEY paslaptį ir paleiskite langelius iš eilės. Išsaugokite gautus rezultatus. Tuomet paleiskite Lab_1_6_RAG_ChromaDB.ipynb ir išmatuokite, ar papildomas kontekstas padėjo.

## 1 1 NotebookLM šaltinių analizė

Pateiktoje ekrano nuotraukoje matomi keturi šaltiniai: BD3.docx ir trys su automatizuota kodo peržiūra susiję straipsniai. Studio srityje taip pat matomi vaizdo apžvalgos, garso apžvalgos ir minčių žemėlapio įrašai. Tai atitinka pagrindinę 1.1 užduoties struktūrą.

### Pasirinktų straipsnių paskirtis

Automated Code Review Using Large Language Models at Ericsson aprašo lengvą kodo peržiūros įrankį, kuriame LLM derinamas su statine programų analize. Straipsnis pagrindžia praktinį darbo pritaikymą programinės įrangos kūrimo įmonėje [1].

BitsAI-CR nagrinėja dviejų etapų peržiūrą: pradinis taisyklių tikrinimas papildomas komentarų filtravimu. Šiam darbui svarbi mintis – vien sugeneruoti pastabą neužtenka; reikia mažinti netikslias pastabas ir vertinti jų kokybę [2].

Towards Automating Code Review Activities tiria giliojo mokymosi pritaikymą kodo pakeitimams, kylantiems per peržiūrą, generuoti. Tai padeda atskirti problemos paaiškinimą ir konkrečios pataisos generavimą [3].

### Tekstas pristatymo pradžiai

Mano darbo tema yra giliuoju mokymusi pagrįstas Python kodo peržiūros asistentas. Į NotebookLM įkėliau savo darbą ir tris susijusius mokslinius straipsnius. Jie nagrinėja automatizuotos kodo peržiūros taikymą ir galimus jos ribotumus. Pagal šaltinius sugeneravau vaizdo bei garso apžvalgas ir minčių žemėlapį. Šias priemones naudoju darbo problemai, siūlomam sprendimui ir vertinimo būdams pristatyti. Mano projekte AI gauna kodą, pateikia galimą problemą ir pasiūlo pataisą. Pataisą turi įvertinti programuotojas, nes sugeneruotas atsakymas gali būti netikslus.

### Ką pridėti po peržiūros

- NotebookLM užrašinės nuorodą ir prieigos nustatymą dėstytojui.

- Vaizdo, garso apžvalgos ir minčių žemėlapio nuorodas arba jų eksporto failus.

- Po vieną konkretų pastebėjimą iš kiekvieno produkto ir bent vieną patikrintą netikslumą, jeigu toks rastas.

Konkrečias sugeneruotų produktų išvadas reikia įrašyti juos peržiūrėjus. Ekrano nuotrauka parodo produktų buvimą, bet ne visą jų turinį.

## 1 2 Sistema nuo įvesties iki rezultato

Sistema skirta programuotojui, kuris nori pirminės savo Python fragmento peržiūros. Įvestis X apima kodą ir tikėtiną jo elgesį. Išvestis y aprašo vieną pagrindinę problemą arba nurodo, kad pagal sutartį jos nerasta. Visą grandinę valdo vienas agentas.

| Elementas | Reikšmė šiame projekte |
| --- | --- |
| X | language, code ir contract laukai |
| y | has_issue, issue_type, severity, line, problematic_code, explanation, recommendation, suggested_code, confidence |
| Modelis | Gemini: kodo analizė ir struktūrizuoto atsakymo generavimas |
| Kontekstas | Be pavyzdžių, trys pastovūs pavyzdžiai arba trys RAG rezultatai |

### Vienos poros paaiškinimas

Sutartis: kiekvienas kvietimas be bucket argumento turi gauti naują sąrašą. X pavyzdys iš data katalogo:

```
def review_mutable_default_0(value_0, bucket=[]):
    bucket.append(value_0)
    return bucket
```

Tikėtinas y nurodo correctness problemą pirmoje eilutėje ir medium svarbą. Numatytasis sąrašas sukuriamas apibrėžiant funkciją, todėl tas pats objektas naudojamas per kelis kvietimus. Pataisa:

```
def review_mutable_default_0(value_0, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(value_0)
    return bucket
```

### Duomenys GitHub kataloge

data/examples_small.json pateikia tris pilnas poras su visais y laukais. data/examples.jsonl pateikia 1200 porų RAG korpusą. data/README.md paaiškina jų struktūrą, kilmę ir ribotumus. Tai parengti etaloniniai atsakymai, o ne Gemini bandymo rezultatai.

## 1 2 Proceso brėžinys ir Colab analizė

### Ranka braižoma preliminari schema

Nubraižykite pradžią, X pateikimą ir įvesties patikrą. Toliau pridėkite pasirinkimą, ar naudojamas RAG. RAG šakoje apskaičiuojamas semantinis vektorius ir iš ChromaDB paimami trys pavyzdžiai. Kitoje šakoje naudojama užklausa be pavyzdžių arba su pastoviais few-shot pavyzdžiais. Šakos susijungia prieš siunčiant užklausą Gemini. Po generavimo tikrinamas JSON ir grąžinamas y arba parodoma klaida. AI naudojimą pažymėkite ties modelio inferencija.

Tikslus veiklos diagramos šaltinis pateiktas diagrams/process.puml. Dėstytojo reikalaujamą rankinį brėžinį nuskenuokite arba nufotografuokite ir pridėkite prie projekto.

### Dviejų originalių Colab užrašinių nagrinėjimas

Užduotyje pateiktų dviejų užrašinių turinio nepavyko nuskaityti, todėl jų veikimo analizė dar turi būti atlikta pagal originalius .ipynb failus. Nuorodų ir analizės klausimų failas yra docs/Destytojo_Colab_analize.md.

| Tikrinama dalis | Ką paaiškinti pristatant |
| --- | --- |
| Tikslas ir duomenys | Kokį uždavinį sprendžia užrašinė ir kokie yra X bei y |
| Paruošimas | Kokios bibliotekos diegiamos ir kaip paruošiami duomenys |
| Modelio naudojimas | Ar modelis mokomas, ar vykdoma inferencija; kokie parametrai |
| Rezultatas | Kokia faktinė išvestis arba metrika gaunama |
| Pritaikymas | Kurį principą galima panaudoti Python kodo peržiūrai |

Atverkite kiekvieną originalią užrašinę ir pasirinkite File → Download → Download .ipynb. Analizuojant užrašinę būtina perskaityti jos langelius ir rezultatus, o ne spręsti apie veikimą vien iš užduoties temos.

## 1 3 Įmonė ir UML integracija

Tinkama pasirinkta įmonė yra Ericsson. Jų patirties ataskaitoje nagrinėjamas LLM ir statinės analizės naudojimas kodo peržiūrai, todėl siūlomo asistento paskirtis tiesiogiai atitinka aprašytą poreikį [1]. Šiame darbe Ericsson naudojama kaip pagrįstas taikymo scenarijus; integracija į tikrą įmonės infrastruktūrą neatliekama.

| Diagrama | Ką parodo | PlantUML failas |
| --- | --- | --- |
| Panaudos atvejų | Programuotojo veiksmus ir išorinį Gemini | use_case.puml |
| Komponentų | Colab, agentą, ChromaDB, MiniLM ir Gemini | components.puml |
| Sekų | Įvesties, konteksto, užklausos ir rezultato perdavimo tvarką | sequence.puml |

Generatyvinis AI integruotas Gemini komponente. ChromaDB atlieka paiešką, MiniLM sudaro vektorius, o agentas tvarko procesą ir tikrina rezultatą. Agentas yra vienas, nors jis naudoja kelis techninius komponentus.

Aiškinamoji komponentų ryšių schema. UML šaltiniai pateikti diagrams kataloge.

## 1 4 Vienas agentas ir dvi užklausos

Agentas gauna naują X, patikrina jo struktūrą, suformuoja užklausą, iškviečia Gemini ir validuoja y. Modelio generuojamas trumpas paaiškinimas sieja klaidą su konkrečiu kodu. Paslėpta modelio mąstymo grandinė neprašoma; tarpinius etapus rodo programos žurnalas.

### Zero shot pavyzdys

prompts/zero_shot.txt pateikta nauja įvestis be žinomų porų. Sutartyje nurodyta, kad count gali būti nulis ir tokiu atveju reikia grąžinti None.

```
def calculate_ratio(total, count):
    return total / count
```

Agentui nurodoma grąžinti vieną JSON objektą, identifikuoti pagrindinę problemą, tiksliai nurodyti eilutę, paaiškinti jos priežastį ir pateikti pataisytą fragmentą. Tikėtinas aptikimas šiame pavyzdyje yra dalybos iš nulio rizika. Tikrą Gemini atsakymą išsaugos 1.5 užrašinė.

### Few shot pavyzdys

prompts/few_shot.txt pateikta ta pati nauja įvestis ir trys anksčiau žinomos poros. Jos parinktos iš 1.2 duomenų, o jų identifikatoriai saugomi few_shot_ids.json.

| Pavyzdžio ID | Paskirtis |
| --- | --- |
| mutable_default-000-issue | Parodo bendro numatytojo sąrašo problemą |
| unsafe_eval-000-issue | Parodo nepatikimo kodo vykdymo problemą |
| division_zero-000-clean | Parodo tinkamą nulio tikrinimą ir atsakymą be problemos |

Few-shot režimas parodo norimą atsakymo struktūrą ir sprendimo pobūdį. Naujo X tikėtinas y į užklausą nededamas. Palyginimas turi naudoti tą patį modelį ir tą pačią naują įvestį abiem režimams.

### Svarbūs rezultatų laukai

has_issue nurodo, ar rasta problema. line skaičiuojama nuo 1 ir tikrinama pagal problematic_code. Kai problemos nėra, line yra null, issue_type ir severity yra none, o kodo laukai tušti. confidence yra nekalibruotas modelio įvertis, todėl jo negalima laikyti išmatuota teisingumo tikimybe.

## 1 5 Gemini demonstravimas Google Colab

Atverkite notebooks/Lab_1_5_Gemini.ipynb per Colab File → Upload notebook. Užrašinėje yra diegimo, failų paruošimo, saugaus rakto gavimo, įvesties, užklausų vykdymo ir rezultatų išsaugojimo langeliai.

### Saugus prisijungimas

Colab Secrets skiltyje sukurkite GEMINI_KEY ir leiskite šiai užrašinei jį naudoti. Raktas gaunamas per userdata.get ir perduodamas Gemini klientui. Jis neturi būti įrašomas į GitHub arba spausdinamas išvestyje.

```
from google.colab import userdata
from google import genai
GEMINI_KEY = userdata.get('GEMINI_KEY')
client = genai.Client(api_key=GEMINI_KEY)
```

Naudojamas google-genai SDK ir oficialiai dokumentuotas Interactions iškvietimas su JSON schema [4, 5]. Modelio nustatymas yra vienoje vietoje. Pateiktas gemini-3.8-flash pagal 2026-11-17 dokumentaciją; prieš vykdymą galima parinkti paskyroje prieinamą tekstinį modelį.

| Etapas | Matomas rezultatas |
| --- | --- |
| Įvesties supratimas | Eilučių skaičius, funkcijos, sintaksės patikra |
| Užklausos paruošimas | Instrukcija, X ir pasirinkti pavyzdžiai |
| Inferencija | Gemini grąžintas JSON kandidatas |
| Išvesties generavimas | Pydantic schema ir eilutės atitiktis, y bei trukmė |

### Refleksijos tekstas po paleidimo

Užrašinėje pateiktas aštuonių sakinių refleksijos tekstas su vietomis faktiniams rezultatams įrašyti. Aprašykite agento paskirtį, Gemini ir užklausų vaidmenį, gautą išvadą abiem režimais ir validaciją praėjusių atsakymų skaičių. Nurodykite konkretų skirtumą arba tai, kad jo nebuvo. Užbaikite realių duomenų ir žmogaus vertinimo poreikiu.

Į GitHub išsaugokite įvykdytą .ipynb su matomais rezultatais ir JSONL žurnalą. Vien pateiktas kodas dar neparodo, kad API demonstravimas įvyko.

## 1 6 RAG išplėtimas su ChromaDB

RAG padeda parinkti modeliui aktualų kontekstą konkrečiai įvesčiai. Naujas X paverčiamas vektoriumi, ChromaDB suranda tris artimiausius pavyzdžius, o jų poros pridedamos prie užklausos. Gemini gauna tiek naują kodą, tiek atrinktus peržiūrų pavyzdžius.

| Duomenų savybė | Reikšmė |
| --- | --- |
| RAG korpusas | 1200 sintetinių (X,y) porų |
| Sudėtis | 12 šeimų × 50 variantų × 2 būsenos |
| Pasiskirstymas | 600 su problema ir 600 tinkamų pagal sutartį |
| Atskira patikra | 24 įrašai, neįtraukti į ChromaDB |
| Embedding modelis | all-MiniLM-L6-v2 per ONNX |
| Paieška | X sutartis ir kodas, kosinusinis atstumas, k = 3 |

Duomenų bazėje saugomi X vektoriai ir porų metaduomenys. Tikėtinas y nenaudojamas skaičiuojant paieškos vektorių. Naudojamas Chroma PersistentClient, todėl duomenys saugomi vietiniame chroma_db kataloge. Užklausa su n_results=3 grąžina tris artimiausius rezultatus [6].

### Paleidimas

- Įkelkite Lab_1_6_RAG_ChromaDB.ipynb į Colab ir pridėkite GEMINI_KEY.

- Sugeneruokite duomenis, sukurkite vektorius ir patikrinkite, kad count yra 1200.

- Pateikite X, peržiūrėkite trijų atrinktų pavyzdžių ID, kodą ir atstumus.

- Peržiūrėkite papildytą užklausą ir sugeneruotą y; atsisiųskite rezultatus.

### Duomenų ribotumas

Variantai daugiausia skiriasi identifikatoriais ir scenarijaus žymomis. Toks kiekis atitinka mokomąjį minimumą, tačiau nepakeičia įvairių realių peržiūrų. Patikros fragmentai skiriasi struktūriniu apvalkalu ir neturi tikslių kopijų korpuse, bet apima tas pačias problemų šeimas. MiniLM nėra specialiai šiam lietuviško konteksto ir Python kodo rinkiniui pritaikytas modelis.

## Rezultatų vertinimas ir pateikimas

RAG pagerėjimą vertinkite tais pačiais 24 patikros pavyzdžiais, naudodami tą patį modelį ir parametrus. Užrašinėje nustatykite RUN_EVALUATION = True. Vienam kartojimui atliekami 48 iškvietimai. Temperatūra lygi nuliui, tačiau modelio atsakymai vis tiek gali kisti.

| Metrika | Be RAG | Su RAG |
| --- | --- | --- |
| Tinkamo atsakymo dalis | Įrašyti po vykdymo | Įrašyti po vykdymo |
| Problemos aptikimo tikslumas | Įrašyti po vykdymo | Įrašyti po vykdymo |
| Tipo nustatymo tikslumas | Įrašyti po vykdymo | Įrašyti po vykdymo |
| Precision, recall ir F1 | Įrašyti po vykdymo | Įrašyti po vykdymo |
| Vidutinė tinkamo atsakymo trukmė | Įrašyti po vykdymo | Įrašyti po vykdymo |

Aptikimo tikslumas yra teisingų has_issue sprendimų dalis iš visų bandymų. Precision parodo, kokia dalis pažymėtų problemų buvo tikros; recall – kokia dalis etaloninių problemų aptikta. API ir validavimo klaidos lieka bendrame tikslumo vardiklyje. Dėl nedidelės imties rezultatų negalima apibendrinti visiems Python projektams.

### Kas patikrinta prieš perduodant

Praėjo trys automatiniai testai: 1200 korpuso ir 24 patikros įrašų sintaksė bei etikečių atitiktis; netinkamos atsakymo eilutės atmetimas; agento grandinės vykdymas su imitaciniu tiekėju. Taip pat su tikru MiniLM modeliu sukurta 1200 įrašų ChromaDB ir patikrinta trijų artimiausių rezultatų paieška. Jos įrašas yra docs/semantic_retrieval_check.json, o DB kopija – data/chroma_db. Tikri Gemini atsakymai ir jų kokybė dar turi būti įvertinti Colab.

### Galutinis pateikimas

- GitHub turi matomus data, prompts, notebooks, src ir diagrams katalogus.

- Pridėta ranka braižyta 1.2 schema ir dviejų originalių Colab analizė.

- Pateiktos sugeneruotų NotebookLM produktų nuorodos ir išvados.

- Colab užrašinėse išsaugoti tikri atsakymai, RAG paieška ir matavimai.

- Abi refleksijos papildytos gautais rezultatais, nepalikti pildymo žymekliai.

## Šaltiniai ir pristatymo paaiškinimai

[1] Ramesh ir kt. Automated Code Review Using Large Language Models at Ericsson An Experience Report. 2025. https://arxiv.org/abs/2507.19115

[2] Sun ir kt. BitsAI-CR Automated Code Review via LLM in Practice. 2025. https://arxiv.org/abs/2501.15134

[3] Tufano ir kt. Towards Automating Code Review Activities. 2021. https://arxiv.org/abs/2101.02518

[4] Google AI for Developers. Text generation. https://ai.google.dev/gemini-api/docs/text-generation

[5] Google AI for Developers. Structured outputs. https://ai.google.dev/gemini-api/docs/structured-output

[6] Chroma Docs. Query and Get. https://docs.trychroma.com/docs/querying-collections/query-and-get

Techninė dokumentacija tikrinta 2026 m. lapkričio 17 d. Pavyzdžiai ir paaiškinimai pritaikyti šio laboratorinio projekto temai.

### Kaip paaiškinti X ir y

X yra tai, ką pateikiu sistemai: Python kodas ir elgesio sutartis. y yra tai, ką sistema grąžina: problema, jos vieta, paaiškinimas ir siūlomas pataisytas kodas. Porose etaloninis y yra žinomas iš anksto ir naudojamas kaip pavyzdys arba vertinimo pagrindas.

### Kaip paaiškinti vieną agentą

Vienas agentas valdo visą apdorojimą. Įvesties patikra, ChromaDB ir Gemini nėra atskiri savarankiškai sprendžiantys agentai. Tai vieno proceso komponentai, kuriuos iškviečia ta pati run_agent funkcija.

### Kaip paaiškinti RAG ir modelio mokymą

RAG nekeičia Gemini svorių. Jis pakeičia modelio gaunamą kontekstą, prieš užklausą surasdamas panašius pavyzdžius. Šiame darbe naudoju parengtą giliojo mokymosi modelį inferencijai ir vertinu jo atsakymus.
