# X ir y duomenys

`examples.jsonl` yra 1 200 porų RAG korpusas. `holdout.jsonl` turi 24 atskirus
demonstracinio vertinimo įrašus. `examples_small.json` pateikia tris 1.4 dalies
few-shot pavyzdžius. `demo_input.json` yra nauja įvestis abiem 1.5 režimams.

X struktūra: `language` (python), `code` (kodo fragmentas), `contract` (tikėtinas elgesys).
y struktūra: `has_issue`, `issue_type`, `severity`, `line`, `problematic_code`,
`explanation`, `recommendation`, `suggested_code`, `confidence`.

Pavyzdys: `def calculate_ratio(total, count): return total / count` turi
problemą, jeigu sutartyje leidžiama `count=0` ir reikalaujama grąžinti `None`.
Išvestyje nurodoma `has_issue=true`, `issue_type=runtime`, `severity=high`,
probleminė eilutė ir pataisa su nulio patikra. Jei sutartis uždraustų nulį,
tos pačios išvados be papildomo pagrindo daryti negalima.

## Generavimo metodika

`python -m src.dataset` deterministiškai atkuria rinkinius. Korpusas sudarytas
iš 12 šeimų, po 50 variantų ir po dvi būsenas (klaidinga / tinkama).
Taigi 12 × 50 × 2 = 1 200; 600 turi problemą, 600 jos neturi pagal nagrinėjamą
aspektą. Variantai daugiausia keičia identifikatorius ir scenarijaus žymą.
Įrašai pažymėti `source=synthetic_template`, patikros įrašai `synthetic_holdout`.

Šeimos: bendras numatytasis sąrašas, eval, pickle, YAML UnsafeLoader, SQL ir
shell įterpimas, HTTP timeout, platus išimčių gaudymas, failo uždarymas,
dalyba iš nulio, intervalo ribos ir None tikrinimas.

Etiketės nustatytos pagal šablono sutartį. `confidence=1.0` etiketėje nereiškia
išmatuotos modelio tikimybės. Tai deterministinio žymėjimo reikšmė.
AST tikrinimas patvirtina sintaksę, bet ne visos programos veikimo teisingumą.

## Duomenų atskyrimas

ChromaDB gauna visą 1 200 porų korpusą, o 24 patikros poros į jį nepatenka.
Patikros funkcijos perkeltos į klasę su staticmethod. SHA-256 patikra neleidžia
tikslioms kodo kopijoms sutapti. Abi imtys apima tas pačias problemų šeimas,
todėl tai yra demonstracinis, o ne nepriklausomas pramoninis vertinimas.
Moksliniam palyginimui reikėtų realių pavyzdžių, ekspertinio žymėjimo ir
atskyrimo pagal šaltinio projektą arba visas šablonų šeimas.
