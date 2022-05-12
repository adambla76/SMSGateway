# SMSGateway
Bramka SMS służąca do wyświetlania wiadomości SMS na stronie WWW z użyciem Raspberry PI

  Do odbierania wiadomości SMS użyty został prosty moduł SIM800L widoczny poniżej 

![pol_pm_Miniaturowy-modul-GSM-SIM800L-MicroSim-TTL-GPRS-3-7-4-2V-11741_1](https://user-images.githubusercontent.com/17962241/168175874-df096f65-bb62-4700-a094-928223b65f3b.jpg)

  Moduł należy podłączyć za pomocą pinów RX / TX do Raspberry PI jak poniżej:
  
  


![6sQiFTKXhZptFiGnPlsc](https://user-images.githubusercontent.com/17962241/168176563-74a9d0e2-78fa-49c9-9df6-fb2d433c6efc.png)

Po uruchomieniu kodu SMSGateway.py na adresie localhost i porcie 8888 dostaniemy stronę WWW jak poniżej:

![scr1](https://user-images.githubusercontent.com/17962241/168176842-710fc101-33a2-46a8-9165-85e40a2a2ac1.jpg)

Po odebraniu SMS przez moduł GSM na stronie WWW pojawi się pełna treść SMS'a

![scr2](https://user-images.githubusercontent.com/17962241/168177478-78d1742b-3e03-415f-8425-260f89e6c052.jpg)

W przypadku kiedy SMS pochodzi z systemu bankowego ING i jest kodem potwierdzającym transakcję, aplikacja odczytuje SMS'a, wycina z niego najważniejsze informacje i prezentuje na stronie WWW w taki sposób aby kod był widoczny dla osoby słabowidzącej. Wystarczy kliknąć myszką na kod autoryzacyjny a zostanie on automatycznie skopiowany do schowka. Umożliwi to bardzo prostę wklejenie go do systemu transakcyjnego banku ING

![scr3](https://user-images.githubusercontent.com/17962241/168178077-479bf655-854d-4a6e-8ec9-75417eccb832.jpg)
