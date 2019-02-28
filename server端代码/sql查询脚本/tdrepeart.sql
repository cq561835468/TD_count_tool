create procedure tdrepeart
@m nvarchar(max),
@n nvarchar(max)
as
begin
DECLARE @s nvarchar(2000)
DECLARE @u nvarchar(2000)
DECLARE @p nvarchar(2000)
DECLARE @ID int
DECLARE @name nvarchar(2000)
DECLARE @fold nvarchar(2000)
DECLARE @count int
DECLARE @nowco int
DECLARE @runid nvarchar(2000)
DECLARE @out nvarchar(2000)
DECLARE @pu nvarchar(2000)
DECLARE @TEST_NAME nvarchar(2000)
DECLARE @cycle_id nvarchar (2000)
DECLARE @test_id nvarchar (2000)
DECLARE @cycle_id_tmp4 nvarchar (2000)
DECLARE @test_id_tmp4 nvarchar (2000)
DECLARE @updata_cycle nvarchar(2000)
DECLARE @updata_test_name nvarchar(2000)
DECLARE @updata_end_ST_MIN_TEST nvarchar(2000)
DECLARE @updata_end_ST_TEST_PROJECT nvarchar(2000)
DECLARE @replace_one nvarchar(2000)
DECLARE @replace_two nvarchar(2000)
DECLARE @replace_three nvarchar(2000)
DECLARE @replace_four nvarchar(2000)
DECLARE @replace_five nvarchar(2000)
DECLARE @replace_sex nvarchar(2000)
create table ##tmp
(
id int,
name varchar(2000),
fold int
)
--保存测试人与用例，测试项关系
create table ##tmp2 
(
RN_CYCLE_ID int,
RN_TEST_ID int,
RN_RUN_ID int,
RN_RUN_NAME  varchar(2000),
RN_TESTER_NAME  varchar(2000)
)
create table ##tmp3 
(
RN_CYCLE_ID int,
RN_CYCLE_name varchar(2000),
RN_TEST_ID int,
RN_TEST_name varchar(2000),
RN_RUN_ID int,
RN_RUN_NAME  varchar(max),
RN_TESTER_NAME  varchar(max),
)

set @s = 'insert into ##tmp 
select distinct RN_TEST_ID,RN_TESTER_NAME,RN_CYCLE_ID
from '+@n+'.[dbo].[RUN]
where RN_CYCLE_ID in 
(select CY_CYCLE_ID 
from '+@n+'.[dbo].[CYCLE] 
where CY_FOLDER_ID in (SELECT CF_ITEM_ID FROM '+@n+'.[dbo].[CYCL_FOLD] where CF_ITEM_PATH like '''+@m+'''))'
--插入临时##tmp表中搜索出来的测试者与用例的关系
exec(@s)

set @u = 'insert into ##tmp2
select RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_TESTER_NAME 
from '+@n+'.[dbo].[RUN]
where RN_CYCLE_ID in 
(select CY_CYCLE_ID 
from '+@n+'.[dbo].[CYCLE] 
where CY_FOLDER_ID in (SELECT CF_ITEM_ID FROM '+@n+'.[dbo].[CYCL_FOLD] where CF_ITEM_PATH like '''+@m+'''))order by RN_Run_ID desc'
exec(@u)
--插入##tmp2表中，符合测试项的所有测试者与用例对应关系 

set @count = (SELECT COUNT(*) from ##tmp)
set @nowco = 0
insert into tmp4 values('测试项','测试点','0','测试步骤','状态','用例执行日期','用例执行时间','用例执行步骤','用例执行结果','0')
while(@nowco < @count) 
begin 
set @ID = (select top 1 id from ##tmp)              --RN_TEST_ID
set @name =  (select top 1 name from ##tmp)		  --RN_TESTER_NAME
set @fold = (select top 1 fold from ##tmp)		  --RN_CYCLE_ID  对应最小测试点
--------------------------------------##tmp1与##tmp2获取##tmp3表
insert into ##tmp3(RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_TESTER_NAME)
select top 1 * 
from ##tmp2 
where RN_TEST_ID=@ID and RN_TESTER_NAME=@name and RN_CYCLE_ID=@fold 
order by RN_Run_ID desc
--获取##tmp3的RN_RUN_ID
------------------------------------------获取##tmp3第一行runid cycle_id test_id
set @runid = (select top 1 RN_RUN_ID from ##tmp3)
set @cycle_id = (select top 1 RN_CYCLE_ID from ##tmp3)
set @test_id = (select top 1 RN_TEST_ID from ##tmp3)
------------------------------------------更新##tmp3的RN_CYCLE_name
set @updata_cycle = '
update '+@n+'.[dbo].[##tmp3] set RN_CYCLE_name = (select CY_CYCLE from '+@n+'.[dbo].[CYCLE] where CY_CYCLE_ID = '+@cycle_id+')where RN_CYCLE_ID = '+@cycle_id+''
exec(@updata_cycle)
------------------------------------------更新##tmp3的RN_TEST_name
set @updata_test_name = '
update '+@n+'.[dbo].[##tmp3] set RN_TEST_name = (select TS_NAME from '+@n+'.[dbo].[TEST] where TS_TEST_ID = '+@test_id+')where RN_TEST_ID = '+@test_id+''
exec(@updata_test_name)
-----------------------------------------写入tmp4 符合过滤出的runid的STEP
set @p = 'insert into tmp4(ST_TEST_ID,ST_STEP_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME,ST_DESCRIPTION,ST_EXPECTED,RUN_ID)
select ST_TEST_ID,ST_STEP_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME,ST_DESCRIPTION,ST_EXPECTED,ST_RUN_ID
from '+@n+'.[dbo].[STEP] 
where ST_RUN_ID = '+@runid+''
exec(@p)
------------------------------------------更新符合该runid的STEP的ST_MIN_TEST和ST_TEST_PROJECT
set @updata_end_ST_MIN_TEST = '
update '+@n+'.[dbo].[tmp4] set [ST_MIN_TEST] = (select RN_CYCLE_name from '+@n+'.[dbo].[##tmp3] where RN_RUN_ID = '+@runid+') where ST_TEST_ID = '+@test_id+''
exec(@updata_end_ST_MIN_TEST)

set @updata_end_ST_TEST_PROJECT = 'update '+@n+'.[dbo].[tmp4] set [ST_TEST_PROJECT] = (select RN_TEST_name from '+@n+'.[dbo].[##tmp3] where RN_RUN_ID = '+@runid+') where ST_TEST_ID = '+@test_id+''
exec(@updata_end_ST_TEST_PROJECT)

set @replace_one = 'update '+@n+'.dbo.tmp4 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(13),'''+'<out>'+''')'
set @replace_two = 'update '+@n+'.dbo.tmp4 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(10),'''+'<out>'+''')'
set @replace_three = 'update '+@n+'.dbo.tmp4 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(13),'''+'<out>'+''')'
set @replace_four = 'update '+@n+'.dbo.tmp4 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(10),'''+'<out>'+''')'
set @replace_five = 'update '+@n+'.dbo.tmp4 set ST_STEP_NAME = REPLACE(ST_STEP_NAME,CHAR(13),'''+'<out>'+''')'
set @replace_sex = 'update '+@n+'.dbo.tmp4 set ST_STEP_NAME = REPLACE(ST_STEP_NAME,CHAR(10),'''+'<out>'+''')'
exec(@replace_one)
exec(@replace_two)
exec(@replace_three)
exec(@replace_four)
exec(@replace_five)
exec(@replace_sex)

delete ##tmp where id=@ID and name=@name and fold=@fold
delete ##tmp2 where RN_TEST_ID=@ID and RN_TESTER_NAME=@name and RN_CYCLE_ID=@fold
delete ##tmp3 where RN_RUN_ID = @runid
set @nowco = @nowco +1
end
drop table ##tmp
drop table ##tmp2
drop table ##tmp3
end