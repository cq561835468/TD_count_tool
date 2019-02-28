create procedure tablecreattmp_rule6
as
begin
create table tmp_rule6
(
CY_CYCLE varchar(2000),
ST_TEST_ID nvarchar(2000),
ST_TEST_NAME nvarchar(2000),
ST_USER  nvarchar(2000),
ST_RUN_NAME  nvarchar(2000),
ST_STATUS nvarchar(2000),
ST_EXECUTION_DATE nvarchar(2000),
ST_EXECUTION_TIME nvarchar(2000),
ST_DESCRIPTION nvarchar(2000),
ST_EXPECTED nvarchar(2000)
)
end