create procedure td_rule_5
@a nvarchar(max)
as
begin
--DECLARE @a nvarchar(2000)
DECLARE @b nvarchar(2000)

--set @a = 'AAAA%'

set @b = 'INSERT INTO tmp_rule5
select TC_CYCLE_ID,TC_TEST_ID,TC_STATUS,TC_EXEC_DATE,TC_EXEC_TIME,TC_ACTUAL_TESTER from TESTCYCL where TC_CYCLE_ID in 
(select CY_CYCLE_ID from CYCLE where CY_folder_id IN (select CF_ITEM_ID from CYCL_FOLD where CF_ITEM_PATH like '''+@a+'''))'
EXEC(@b)

UPDATE tmp_rule5 set TC_CYCLE_ID = (select CY_CYCLE from CYCLE where tmp_rule5.TC_CYCLE_ID = cycle.cy_cycle_id)
UPDATE tmp_rule5 set TC_TEST_ID = (select TS_NAME from test where tmp_rule5.TC_TEST_ID = test.ts_test_id)

--select * from tmp_rule5

end