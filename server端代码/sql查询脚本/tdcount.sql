create procedure tdcount
	@m nvarchar(max),
	@n nvarchar(max)
as
begin
declare @s nvarchar(max)
--declare @m nvarchar(max)
--declare @n nvarchar(max)
create table ##tmp2 
(
RN_CYCLE_ID int,
RN_TEST_ID int,
RN_RUN_ID int,
RN_RUN_NAME  varchar(max),
RN_TESTER_NAME  varchar(max)
)
--保存符合过滤规则的用例

create table ##tmp5
(
id int,
name int,
)

--set @n = N'testadmin_test_db'
--set @m = N'AAAAB%'
--set @s = 'select RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_TESTER_NAME from '+@n+'.dbo.RUN where RN_CYCLE_ID in (select CY_CYCLE_ID from '+@n+'.dbo.CYCLE where CY_FOLDER_ID in (SELECT CF_ITEM_ID FROM '+@n+'.dbo.CYCL_FOLD where CF_ITEM_PATH like '''+@m+'''))'
set @s = 'insert into ##tmp2
select RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_TESTER_NAME 
from '+@n+'.dbo.RUN
where RN_CYCLE_ID in 
(select CY_CYCLE_ID 
from '+@n+'.dbo.CYCLE
where CY_FOLDER_ID in (SELECT CF_ITEM_ID FROM '+@n+'.dbo.CYCL_FOLD where CF_ITEM_PATH like '''+@m+'''))'
exec(@s)

insert into ##tmp5
select RN_CYCLE_ID,RN_TEST_ID from ##tmp2
group by RN_CYCLE_ID,RN_TEST_ID
having(count(*))>1

SELECT COUNT(*) from ##tmp5
drop table ##tmp2
drop table ##tmp5
end