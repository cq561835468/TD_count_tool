create procedure tdpicture
@m nvarchar(max),
@n nvarchar(max)
as
begin
declare @s nvarchar(max)
declare @w nvarchar(max)
declare @c nvarchar(max)
declare @count int
declare @nowco int
create table ##tmp 
(
RN_CYCLE_ID int,
RN_TEST_ID int,
RN_RUN_ID int,
RN_RUN_NAME  varchar(2000)
)

create table ##tmp2 
(
ST_RUN_ID varchar(2000),
ST_STEP_NAME varchar(2000),
ST_STATUS varchar(2000),
ST_EXECUTION_DATE varchar(2000),
ST_EXECUTION_TIME varchar(2000),
ST_TEST_ID varchar(2000)
)

--set @n = N'testadmin_test_db'
--set @m = N'AAAAAAAAA%'

--------------------------------------------获取符合所选轮次下的所有RN_RUN_ID
set @s = 'insert into ##tmp
select RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME 
from '+@n+'.[dbo].[RUN]
where RN_CYCLE_ID in 
(select CY_CYCLE_ID 
from '+@n+'.[dbo].[CYCLE] 
where CY_FOLDER_ID in (SELECT CF_ITEM_ID FROM '+@n+'.[dbo].[CYCL_FOLD] where CF_ITEM_PATH like '''+@m+'''))order by RN_Run_ID desc'
exec(@s)
----------------------------------------------------------------------------------
set @count = (SELECT COUNT(*) from ##tmp)
set @nowco = 0
while (@nowco < @count)
begin
----------------------------------------------------使用RN_RUN_ID获取符合的所有Step
set @w = (select top 1 RN_RUN_ID from ##tmp)
set @c = 'insert into ##tmp2
select ST_RUN_ID,ST_STEP_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME,ST_TEST_ID
from '+@n+'.[dbo].[STEP]
where ST_RUN_ID = '+@w+''
exec(@c)
set @nowco = @nowco +1
delete ##tmp where RN_RUN_ID = @w
end
----------------------------------------------------------------------------------------
insert into tmp6
select ST_STEP_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME from ##tmp2 t1 where not exists(select * from ##tmp2 where ST_STEP_NAME=t1.ST_STEP_NAME and ST_EXECUTION_DATE=t1.ST_EXECUTION_DATE and ST_TEST_ID=t1.ST_TEST_ID and ST_RUN_ID > t1.ST_RUN_ID)ORDER BY ST_EXECUTION_DATE
drop table ##tmp
drop table ##tmp2
end