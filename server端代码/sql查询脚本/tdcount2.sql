create procedure tdcount2
	@testname nvarchar(max),
	@n nvarchar(max)
as
begin
declare @cpi nvarchar(max)
DECLARE @count2 int
DECLARE @count3 int
declare @group nvarchar(max)
declare @group2 nvarchar(max)
declare @s nvarchar(max)
create table ##te2
(
long nvarchar(max),
name nvarchar(max)
)
create table ##tmp2 
(
RN_CYCLE_ID int,
RN_TEST_ID int,
RN_RUN_ID int,
RN_RUN_NAME  varchar(2000),
RN_TESTER_NAME  varchar(2000)
)

create table ##tmp5
(
id int,
name int,
fold varchar(2000),
)

--set @n = 'testadmin_test_db'
--set @testname = 'chenqi'
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
		
set @s = 'insert into ##tmp2	
select RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_TESTER_NAME 
from '+@n+'.dbo.RUN
where RN_CYCLE_ID in 
(select CY_CYCLE_ID 
from '+@n+'.dbo.CYCLE
where CY_FOLDER_ID in (SELECT CF_ITEM_ID FROM '+@n+'.dbo.CYCL_FOLD where CF_ITEM_PATH like '''+@group2+'''))'
exec(@s)

insert into ##tmp5
select RN_CYCLE_ID,RN_TEST_ID,RN_TESTER_NAME from ##tmp2
group by RN_CYCLE_ID,RN_TEST_ID,RN_TESTER_NAME
having(count(*))>1

set @count3 = @count3 + 1
end
drop table ##tmp2
SELECT COUNT(*) from ##tmp5 where fold = @testname
drop table ##tmp5
drop table ##te2
end