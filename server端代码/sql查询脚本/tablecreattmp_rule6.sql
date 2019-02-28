create procedure tablecreattmp_rule6
as
begin
create table tmp_rule6
(
CY_CYCLE varchar(max),
ST_TEST_ID nvarchar(max),
ST_TEST_NAME nvarchar(max),
ST_USER  nvarchar(max),
ST_RUN_NAME  nvarchar(max),
ST_STATUS nvarchar(max),
ST_EXECUTION_DATE nvarchar(max),
ST_EXECUTION_TIME nvarchar(max),
ST_DESCRIPTION nvarchar(max),
ST_EXPECTED nvarchar(max)
)
end