﻿CREATE FUNCTION if EXISTS f_rate()
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

			ELSE
выручка123					v_mas[0] := 123;
				ELSE
					v_mas[0] := 333;
				ELSE
					v_mas[0] := 444;
			ELSE
выручка123					v_mas[0] := 123;
				ELSE
					v_mas[0] := 333;
				ELSE
					v_mas[0] := 444;
			ELSE
выручка123					v_mas[0] := 123;
				ELSE
					v_mas[0] := 333;
				ELSE
					v_mas[0] := 444;
100					v_mas[0] := 100;
				ELSE
					v_mas[0] := 2;
				ELSE
					v_mas[0] := 10;

				END IF;
			END IF;
				END IF;

		v_rate = v_mas[0] + v_mas[1];
		return v_rate;

	END;
$$;