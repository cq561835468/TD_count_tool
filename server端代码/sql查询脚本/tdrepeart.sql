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
--������������������������ϵ
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
--������ʱ##tmp�������������Ĳ������������Ĺ�ϵ
exec(@s)

set @u = 'insert into ##tmp2
select RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_TESTER_NAME 
from '+@n+'.[dbo].[RUN]
where RN_CYCLE_ID in 
(select CY_CYCLE_ID 
from '+@n+'.[dbo].[CYCLE] 
where CY_FOLDER_ID in (SELECT CF_ITEM_ID FROM '+@n+'.[dbo].[CYCL_FOLD] where CF_ITEM_PATH like '''+@m+'''))order by RN_Run_ID desc'
exec(@u)
--����##tmp2���У����ϲ���������в�������������Ӧ��ϵ 

set @count = (SELECT COUNT(*) from ##tmp)
set @nowco = 0
insert into tmp4 values('������','���Ե�','0','���Բ���','״̬','����ִ������','����ִ��ʱ��','����ִ�в���','����ִ�н��','0')
while(@nowco < @count) 
begin 
set @ID = (select top 1 id from ##tmp)              --RN_TEST_ID
set @name =  (select top 1 name from ##tmp)		  --RN_TESTER_NAME
set @fold = (select top 1 fold from ##tmp)		  --RN_CYCLE_ID  ��Ӧ��С���Ե�
--------------------------------------##tmp1��##tmp2��ȡ##tmp3��
insert into ##tmp3(RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_TESTER_NAME)
select top 1 * 
from ##tmp2 
where RN_TEST_ID=@ID and RN_TESTER_NAME=@name and RN_CYCLE_ID=@fold 
order by RN_Run_ID desc
--��ȡ##tmp3��RN_RUN_ID
------------------------------------------��ȡ##tmp3��һ��runid cycle_id test_id
set @runid = (select top 1 RN_RUN_ID from ##tmp3)
set @cycle_id = (select top 1 RN_CYCLE_ID from ##tmp3)
set @test_id = (select top 1 RN_TEST_ID from ##tmp3)
------------------------------------------����##tmp3��RN_CYCLE_name
set @updata_cycle = '
update '+@n+'.[dbo].[##tmp3] set RN_CYCLE_name = (select CY_CYCLE from '+@n+'.[dbo].[CYCLE] where CY_CYCLE_ID = '+@cycle_id+')where RN_CYCLE_ID = '+@cycle_id+''
exec(@updata_cycle)
------------------------------------------����##tmp3��RN_TEST_name
set @updata_test_name = '
update '+@n+'.[dbo].[##tmp3] set RN_TEST_name = (select TS_NAME from '+@n+'.[dbo].[TEST] where TS_TEST_ID = '+@test_id+')where RN_TEST_ID = '+@test_id+''
exec(@updata_test_name)
-----------------------------------------д��tmp4 ���Ϲ��˳���runid��STEP
set @p = 'insert into tmp4(ST_TEST_ID,ST_STEP_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME,ST_DESCRIPTION,ST_EXPECTED,RUN_ID)
select ST_TEST_ID,ST_STEP_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME,ST_DESCRIPTION,ST_EXPECTED,ST_RUN_ID
from '+@n+'.[dbo].[STEP] 
where ST_RUN_ID = '+@runid+''
exec(@p)
------------------------------------------���·��ϸ�runid��STEP��ST_MIN_TEST��ST_TEST_PROJECT
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