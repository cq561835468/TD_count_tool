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
--��������
--set @path = 'AAAKAB%'
--set @table = 'testadmin_test_db'
--TRUNCATE TABLE tmp7
--��ʱtmp1д����ļ��к�������
set nocount on 
set @sql3 = 'insert into ##tmp1 SELECT [AL_ITEM_ID],[AL_FATHER_ID],[AL_DESCRIPTION],[AL_ABSOLUTE_PATH] FROM '+@table+'.[dbo].[ALL_LISTS] where AL_ABSOLUTE_PATH like '''+@path+''' '
exec(@sql3)



--��������aaa д����ʱtmp2 ����tmp1��AL_ITEM_ID��TS_TEST_ID
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
--�رո���aaa д��##tmp2

--�����ͷ
insert into tmp7 values('������','���Ե�','000','���Բ���','״̬','����ִ������','����ִ��ʱ��','����ִ�в���','����ִ�н��','���Բ���ID','�����������')

--��������bbb д��tmp7 ����tmp2 TS_TEST_ID��ִ�й��Ĳ�������
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
--�رո���aaa д��tmp7

--д��##tmp3 ��Ҫ��ȡ������Ͳ��Ե��ST_RUN_ID
set @zero = '000'
set @sql6 = 'insert into ##tmp3(ST_RUN_ID)
select distinct ST_RUN_ID from '+@table+'.[dbo].tmp7 where ST_RUN_ID != '+@zero+''
exec(@sql6)

--��������ccc д��##tmp3 ����ST_RUN_ID�Ĳ��Ե�Ͳ�����
DECLARE ccc CURSOR for select ST_RUN_ID from [dbo].##tmp3
Open ccc
fetch next from ccc into @temp_temp 
while @@fetch_status=0
begin
    --��ȡrun���cycle_id
	set @cy_run = (select RN_CYCLE_ID from [dbo].[RUN] where RN_RUN_ID = @temp_temp)
	--����run���cycle_id��ȡcycle���CY_CYCLE
	set @cy_name = (select CY_CYCLE from [dbo].[CYCLE] where CY_CYCLE_ID = @cy_run)
	--����ȡ��CY_CYCLE���µ�##tmp3��
	set @sql8 = 'update ##tmp3 set CY_CYCLE = (select CY_CYCLE from [dbo].[CYCLE] where CY_CYCLE_ID = '+@cy_run+') where ST_RUN_ID = '+@temp_temp+''
	exec(@sql8)
	--����run���cycle_id��ȡcycle���CY_FOLDER_ID
	set @cy_name = (select CY_FOLDER_ID from [dbo].[CYCLE] where CY_CYCLE_ID = @cy_run)
	--����CY_FOLDER_ID��ȡCYCL_FOLD�����ϼ��ļ���
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
	--����ȡ��CF_ITEM_name���µ�##tmp3��
	update ##tmp3 set CF_ITEM_NAME = @father_name
	fetch next from ccc into @temp_temp 
end
Close ccc
Deallocate ccc

--��������ddd д��tmp7 ����ST_RUN_ID�Ĳ��Ե�Ͳ�����
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