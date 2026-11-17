# Atlikti techniniai patikrinimai

Patikrinta 2026-11-17.

- 1 200 korpuso ir 24 atskirų patikros įrašų Python sintaksė, unikalumas ir kodo eilučių etiketės.
- Visų tikėtinų y atitiktis Pydantic schemai ir ryšiui su atitinkama X eilute.
- Netinkamo atsakymo eilutės atmetimas.
- Visas agento vykdymas su imitaciniu modelio atsakymu.
- Chroma PersistentClient įrašymas ir trijų artimiausių vektorių užklausa.
- Tikras all-MiniLM-L6-v2 semantinių vektorių sudarymas visiems 1 200 įrašų.
- Naujo patikros fragmento paieška; rezultatai pateikti `semantic_retrieval_check.json`.
- Abiejų `.ipynb` Python langelių vykdymas laikinoje aplinkoje: tikra MiniLM ir ChromaDB, imituotas Gemini tiekėjas ir Colab paslapčių bei atsisiuntimo sąsajos. Diegimo langelis nepaleistas iš naujo, nes priklausomybės įdiegtos atskirai.
- Įdiegtos google-genai 3.4.0 Interactions užklausos schemos atitiktis SDK tipams.
- PlantUML šaltinių vietinis atvaizdavimas ir Word vadovo puslapių vaizdinė patikra.

Gemini API su tikru asmeniniu raktu nepaleista. Tokių bandymų išvestys ir RAG
kokybės matavimai nebuvo sukurti ar imituoti kaip tikri rezultatai. Galutinį
demonstravimą ir refleksijas reikia atlikti Colab paskyroje.
