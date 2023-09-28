from datetime import date

STRIPPED_DATE_STRINGS_TO_TEST_1=["Zaktualizowano 2 dni temu", "Lokalnie", "Oferta Lokalnie", "cze 23."]

DESIRED_DATE_STRINGS_1=["2 dni", "", "Oferta ", "cze 23."]

STRIPPED_DATE_STRINGS_TO_TEST_2=["5 min", "45 s", "4 g", "cze 23.",
                    "sty 1.", "maj 3. 2021", "sty 23. 2022"]

DESIRED_DATE_STRINGS_2=[date.today().strftime("%Y-%m-%d"), date.today().strftime("%Y-%m-%d"),
                    date.today().strftime("%Y-%m-%d"), "2023-06-23", "2023-01-01", "2021-05-03",
                    "2022-01-23"]