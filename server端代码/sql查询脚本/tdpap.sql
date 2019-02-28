create procedure tdpap
	@testname nvarchar(max),
	@n nvarchar(max)
as
begin
create table ##te2
(
long nvarchar(max),
name nvarchar(max)
)
create table ##tmp
(
id int,
name varchar(max),
fold int
)
--保存测试人与用例，测试项关系
create table ##tmp2 
(
RN_CYCLE_ID int,
RN_TEST_ID int,
RN_RUN_ID int,
RN_RUN_NAME  varchar(max),
RN_TESTER_NAME  varchar(max)
)
--保存符合过滤规则的用例

create table ##tmp3 
(
RN_CYCLE_ID int,
RN_TEST_ID int,
RN_RUN_ID int,
RN_RUN_NAME  varchar(max),
RN_TESTER_NAME  varchar(max)
)
create table ##tmp4
(
ST_STEP_NAME varchar(max),
ST_STATUS varchar(max),
ST_EXECUTION_DATE varchar(max),
ST_EXECUTION_TIME  varchar(max),
ST_DESCRIPTION  varchar(max),
ST_EXPECTED varchar(max)
)
DECLARE @count2 int
DECLARE @count3 int
DECLARE @count4 int
DECLARE @s nvarchar(max)
DECLARE @u nvarchar(max)
DECLARE @p nvarchar(max)
DECLARE @ID int
DECLARE @name varchar(max)
DECLARE @fold int
DECLARE @count int
DECLARE @nowco int
DECLARE @runid varchar(max)
DECLARE @out varchar(max)
DECLARE @pu varchar(max)
declare @a nvarchar(max)
declare @co int 
declare @cpi nvarchar(max)
declare @group nvarchar(max)
declare @group2 nvarchar(max)
declare @pp nvarchar(max)
--------------------------------------------------------------------------------------------表-----------------------------
truncate table testadmin_test_db.dbo.tmp5

--set @n = 'kdm39_2800v1r2_db'
--set @testname = 'pangxiaowei'
	set @cpi = 'insert into ##te2
	select [CF_ITEM_PATH],[CF_ITEM_NAME] from '+@n+'.[dbo].[CYCL_FOLD] where len([CF_ITEM_PATH])=5'
	exec(@cpi)
	set @count2 = (SELECT COUNT(*) from ##te2)
	set @count3 = 1
	while (@count3<=@count2)
		begin
		set @group = (select top 1 long from ##te2)
		delete ##te2 where long=@group
		set @group2 = @group + '%'
-------------------------------------------------------------------------------------------------------
print @n
print @group2
print @testname
set @s = 'insert into ##tmp 
select distinct RN_TEST_ID,RN_TESTER_NAME,RN_CYCLE_ID
from '+@n+'.[dbo].[RUN]
where RN_CYCLE_ID in 
(select CY_CYCLE_ID 
from '+@n+'.[dbo].[CYCLE] 
where CY_FOLDER_ID in (SELECT CF_ITEM_ID FROM '+@n+'.[dbo].[CYCL_FOLD] where CF_ITEM_PATH like '''+@group2+'''))
and RN_TESTER_NAME = '''+@testname+''''
set nocount on
exec(@s)

set @u = 'insert into ##tmp2
select RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_TESTER_NAME 
from '+@n+'.[dbo].[RUN]
where RN_CYCLE_ID in 
(select CY_CYCLE_ID 
from '+@n+'.[dbo].[CYCLE] 
where CY_FOLDER_ID in (SELECT CF_ITEM_ID FROM '+@n+'.[dbo].[CYCL_FOLD] where CF_ITEM_PATH like '''+@group2+'''))'
--插入tmp2表中，符合测试项的所有测试者与用例对应关系 （过滤了重复TEST_ID与多余的字段)
exec(@u)

set @count = (SELECT COUNT(*) from ##tmp2)
set @nowco = 0
while(@nowco < @count) 
	begin 
	set @ID = (select top 1 id from ##tmp)
	set @name =  (select top 1 name from ##tmp)
	set @fold = (select top 1 fold from ##tmp)
	insert into ##tmp3
	select top 1 * 
	from ##tmp2 
	where RN_TEST_ID=@ID and RN_TESTER_NAME=@name and RN_CYCLE_ID=@fold 
	order by RN_Run_ID desc
	set @runid = (select top 1 RN_RUN_ID from ##tmp3)
	set @pp = 'insert into testadmin_test_db.dbo.tmp5
	select ST_STEP_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME,ST_DESCRIPTION,ST_EXPECTED
	from '+@n+'.[dbo].[STEP] 
	where ST_RUN_ID = '+@runid+''
	exec(@pp)
	set @p = 'insert into ##tmp4
	select ST_STEP_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME,ST_DESCRIPTION,ST_EXPECTED
	from '+@n+'.[dbo].[STEP] 
	where ST_RUN_ID = '+@runid+''
	exec(@p)
	delete ##tmp where id=@ID and name=@name and fold=@fold
	delete ##tmp2 where RN_TEST_ID=@ID and RN_TESTER_NAME=@name and RN_CYCLE_ID=@fold
	delete ##tmp3 where RN_RUN_ID = @runid
	set @nowco = @nowco +1
	end --step循环
-------------------------------------------------------------------------------------------------------
		set @count3 = @count3 + 1
		end --组循环
		--insert into tmp6 values (@n,@ddd)
	set @a = @a +1 
update testadmin_test_db.dbo.tmp5 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(13),'<out>')
update testadmin_test_db.dbo.tmp5 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(10),'<out>')
update testadmin_test_db.dbo.tmp5 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(13),'<out>')
update testadmin_test_db.dbo.tmp5 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(10),'<out>')
SELECT COUNT(*) from ##tmp4
drop table ##te2
drop table ##tmp
drop table ##tmp2
drop table ##tmp3
drop table ##tmp4
end