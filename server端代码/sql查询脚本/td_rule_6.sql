create procedure td_rule_6
@m nvarchar(max)
as
begin
DECLARE @sql1 nvarchar(max)
--DECLARE @m nvarchar(max)
DECLARE @temp_temp nvarchar(max)
DECLARE @temp_temp2 nvarchar(max)
DECLARE @temp_temp3 nvarchar(max)
DECLARE @Priority nvarchar(max)
DECLARE @sql_status nvarchar(max)
DECLARE @sql_status_value nvarchar(max)

-------####tmp_f_1原始数据与不重复数据用例
create table ##tmp_f_1
(
CF_ITEM_NAME varchar(max),
CY_CYCLE varchar(max),
RN_TEST_ID  varchar(max),
RN_RUN_ID  varchar(max)
)
--------###tmp_f_2重复数据用例
create table ##tmp_f_2
(
CF_ITEM_NAME varchar(max),
CY_CYCLE varchar(max),
ST_RUN_ID varchar(max),
ST_TEST_ID nvarchar(max),
ST_RUN_NAME  varchar(max),
ST_STATUS varchar(max),
ST_EXECUTION_DATE varchar(max),
ST_EXECUTION_TIME varchar(max),
ST_DESCRIPTION varchar(max),
ST_EXPECTED varchar(max),
ST_Priority varchar(max) default 0
)
--------###tmp_f_3过滤完成的数据用例
create table ##tmp_f_3
(
CY_CYCLE varchar(max),
ST_TEST_ID nvarchar(max),
ST_TEST_NAME nvarchar(max),
ST_RUN_ID varchar(max),
ST_RUN_NAME  varchar(max),
ST_STATUS varchar(max),
ST_EXECUTION_DATE varchar(max),
ST_EXECUTION_TIME varchar(max),
ST_DESCRIPTION varchar(max),
ST_EXPECTED varchar(max)
)

--set nocount on 
--自定义数据
--Truncate table tmp4
--set @m = 'AAABAAA%'

--select * from ##tmp4
--插入表头
insert into tmp_rule6 values('测试项 ','测试ID','测试点','执行人','测试步骤','状态','用例执行日期','用例执行时间','用例执行步骤','用例执行结果')

--写入##tmp_f_1原始数据,所有执行的用例
set @sql1 = 
'insert into ##tmp_f_1(CF_ITEM_NAME,CY_CYCLE,RN_TEST_ID,RN_RUN_ID)
select CF.CF_ITEM_NAME,C.CY_CYCLE,R.RN_TEST_ID,R.RN_RUN_ID
from CYCL_FOLD as CF,CYCLE as C ,RUN as R
where CF_ITEM_ID = C.CY_FOLDER_ID and C.CY_CYCLE_ID = R.RN_CYCLE_ID AND CF.CF_ITEM_PATH LIKE '''+@m+''''
exec(@sql1)

--写入##tmp_f_2原始数据,所有执行的用例
insert into ##tmp_f_2
select t1.CF_ITEM_NAME,t1.CY_CYCLE,st.ST_RUN_ID,t1.RN_TEST_ID,st.ST_STEP_NAME,st.ST_STATUS,st.ST_EXECUTION_DATE,st.ST_EXECUTION_TIME,st.ST_DESCRIPTION,st.ST_EXPECTED,0
from ##tmp_f_1 as t1,step as st
where t1.RN_RUN_ID = st.ST_RUN_ID 

--游标1 ST_TEST_ID
DECLARE aaa CURSOR for select distinct ST_TEST_ID from ##tmp_f_2
Open aaa
fetch next from aaa into @temp_temp 
while @@fetch_status=0
begin
set @Priority = 1
	--select * from ##tmp_f_2 where ST_TEST_ID = @temp_temp
	--select * from ##tmp_f_2 where ST_TEST_ID = @temp_temp
	--游标2 ST_DESCRIPTION
	DECLARE bbb CURSOR for select distinct ST_RUN_NAME from ##tmp_f_2 where ST_TEST_ID = @temp_temp
	Open bbb
	fetch next from bbb into @temp_temp2
	while @@fetch_status=0
	begin
		--select * from ##tmp_f_2 where ST_RUN_NAME = @temp_temp2 and ST_TEST_ID = @temp_temp
		--游标3 ST_STATUS
		DECLARE ccc CURSOR for select ST_RUN_ID from ##tmp_f_2 where ST_RUN_NAME = @temp_temp2 and ST_TEST_ID = @temp_temp
		Open ccc
		fetch next from ccc into @temp_temp3
		while @@fetch_status=0
		begin
		set @sql_status = (select ST_STATUS from ##tmp_f_2 where  cast(ST_RUN_NAME as varbinary)= cast(@temp_temp2 as varbinary) and ST_TEST_ID = @temp_temp and ST_RUN_ID = @temp_temp3)
		print @sql_status
		if (@sql_status= 'Failed' or @sql_status= 'Passed')
			begin
				print 'okk'
				update ##tmp_f_2 set ST_Priority = @Priority where ST_RUN_NAME = @temp_temp2 and ST_TEST_ID = @temp_temp and ST_RUN_ID = @temp_temp3
				set @Priority = @Priority +1
			end
		fetch next from ccc into @temp_temp3
		end
		Close ccc    
		Deallocate ccc 
		------------------------------，每个step处理完成后插入表中--------------------------
	insert into ##tmp_f_3 select top 1 CY_CYCLE,ST_TEST_ID,ST_TEST_ID,ST_RUN_ID,ST_RUN_NAME,ST_STATUS,ST_EXECUTION_DATE,ST_EXECUTION_TIME,ST_DESCRIPTION,ST_EXPECTED
	from ##tmp_f_2 where ST_RUN_NAME = @temp_temp2 and ST_TEST_ID = @temp_temp order by St_Priority+0 desc, ST_EXECUTION_DATE desc,ST_EXECUTION_TIME desc 

	fetch next from bbb into @temp_temp2 
	end
	Close bbb    
	Deallocate bbb 
	
fetch next from aaa into @temp_temp 
end
Close aaa    
Deallocate aaa 

----------------------------更新用例名称-----------
update ##tmp_f_3 SET ST_TEST_NAME = (select TS_NAME from TEST where TEST.TS_TEST_ID = ##tmp_f_3.ST_TEST_ID)
----------------------------更新执行人名称-----------
--select * from ##tmp_f_3
update ##tmp_f_3 SET ST_RUN_ID = (select RN_TESTER_NAME from RUN where RUN.RN_RUN_ID = ##tmp_f_3.ST_RUN_ID)

insert into tmp_rule6 select * from ##tmp_f_3 

--select * from tmp_rule6

update tmp_rule6 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(13),'<out>')
update tmp_rule6 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(10),'<out>')
update tmp_rule6 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(9),'<out>')
update tmp_rule6 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(13),'<out>')
update tmp_rule6 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(10),'<out>')
update tmp_rule6 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(9),'<out>')
update tmp_rule6 set ST_RUN_NAME = REPLACE(ST_RUN_NAME,CHAR(13),'<out>')
update tmp_rule6 set ST_RUN_NAME = REPLACE(ST_RUN_NAME,CHAR(10),'<out>')
update tmp_rule6 set ST_RUN_NAME = REPLACE(ST_RUN_NAME,CHAR(9),'<out>')


drop table ##tmp_f_1
drop table ##tmp_f_2
drop table ##tmp_f_3
end