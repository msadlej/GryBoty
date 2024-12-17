# Cel projektu

Celem jest stworzenie systemu w formie aplikacji webowej, który pozwoli na porównywanie botów stworzonych do grania w deterministyczne gry dwuosobowe (np. kółko i krzyżyk, Connect Four) metodą turniejową. Aplikacja będzie służyć zarówno użytkownikom, którzy chcą przetestować swoje algorytmy w warunkach turniejowych, jak i organizatorom takich turniejów.

System zapewni możliwość rejestracji nowych użytkowników, logowania do konta oraz edycji profilu (np. zmiana hasła). System powinien pozwolić użytkownikom na wgranie kodu źródłowego bota napisanego w Pythonie 3 zgodnego z  przedefiniowanymi wymaganiami gry. Wymagania te określają przede wszystkim format kodu źródłowego zgodny z dostarczoną abstrakcyjną implementacją gry, obejmującą odpowiednie klasy i metody. 


Dodatkowo użytkownik powinien mieć możliwość wyboru turnieju, dołączenia do turnieju bota realizującego formułę gry w jakiej przeprowadzany jest turniej, oraz na wgląd do uzyskanych wyników (rezultatów rozgrywek turniejowych odbytych przed bota). Widok wyników powinien obejmować zarówno szczegóły rozgrywki (dokładny zapis ruchów bota oraz jego przeciwnika), jak i ogólny obraz wyników danego turnieju w formie drabinki turniejowej.


Ponadto, system powinien umożliwiać wyznaczonym użytkownikom (tzw. Użytkownikom Premium) na wgrywanie i konfigurację turnieju: dodanie do niego użytkowników, usuwanie z niego użytkowników, ustalenie limitu graczy, ustawienie daty rozpoczęcia oraz wgląd do wyników turnieju, a także edycję warunków turnieju po jego ogłoszeniu. Użytkownicy Premium powinni móc zaprosić innych użytkowników na podstawie wygenerowanego unikalnego dla turnieju kodu dołączenia oraz mieć sposobność banowania/odbanowania (uniemożliwienia/umożliwienia użytkownikom brania udziału w turniejach oraz tworzenia botów) użytkowników, którzy np. naruszyli zasady bezpieczeństwa systemu lub otrzymali kod dołączenia do turnieju w niepożądany sposób od osób trzecich. 

W systemie będzie istniał jeden główny administrator - tzw. Superużytkownik z uprawnieniami Użytkownika Premium, którego kompetencje będą ponadto rozszerzone o możliwość nadawania zwykłym użytkownikom statusu Użytkownika Premium mogącego tworzyć turnieje. 

Dodatkowo realizowany projekt powinien zapewnić  uczciwość i bezpieczeństwo systemu, zatem system będzie odpowiednio izolował środowisko wykonawcze wgrywanych botów, zapobiegając nieautoryzowanemu dostępowi do zasobów systemu.
