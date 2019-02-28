create procedure tablecreate_tmp_rule5
as
begin
create table tmp_rule5
(
TC_CYCLE_ID varchar(2000),
TC_TEST_ID varchar(2000),
TC_STATUS varchar(2000),
TC_EXEC_DATE varchar(2000),
TC_EXEC_TIME varchar(2000),
TC_ACTUAL_TESTER  varchar(max)
)
end