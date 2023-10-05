
IF выручка > 123 THEN
	mas[3] := 333;
ELSE
	mas[3] := 444;
IF вклад > 300 THEN
	mas[2] := 5;
ELSE
	mas[2] := mas[3];
IF сальдо + mas[2] > 100 THEN
	mas[1] := 2;
ELSE
	mas[1] := 10;