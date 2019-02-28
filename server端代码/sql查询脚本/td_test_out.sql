create procedure td_test_out
@m nvarchar(max)
as
begin
--DECLARE @m nvarchar(MAX)
--DECLARE @n nvarchar(MAX)
DECLARE @p nvarchar(MAX)

/*
CREATE TABLE tmp_chenqi
(
test_id nvarchar(MAX),
test_name nvarchar(MAX),
test_step nvarchar(MAX),
test_des nvarchar(MAX),
test_exp nvarchar(MAX)
)
*/

--select * from ALL_LISTS where AL_DESCRIPTION = '快速测试'
--1
--select * from ALL_LISTS where AL_ABSOLUTE_PATH LIKE 'AAAKAM%'
--2
--select * from TEST WHERE TS_SUBJECT IN (select AL_ITEM_ID from ALL_LISTS where AL_ABSOLUTE_PATH LIKE 'AAAKAM%')
--3
--set @m = 'AAAKAM%'
--set @n = 'SELECT * from DESSTEPS WHERE DS_TEST_ID In (select TS_TEST_ID from TEST WHERE TS_SUBJECT IN (select AL_ITEM_ID from ALL_LISTS where AL_ABSOLUTE_PATH LIKE '''+@m+'''))' --'AAAKAM%'
--exec(@n)

--set @n = 'SELECT * from DESSTEPS WHERE DS_TEST_ID In (select TS_TEST_ID from TEST WHERE TS_SUBJECT IN (select AL_ITEM_ID from ALL_LISTS where AL_ABSOLUTE_PATH LIKE '''+@m+'''))'
--insert into tmp_alltest values('000','测试点','测试步骤','用例执行步骤','用例执行结果')
set @p = 'insert into tmp_alltest(test_id,test_step,test_des,test_exp) SELECT DS_TEST_ID,DS_STEP_NAME,DS_DESCRIPTION,DS_EXPECTED from DESSTEPS WHERE DS_TEST_ID In (select TS_TEST_ID from TEST WHERE TS_SUBJECT IN (select AL_ITEM_ID from ALL_LISTS where AL_ABSOLUTE_PATH LIKE '''+@m+'''))'
exec(@p)

--set @p = 'insert into tmp_chenqi(test_id,test_step,test_des,test_exp) SELECT DS_TEST_ID,DS_STEP_NAME,DS_DESCRIPTION,DS_EXPECTED from @n';
--exec(@p)

UPDATE tmp_alltest SET test_name = (select TS_NAME from TEST where tmp_alltest.test_id=TS_TEST_ID)

--SELECT * from tmp_alltest

--drop TABLE tmp_alltest

update tmp_alltest set test_name = REPLACE(test_name,CHAR(13),'<out>')
update tmp_alltest set test_name = REPLACE(test_name,CHAR(10),'<out>')
update tmp_alltest set test_step = REPLACE(test_step,CHAR(13),'<out>')
update tmp_alltest set test_step = REPLACE(test_step,CHAR(10),'<out>')
update tmp_alltest set test_des = REPLACE(test_des,CHAR(13),'<out>')
update tmp_alltest set test_des = REPLACE(test_des,CHAR(10),'<out>')
update tmp_alltest set test_exp = REPLACE(test_exp,CHAR(13),'<out>')
update tmp_alltest set test_exp = REPLACE(test_exp,CHAR(10),'<out>')
END
