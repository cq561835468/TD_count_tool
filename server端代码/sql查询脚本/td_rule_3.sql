create procedure td_rule_3
@m nvarchar(max)
as
begin
DECLARE @sql1 nvarchar(2000)
DECLARE @sql2 nvarchar(2000)
DECLARE @sql3 nvarchar(2000)
--DECLARE @m nvarchar(2000)
DECLARE @temp_temp nvarchar(2000)
DECLARE @temp_temp2 nvarchar(2000)

-------####tmp_f_1原始数据与不重复数据用例
create table ##tmp_f_1
(
CF_ITEM_NAME varchar(2000),
CY_CYCLE varchar(2000),
RN_CYCLE_ID int,
RN_TEST_ID  varchar(2000),
RN_RUN_ID  varchar(2000),
RN_RUN_NAME varchar(2000),
RN_STATUS varchar(2000),
RN_TESTER_NAME varchar(2000),
RN_number varchar(2000) default 0,
RN_number_f_p varchar(2000) default 0
)
--------###tmp_f_2重复数据用例
create table ##tmp_f_2
(
CF_ITEM_NAME varchar(2000),
CY_CYCLE varchar(2000),
RN_CYCLE_ID int,
RN_TEST_ID  varchar(2000),
RN_RUN_ID  varchar(2000),
RN_RUN_NAME varchar(2000),
RN_STATUS varchar(2000),
RN_TESTER_NAME varchar(2000),
RN_number varchar(2000) default 0,
RN_number_f_p varchar(2000) default 0
)

--------###tmp_f_3不重复数据step
create table ##tmp_f_3
(
ST_MIN_TEST varchar(max),
ST_TEST_PROJECT varchar(max),
ST_TEST_ID varchar(max),
ST_STEP_NAME varchar(max),
ST_STATUS varchar(max),
ST_EXECUTION_DATE varchar(max),
ST_EXECUTION_TIME  varchar(max),
ST_DESCRIPTION  varchar(max),
ST_EXPECTED varchar(max),
RUN_ID varchar(max)
)


--##tmp_f_5重复用例step
create table ##tmp_f_5
(
ST_MIN_TEST varchar(max),
ST_TEST_PROJECT varchar(max),
ST_TEST_ID varchar(max),
ST_STEP_NAME varchar(max),
ST_STATUS varchar(max),
ST_EXECUTION_DATE varchar(max),
ST_EXECUTION_TIME  varchar(max),
ST_DESCRIPTION  varchar(max),
ST_EXPECTED varchar(max),
RUN_ID varchar(max),
ST_STEP_ID varchar(max),
ST_number_f_p varchar(2000) default 0
)

set nocount on 
--自定义数据
--Truncate table tmp4
--set @m = 'AAAAB'


--插入表头
insert into tmp4 values('测试项 ','测试点 ','000','测试步骤','status','用例执行日期','用例执行时间','用例执行步骤','用例执行结果','000')

--写入##tmp_f_1原始数据
set @sql1 = 
'insert into ##tmp_f_1(CF_ITEM_NAME,CY_CYCLE,RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_STATUS,RN_TESTER_NAME)
select CF.CF_ITEM_NAME,C.CY_CYCLE,R.RN_CYCLE_ID,R.RN_TEST_ID,R.RN_RUN_ID,R.RN_RUN_NAME,R.RN_STATUS,RN_TESTER_NAME
from CYCL_FOLD as CF,CYCLE as C ,RUN as R
where CF_ITEM_ID = C.CY_FOLDER_ID and C.CY_CYCLE_ID = R.RN_CYCLE_ID AND CF.CF_ITEM_PATH LIKE '''+@m+''''
exec(@sql1)
--select * from ##tmp_f_1 

--写入##tmp_f_2重复数据
insert into ##tmp_f_2
select t1.CF_ITEM_NAME,t1.CY_CYCLE,t1.RN_CYCLE_ID,t1.RN_TEST_ID,t1.RN_RUN_ID,t1.RN_RUN_NAME,t1.RN_STATUS,t1.RN_TESTER_NAME,t1.RN_number,RN_number_f_p
from ##tmp_f_1 t1, (select RN_CYCLE_ID,RN_TEST_ID from ##tmp_f_1 
group by RN_CYCLE_ID,RN_TEST_ID
having(count(RN_TEST_ID)>1)) tt 
where t1.RN_CYCLE_ID = tt.RN_CYCLE_ID and t1.RN_TEST_ID = tt.RN_TEST_ID 

--删除原始数据中重复的数据，留下不重复的数据
delete from ##tmp_f_1
where exists(select * from ##tmp_f_2 t2 where ##tmp_f_1.RN_TEST_ID = t2.RN_TEST_ID)

--插入tmp4,不重复的用例对应的step
insert into tmp4
select t1.CF_ITEM_NAME,t1.CY_CYCLE,t1.RN_TEST_ID,sp.ST_STEP_NAME,sp.ST_STATUS, sp.ST_EXECUTION_DATE,sp.ST_EXECUTION_TIME,sp.ST_DESCRIPTION ,sp.ST_EXPECTED ,t1.RN_RUN_ID
from ##tmp_f_1 t1,STEP sp
where t1.RN_RUN_ID = sp.ST_RUN_ID


insert into ##tmp_f_5
select t2.CF_ITEM_NAME,t2.CY_CYCLE,t2.RN_TEST_ID,sp.ST_STEP_NAME,sp.ST_STATUS, sp.ST_EXECUTION_DATE,sp.ST_EXECUTION_TIME,sp.ST_DESCRIPTION ,sp.ST_EXPECTED ,t2.RN_RUN_ID,SP.ST_STEP_ID,0
from ##tmp_f_2 t2,STEP sp
where t2.RN_RUN_ID = sp.ST_RUN_ID


--游标1 run_id
DECLARE aaa CURSOR for select ST_TEST_ID from ##tmp_f_5 group by ST_TEST_ID
Open aaa
fetch next from aaa into @temp_temp 
while @@fetch_status=0
begin
	--print @temp_temp
	--select ST_STEP_ID  from ##tmp_f_5 where ST_TEST_ID = @temp_temp group by ST_STEP_ID 
	--游标2 step_ID
	DECLARE bbb CURSOR for select ST_STEP_ID  from ##tmp_f_5 where ST_TEST_ID = @temp_temp group by ST_STEP_ID 
	Open bbb
	fetch next from bbb into @temp_temp2
	while @@fetch_status=0
	begin
		--update ##tmp_f_5 set ST_number_f_p = '1' where ##tmp_f_5.ST_STATUS = 'failed'
		insert into tmp4
		select top 1 [ST_MIN_TEST],[ST_TEST_PROJECT],[ST_TEST_ID],[ST_STEP_NAME],[ST_STATUS],[ST_EXECUTION_DATE],[ST_EXECUTION_TIME],[ST_DESCRIPTION],[ST_EXPECTED],[RUN_ID]
		from ##tmp_f_5 where ST_TEST_ID =@temp_temp and ST_STEP_ID = @temp_temp2 order by ST_EXECUTION_DATE DESC,ST_EXECUTION_TIME DESC
		fetch next from bbb into @temp_temp2
	end
	Close bbb    
	Deallocate bbb 
	fetch next from aaa into @temp_temp 
end
Close aaa    
Deallocate aaa 

update tmp4 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(13),'<out>')
update tmp4 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(10),'<out>')
update tmp4 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(13),'<out>')
update tmp4 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(10),'<out>')
update tmp4 set ST_STEP_NAME = REPLACE(ST_STEP_NAME,CHAR(13),'<out>')
update tmp4 set ST_STEP_NAME = REPLACE(ST_STEP_NAME,CHAR(10),'<out>')

drop table ##tmp_f_1
drop table ##tmp_f_2
drop table ##tmp_f_3
drop table ##tmp_f_5
end