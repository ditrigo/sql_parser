CREATE FUNCTION if EXISTS f_rate()
RETURNS INTEGER
LANGUAGE PLPGSQL
AS 
$$
    DECLARE
        v_rate INTEGER;
        v_origin varchar(255);
        v_value INTEGER;
    BEGIN

        EXECUTE "select origin from main_catalog_fileds where filed_name like "|| <filed_name (сальдо) НАДО ВСТАВИТЬ ИЗ ЗАПРОСА> into v_origin;
        EXECUTE "select "|| v_origin || "from csv_attributes where inn like" || <inn (23445667) НАДО ВСТАВИТЬ ИЗ ЗАПРОСА> into v_value;

        IF v_value > 100 THEN
            v_rate := 2;
        ELSE
            v_rate := 0;
        end IF;
        
        return v_rate;
    END;
$$ d