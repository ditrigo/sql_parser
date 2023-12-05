CREATE FUNCTION if EXISTS f_rate()
RETURNS INTEGER
LANGUAGE PLPGSQL
AS
$$
    DELCARE
        v_rate INTEGER;
        v_mas INTEGER[];
        v_origin varchar(255);
        v_value INTEGER;
    BEGIN
        EXECUTE "SELECT origin FROM main_catalog_fileds WHERE filed_name LIKE "|| <filed_name (сальдо)> into v_origin;
        EXECUTE "SELECT" || v_origin || "FROM csv_attributes WHERE inn LIKE" || <inn (23445667)> into v_value;


IF выручка > 123 THEN
	v_mas[3] := 333;
ELSE
	v_mas[3] := 444;
IF вклад > 300 THEN
	v_mas[2] := 5;
ELSE
	v_mas[2] := v_mas[3];
IF сальдо + v_mas[2] > 100 THEN
	v_mas[1] := 2;
ELSE
	v_mas[1] := 10;
END IF;
END IF;
END IF;

v_result = v_mas[1];

IF долг < 500 THEN
	v_mas[2] := 13;
ELSE
	v_mas[2] := 17;
IF v_mas[2] - кредит > 200 THEN
	v_mas[1] := 7;
ELSE
	v_mas[1] := 9;
END IF;
END IF;

v_result = v_result + v_mas[1];

IF штраф < 300 THEN
	v_mas[1] := 11;
ELSE
	v_mas[1] := 12;
END IF;

v_result = v_result - v_mas[1];

		return v_result;
	END;
$$