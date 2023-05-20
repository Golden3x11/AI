% Odkurzacz
vacuum_cleaner(model_xyz).
battery_operated_vacuum_cleaner(model_xyz).
has(model_xyz, power_cable).
has(model_xyz, power_button).
has(model_xyz, battery).
has(model_xyz, filter).
has(model_xyz, dust_bag).
has(model_xyz, brush_roll).
has(model_xyz, power_led).
has(model_xyz, filter_led).
has(model_xyz, dust_bag_led).


% LED Stanów (Error, Power/BatteryLED, FilterLED, DustBagLED)
leds_state(turned_off, off, off, off).
leds_state(discharged, off, off, off).
leds_state(low_battery, blink, _, _).
leds_state(filter_issue, on, blink, _).
leds_state(filter_issue, blink, blink, _).
leds_state(full_dust_bag, on, _, blink).
leds_state(full_dust_bag, blink, _, blink).
leds_state(brush_roll_issue, on, on, on).

% Błędy i przyczyny
problem(not_turned_on, turned_off). % odkurzacz nie jest włączony
problem(no_battery, discharged). % odkurzacz jest rozładownay
problem(low_battery, low_battery). % niski poziom baterii
problem(dirty_filter, filter_issue). % zabrudzony filtr
problem(full_dust_bag, full_dust_bag). % pełny worek na kurz
problem(brush_roll_issue, brush_roll_issue). % problem z rolką

cause(power_button, not_turned_on). % odkurzacz nie jest włączony
cause(battery, no_battery). % odkurzacz jest rozładownay
cause(battery, low_battery). % niski poziom baterii
cause(filter, dirty_filter). % zabrudzony filtr
cause(dust_bag, full_dust_bag). % pełny worek na kurz
cause(brush_roll, brush_roll_issue). % problem z rolką

% Rozwiązania problemów
fix(turned_off, 'Włącz odkurzacz.').
fix(discharged, 'Bateria rozładowna, naładuj baterię odkurzacza.').
fix(low_battery, 'Naładuj baterię odkurzacza.').
fix(filter_issue, 'Wyczyść filtr odkurzacza.').
fix(full_dust_bag, 'Wymień pełny worek na kurz.').
fix(brush_roll_issue, 'Wyczyść rolkę odkurzacza.').

% Określanie stanu diod i rozwiązywanie problemów
define_led_state(Power, Filter, DustBag, Sucking, ERROR) :-
    leds_state(ERROR, Power, Filter, DustBag),
    problem(STATE, ERROR),
    ((STATE = no_battery; STATE = not_turned_on) -> Sucking = no; Sucking = weak).

define_solution(ERROR, ACTION) :-
    fix(ERROR, ACTION).

troubleshoot(_, _, _, ok, 'Odkurzacz działa poprawnie.').

troubleshoot(Power, Filter, DustBag, Sucking, ACTION) :-
    ((define_led_state(Power, Filter, DustBag, Sucking, ERROR),
    define_solution(ERROR, ACTION));
    ACTION = 'Sprawdź stan diod led').
