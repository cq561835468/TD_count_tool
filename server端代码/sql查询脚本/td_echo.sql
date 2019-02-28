create procedure td_echo
@path varchar(max),
@table varchar(max)
as
begin
declare @temp_temp varchar(max) 
declare @sql1 varchar(max) 
declare @sql2 varchar(max) 
declare @sql3 varchar(max) 
declare @sql4 varchar(max)
declare @sql5 varchar(max)
declare @sql6 varchar(max)
declare @sql7 varchar(max)
declare @sql8 varchar(max)
declare @zero varchar(max) 
declare @cy_run varchar(max) 
declare @cy_name varchar(max)
declare @cy_fol varchar(max)
declare @father_id varchar(max)
declare @father_name varchar(max)

create table ##tmp1
(
AL_ITEM_ID varchar(max),
AL_FATHER_ID varchar(max),
AL_DESCRIPTION varchar(max),
AL_ABSOLUTE_PATH  varchar(max),
)

create table ##tmp2
(
TS_TEST_ID varchar(max),
)

create table ##tmp3
(
CF_ITEM_NAME varchar(max),
CY_CYCLE varchar(max),
ST_RUN_ID varchar(max),
)
--测试数据
--set @path = 'AAAKAB%'
--set @table = 'testadmin_test_db'
--TRUNCATE TABLE tmp7
--临时tmp1写入该文件夹和其子项
set nocount on 
set @sql3 = 'insert into ##tmp1 SELECT [AL_ITEM_ID],[AL_FATHER_ID],[AL_DESCRIPTION],[AL_ABSOLUTE_PATH] FROM '+@table+'.[dbo].[ALL_LISTS] where AL_ABSOLUTE_PATH like '''+@path+''' '
exec(@sql3)



--开启浮标aaa 写入临时tmp2 符合tmp1的AL_ITEM_ID的TS_TEST_ID
DECLARE aaa CURSOR for select AL_ITEM_ID FROM [dbo].##tmp1
Open aaa
fetch next from aaa into @temp_temp 
while @@fetch_status=0
begin
	set @sql1 = 'insert into ##tmp2 SELECT TS_TEST_ID from '+@table+'.[dbo].[TEST] where TS_SUBJECT = '+@temp_temp+''
	exec(@sql1)
	fetch next from aaa into @temp_temp 
end
Close aaa    
Deallocate aaa 
--关闭浮标aaa 写入##tmp2

--插入表头
insert into tmp7 values('测试项','测试点','000','测试步骤','状态','用例执行日期','用例执行时间','用例执行步骤','用例执行结果','测试步骤ID','测试用例编号')

--开启浮标bbb 写入tmp7 符合tmp2 TS_TEST_ID的执行过的测试用例
DECLARE bbb CURSOR for select TS_TEST_ID FROM [dbo].##tmp2
Open bbb
fetch next from bbb into @temp_temp 
while @@fetch_status=0
begin
	set @sql2 = 'insert into tmp7(ST_RUN_ID,ST_STEP_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME,ST_DESCRIPTION,ST_EXPECTED,ST_STEP_ID,ST_TEST_ID) 
	SELECT ST_RUN_ID,ST_STEP_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME,ST_DESCRIPTION,ST_EXPECTED,ST_STEP_ID,ST_TEST_ID from '+@table+'.[dbo].[step] where ST_TEST_ID = '+@temp_temp+' order by ST_TEST_ID'
	exec(@sql2)
	fetch next from bbb into @temp_temp 
end
Close bbb
Deallocate bbb
--关闭浮标aaa 写入tmp7

--写入##tmp3 需要获取测试项和测试点的ST_RUN_ID
set @zero = '000'
set @sql6 = 'insert into ##tmp3(ST_RUN_ID)
select distinct ST_RUN_ID from '+@table+'.[dbo].tmp7 where ST_RUN_ID != '+@zero+''
exec(@sql6)

--开启浮标ccc 写入##tmp3 符合ST_RUN_ID的测试点和测试项
DECLARE ccc CURSOR for select ST_RUN_ID from [dbo].##tmp3
Open ccc
fetch next from ccc into @temp_temp 
while @@fetch_status=0
begin
    --获取run表的cycle_id
	set @cy_run = (select RN_CYCLE_ID from [dbo].[RUN] where RN_RUN_ID = @temp_temp)
	--根据run表的cycle_id获取cycle表的CY_CYCLE
	set @cy_name = (select CY_CYCLE from [dbo].[CYCLE] where CY_CYCLE_ID = @cy_run)
	--将获取的CY_CYCLE更新到##tmp3中
	set @sql8 = 'update ##tmp3 set CY_CYCLE = (select CY_CYCLE from [dbo].[CYCLE] where CY_CYCLE_ID = '+@cy_run+') where ST_RUN_ID = '+@temp_temp+''
	exec(@sql8)
	--根据run表的cycle_id获取cycle表的CY_FOLDER_ID
	set @cy_name = (select CY_FOLDER_ID from [dbo].[CYCLE] where CY_CYCLE_ID = @cy_run)
	--根据CY_FOLDER_ID获取CYCL_FOLD的最上级文件夹
	set @father_id = (select CF_FATHER_ID from dbo.CYCL_FOLD where CF_ITEM_ID = @cy_name)
	set @father_name = (select CF_ITEM_NAME from dbo.CYCL_FOLD where CF_ITEM_ID = @cy_name)
	--print 'father_id is '+@father_id
	--print 'father_name is '+@father_name
	while @father_id !=0
	begin
		set @father_name = (select CF_ITEM_NAME from dbo.CYCL_FOLD where CF_ITEM_ID = @father_id)
		set @father_id = (select CF_FATHER_ID from dbo.CYCL_FOLD where CF_ITEM_ID = @father_id)
		--print 'father_id is '+@father_id
		--print 'father_name is '+@father_name
	end
	--将获取的CF_ITEM_name更新到##tmp3中
	update ##tmp3 set CF_ITEM_NAME = @father_name
	fetch next from ccc into @temp_temp 
end
Close ccc
Deallocate ccc

--开启浮标ddd 写入tmp7 符合ST_RUN_ID的测试点和测试项
DECLARE ddd CURSOR for select ST_RUN_ID from [dbo].##tmp3
Open ddd
fetch next from ddd into @temp_temp 
while @@fetch_status=0
begin
	print @temp_temp
	update dbo.tmp7 set ST_MIN_TEST = (select CF_ITEM_NAME from ##tmp3 where ST_RUN_ID = @temp_temp)
		           ,ST_TEST_PROJECT = (select CY_CYCLE from ##tmp3 where ST_RUN_ID = @temp_temp) 
		           where ST_RUN_ID = @temp_temp
	fetch next from ddd into @temp_temp 
end
Close ddd
Deallocate ddd


update dbo.tmp7 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(13),'<out>')
update dbo.tmp7 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(10),'<out>')
update dbo.tmp7 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(13),'<out>')
update dbo.tmp7 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(10),'<out>')
update dbo.tmp7 set ST_STEP_NAME = REPLACE(ST_STEP_NAME,CHAR(13),'<out>')
update dbo.tmp7 set ST_STEP_NAME = REPLACE(ST_STEP_NAME,CHAR(10),'<out>')



--select * from ##tmp1
--select * from ##tmp2
--select * from ##tmp3
select * from tmp7

--print 'test'
drop table ##tmp1
drop table ##tmp2
drop table ##tmp3
end