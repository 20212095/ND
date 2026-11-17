# Giliuoju mokymusi pagrįstas Python kodo peržiūros asistentas

Martynas Zakrys · 1.1–1.6 laboratoriniai darbai · 2026-11-17

Agentas gauna Python kodą ir jo elgesio sutartį X, parenka kontekstą,
kreipiasi į Gemini ir grąžina validuotą JSON rezultatą y.
Tai parengtas demonstravimo projektas. Gemini atsakymai ir RAG pagerėjimo
matavimai turi būti gauti jūsų Colab paskyroje. Modelio svoriai šiame projekte nemokomi.

## Greita pradžia

1. Atverkite [Google Colab](https://colab.research.google.com/) ir rinkitės **File → Upload notebook**.
2. Įkelkite `notebooks/Lab_1_5_Gemini.ipynb`.
3. Colab **Secrets** skiltyje pridėkite `GEMINI_KEY` ir įjunkite užrašinės prieigą.
4. Paleiskite langelius iš eilės. Palyginimui atliekami 2 Gemini iškvietimai.
5. Išsaugokite užrašinę su gautais rezultatais ir papildykite refleksiją.
6. Taip pat paleiskite `notebooks/Lab_1_6_RAG_ChromaDB.ipynb`.
7. RAG palyginimui nustatykite `RUN_EVALUATION = True` (48 papildomi API iškvietimai).

Abi užrašinės savarankiškos: viduje yra supakuoti pagrindiniai projekto failai,
todėl prieš pirmą paleidimą nereikia turėti GitHub saugyklos. Colab vykdymui
reikia interneto ir jūsų paskyroje prieinamo Gemini modelio. Raktą susikurkite
[Google AI Studio](https://aistudio.google.com/apikey). Jo nesiųskite į GitHub.

## Dalių ir failų atitiktis

| Dalis | Parengti failai | Kas dar atliekama asmeninėje paskyroje |
| --- | --- | --- |
| 1.1 | `docs/Laboratoriniu_darbu_vadovas.docx`, 1.1 tekstas | Patikrinti sugeneruotus NotebookLM produktus, įdėti jų nuorodas |
| 1.2 | `data/`, `src/dataset.py`, `diagrams/process.puml` | Įkelti į GitHub, ranka perpiešti procesą, išnagrinėti dvi dėstytojo užrašines |
| 1.3 | `diagrams/use_case.puml`, `components.puml`, `sequence.puml` | Atvaizduoti PlantUML, pateikti diagramas su paaiškinimu |
| 1.4 | `prompts/` | GitHub saugykloje išsaugoti pavyzdžius |
| 1.5 | `notebooks/Lab_1_5_Gemini.ipynb`, `src/agent.py` | Paleisti su GEMINI_KEY, išsaugoti tikrus atsakymus ir refleksiją |
| 1.6 | `notebooks/Lab_1_6_RAG_ChromaDB.ipynb`, `src/rag.py`, `src/evaluate.py` | Sukurti ChromaDB, paleisti demonstravimą ir palyginimą, užpildyti refleksiją |

## GitHub įkėlimas

Sukurkite saugyklą, pavyzdžiui, `python-code-review-assistant`. Saugykloje turi
būti matomi šio katalogo failai ir katalogai. ZIP failą išskleiskite prieš įkėlimą.
Nepalikite viso projekto viename įkeltame ZIP faile, nes dėstytojas turi matyti
`/data/`, `/prompts/` ir `/notebooks/` turinį.

GitHub puslapyje rinkitės **Add file → Upload files** ir nutempkite projekto
failus bei katalogus. Pabaigoje išsaugokite pakeitimus su **Commit changes**.
Po realaus vykdymo pakeiskite užrašines jų įvykdytomis versijomis. Įvertinkite,
ar išvestyse nėra privačių duomenų. Šiame pavyzdyje naudojamas sintetinis kodas.

Vietiniai patikrinimai iš projekto šakninio katalogo:

```bash
python -m pip install -r requirements.txt
python -m src.dataset
python -m unittest discover -s tests -v
```

## Svarbios ribos

- 1 200 eilučių sugeneruota iš 12 šablonų šeimų. Tai nėra 1 200 nepriklausomų realių klaidų.
- 24 patikros pavyzdžiai turi kitą struktūrinį apvalkalą, tačiau tas pačias problemų šeimas. Tikslių kopijų nėra.
- `confidence` generuotose etiketėse yra šablono žyma; modelio `confidence` nėra kalibruota tikimybė.
- JSON schema ir eilutės atitiktis neįrodo semantinio teisingumo. Siūlomą pataisą turi patikrinti žmogus.
- Agentas pateikto kodo nevykdo. Vertinimas nenaudoja `exec` ar `eval` įvesties tikrinimui.
- Parengta ChromaDB kopija yra `data/chroma_db/`; visi 1200 pavyzdžių jau indeksuoti su MiniLM. Colab užrašinė ją iš naujo sukuria savo aplinkoje ir leidžia atsisiųsti rezultatų ZIP faile.
- Dviejų dėstytojo Colab dokumentų turinys šiame pakete neanalizuotas, nes jo nepavyko pasiekti. Žr. `docs/Destytojo_Colab_analize.md`.

## Šaltiniai

1. [Ericsson patirties ataskaita](https://arxiv.org/abs/2507.19115).
2. [BitsAI-CR](https://arxiv.org/abs/2501.15134).
3. [Towards Automating Code Review Activities](https://arxiv.org/abs/2101.02518).
4. [Gemini teksto generavimas](https://ai.google.dev/gemini-api/docs/text-generation).
5. [Gemini struktūrizuota išvestis](https://ai.google.dev/gemini-api/docs/structured-output).
6. [Chroma užklausos](https://docs.trychroma.com/docs/querying-collections/query-and-get).
