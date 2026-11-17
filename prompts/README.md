# 1.4 Vieno AI agento užklausos

`system.txt` apibrėžia agento užduotį, atsakymo schemą ir taisyklę kodą laikyti duomenimis.
`template.txt` yra bendras šablonas. `zero_shot.txt` pateikia vieną naują X be
žinomų pavyzdžių. `few_shot.txt` pateikia tą patį X ir tris žinomus (X,y) iš 1.2.
`few_shot_ids.json` saugo jų tikslius identifikatorius. Užrašinės ir `build_prompt`
naudoja tuos pačius failus; naujo X etiketė į užklausą nepatenka.

Zero-shot parodo, kaip modelis vykdo vien instrukciją. Few-shot iš anksto
parodo norimą atsakymo formą, klaidos aiškinimą ir atvejį be problemos.
RAG režime tris pastovius pavyzdžius pakeičia trys automatiškai atrinkti
pavyzdžiai pagal X semantinį vektorių. Visi režimai grąžina tą pačią y schemą.
