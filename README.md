# SMSGateway - bramka SMS dla osób słabowidzących 
Projekt praktycznej bramka SMS służąca do wyświetlania wiadomości tekstowej na stronie WWW z użyciem Raspberry PI. Litery na stronie WWW są bardzo duże i jaskrawe ze względu na fakt że użytkownikiem tego systemu jest osoba bardzo słabo widząca. Dzięki temu rozwiązaniu osoba taka bez problemu może dokonywać transakcji na swoim koncie w banku ING, co w przypadku próby odczytu SMSa na ekranie telefony nie było możliwe


  Do odbierania wiadomości SMS użyty został prosty moduł SIM800L widoczny poniżej 

![pol_pm_Miniaturowy-modul-GSM-SIM800L-MicroSim-TTL-GPRS-3-7-4-2V-11741_1](https://user-images.githubusercontent.com/17962241/168175874-df096f65-bb62-4700-a094-928223b65f3b.jpg)

  Moduł należy podłączyć za pomocą pinów RX / TX do Raspberry PI jak poniżej:
  
  


![6sQiFTKXhZptFiGnPlsc](https://user-images.githubusercontent.com/17962241/168176563-74a9d0e2-78fa-49c9-9df6-fb2d433c6efc.png)

Istnieje również możliwość skorzystania z adaptera RS232-USB (FTDI lub CH340), który należy podłączyć do jednego z wejść USB, a następnie zdefiniować w proramie port szeregowy jako /dev/ttyUSB. Po uruchomieniu kodu SMSGateway.py na adresie localhost i porcie 8888 zobaczymy stronę WWW jak poniżej:

![scr1](https://user-images.githubusercontent.com/17962241/168176842-710fc101-33a2-46a8-9165-85e40a2a2ac1.jpg)

Po odebraniu wiadomości SMS przez moduł GSM po chwili na stronie WWW pojawi się poniższa zawartość
![scr2](https://user-images.githubusercontent.com/17962241/168177478-78d1742b-3e03-415f-8425-260f89e6c052.jpg)

W przypadku kiedy SMS pochodzi z systemu bankowego ING i jest kodem potwierdzającym transakcję, aplikacja parsuje wiadomość SMS, wycina z niej najważniejsze informacje i prezentuje na stronie WWW w taki sposób aby kod autoryzacyjny i kwota były widoczne dla osoby słabowidzącej. Wystarczy kliknąć myszką na kod autoryzacyjny a zostanie on automatycznie skopiowany do schowka. Umożliwi to bardzo proste wklejenie go do systemu transakcyjnego banku ING i realizację przelewu

![scr3](https://user-images.githubusercontent.com/17962241/168178077-479bf655-854d-4a6e-8ec9-75417eccb832.jpg)

Dodatkowo skrypt SMSGateway potrafi odpowiadać na pewne ustalowe komendy i odsyła wynik SMS'em na numer nadawcy. Dostępne komendy to:

     #restart -  restartuje Raspberry PI i odsyła SMS o wykonaniu zadania
     #refresh  -  restartuje serwis flask w przypadku zawieszenia
     #info     -  odsyła zwrotnie tekst "Thanks I'm fine my Lord!"
     #test     -  odsyła SMSem spreparowany tekst wiadomości autoryzacyjnej (dla testów)
     ?         -  wysyła SMSem zestaw wszystkich dostępnych komend
     
     przykładowo w treści SMS wpisujemy słowo #reboot i wysyłamy go na numer bramki GSM  - po odebraniu wiadomości skrypt wykona restart RaspberryPI.
   
   
    
