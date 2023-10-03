CREATE FUNCTION if EXISTS f_rate()
RETURNS INTEGER
LANGUAGE PLPGSQL
AS
$$
	DECLARE
		v_rate INTEGER;
		v_mas INTEGER[];
		v_origin varchar(255);
		v_value INTEGER;
	BEGIN

		EXECUTE "SELECT origin FROM main_catalog_fileds WHERE filed_name LIKE "|| <filed_name (сальдо)> into v_origin;
		EXECUTE "SELECT" || v_origin || "FROM csv_attributes WHERE inn LIKE" || <inn (23445667)> into v_value;

		IF сальдо>100 THEN
			v_mas[0] := 2;
		ELSE
			IF  вклад>300 THEN
				v_mas[0] := 5;
			ELSE
				v_mas[0] := 6;

		IF кредит>200 THEN
			v_mas[1] := 7;
		ELSE
			v_mas[1] := 9;

		IF штраф<300 THEN
			v_mas[2] := 11;
		ELSE
			v_mas[2] := 12;

				END IF;
			END IF;
		END IF;
		END IF;

		v_rate = v_mas[0] + v_mas[1] - v_mas[2];
		return v_rate;

	END;
$$;