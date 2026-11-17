# UML ir proceso schemos

`.puml` failai yra tekstinis PlantUML kodas. Nukopijuokite visą failo turinį
į [PlantUML redaktorių](https://www.plantuml.com/plantuml/uml/) ir išsaugokite SVG arba PNG.

Prie kiekvieno `.puml` jau pridėtas vietoje atvaizduotas `.svg` ir `.png` failas.
Diagramų vaizdus galima peržiūrėti iš karto, o šaltinius naudoti pakeitimams.

- `use_case.puml`: programuotojo veiksmai ir Gemini kaip išorinis komponentas.
- `components.puml`: Colab, vienas agentas, embedding modelis, ChromaDB ir Gemini.
- `sequence.puml`: X perdavimas, pasirinktinas RAG, generavimas ir validacija.
- `process.puml`: sprendimų šakos ir viso apdorojimo veiklos eiga.

1.2 daliai ranka perpieškite procesą iš `process.puml` arba žemiau pateikto
aprašymo. Išsaugokite nuskenuotą ranka braižytą schemą šiame kataloge.
Sugeneruotas PlantUML failas nepakeičia dėstytojo prašomo rankinio brėžinio.

Pradžia → X → įvesties patikra → RAG režimo pasirinkimas. Pasirinkus RAG,
apskaičiuojamas vektorius ir iš ChromaDB paimami 3 pavyzdžiai. Kita šaka
naudoja zero-shot arba pastovius few-shot pavyzdžius. Toliau šakos susijungia:
užklausa → Gemini → JSON validacija. Tinkamas atsakymas pateikiamas naudotojui,
netinkamas baigiasi aiškia klaida. Pažymėkite AI dalį ties Gemini inferencija.

`architecture.png` yra aiškinamoji komponentų ryšių iliustracija vadove.
UML pateikimui naudokite atitinkamus `.puml` šaltinius.
