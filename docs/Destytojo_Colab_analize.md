# 1.2 laboratorinis darbas. Dviejų „Colab“ užrašinių analizė

Abi užrašinės sudaro vieną procesą. Pirmoji iš vaizdo įrašo išskiria garsą, atpažįsta kalbą ir išsaugo vieną vaizdo kadrą. Antroji paima šį kadrą ir sugeneruoja jo aprašymą. Užrašines jungia „Google Drive“ saugomas archyvas `frame-data.zip`.

## 1. Vaizdo įrašo apdorojimas

Užrašinės `Demo_video_multimodal_extraction.ipynb` įvestis X yra MP4 vaizdo įrašas. Išvestį y sudaro garso takelis, ištartos kalbos tekstas ir vidurinis vaizdo kadras.

1. Programa su `kagglehub` atsisiunčia vaizdo įrašus iš „Kaggle“ rinkinio `csanskriti/video-and-audio-samples`.
2. `MoviePy` iš kiekvieno MP4 įrašo ištraukia garso takelį ir išsaugo jį MP3 formatu.
3. `Whisper` modelis `medium` atpažįsta garso takelyje ištartus žodžius. Programa įrašo tekstą į TXT failą.
4. Programa padalija įrašo trukmę iš dviejų ir tuo laiko momentu paima vieną kadrą. Pavyzdžiui, iš 10 sekundžių įrašo ji paimtų kadrą ties 5-ąja sekunde. Kadras išsaugomas JPG formatu.
5. Transkripcijos sudedamos į `text-data.zip`, o kadrai – į `frame-data.zip`. Abu archyvai išsaugomi „Google Drive“. MP3 failai lieka „Colab“ darbo aplinkoje.

Užrašinės išvestyje užfiksuoti penki išsaugoti viduriniai kadrai. Toks būdas leidžia trumpai pavaizduoti kiekvieną įrašą, tačiau viename kadre gali nesimatyti kitu metu vykusio veiksmo.

## 2. Vaizdo kadro aprašymo generavimas

Užrašinės `Demo_image_description_generation.ipynb` modelio įvestis X yra paveikslas ir tekstinė instrukcija. Išvestis y yra tekstinis aprašymas, ką modelis atpažino paveiksle.

1. Programa perskaito `GOOGLE_API_KEY` iš „Colab Secrets“, prijungia „Google Drive“ ir išpakuoja pirmosios užrašinės sukurtą `frame-data.zip`.
2. Kiekvieną kadrą kartu su instrukcija „Please describe what is in this image.“ ji siunčia modeliui `gemma-3-27b-it`.
3. Modelio atsakymas gaunamas dalimis. Programa jas sujungia ir išsaugo atskirame TXT faile. Paveikslo ir aprašymo failų vardai sutampa iki plėtinio, todėl galima nustatyti, kuriam kadrui priklauso aprašymas.
4. Visi aprašymai supakuojami į `image-descriptions.zip` ir išsaugomi „Google Drive“.

Užrašinės išvestyje užfiksuoti penki sugeneruoti aprašymai. Pirmojoje užrašinėje gauta transkripcija perteikia, kas įraše buvo pasakyta. Antrosios užrašinės aprašymas perteikia, kas matoma pasirinktame kadre. Generuodamas šį aprašymą modelis gauna tik vaizdą ir instrukciją.

## 3. Ryšys su mano Python kodo peržiūros asistentu

Mano sistemos įvestis X yra Python kodas ir elgesio sutartis, kurioje nurodyta, kaip kodas turėtų veikti. Agentas patikrina kodo struktūrą ir paruošia užklausą. RAG režimu iš „ChromaDB“ jis papildomai atrenka tris panašiausius pavyzdžius. „Gemini“ sugeneruoja kodo peržiūrą, o agentas patikrina JSON struktūrą ir tai, ar nurodyta probleminė eilutė atitinka pateiktą kodą.

Mano bandyme funkcijos `calculate_ratio(total, count)` sutartyje buvo nurodyta grąžinti `None`, kai `count` lygus nuliui. Tačiau antroje eilutėje funkcija iš karto vykdė `return total / count`. Išvestyje y modelis nurodė šią eilutę, paaiškino dalybos iš nulio problemą ir pasiūlė prieš dalijant patikrinti `count`. Taip galėjau palyginti modelio pastabą su konkrečia kodo eilute ir pradiniu reikalavimu.
