create procedure tdrepeart_fail
@m nvarchar(max)
as
begin
DECLARE @sql1 nvarchar(2000)
DECLARE @sql2 nvarchar(2000)
DECLARE @sql3 nvarchar(2000)
--DECLARE @ca nvarchar(2000)
DECLARE @temp_temp nvarchar(2000)

-------##tmp1原始数据
create table ##tmp11
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
--------#tmp21重复数据
create table ##tmp21
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

--------#tmp31不重复数据
create table ##tmp31
(
CF_ITEM_NAME varchar(2000),
CY_CYCLE varchar(2000),
RN_CYCLE_ID int,
RN_TEST_ID  varchar(2000),
RN_RUN_ID  varchar(2000),
RN_RUN_NAME varchar(2000),
RN_STATUS varchar(2000),
RN_TESTER_NAME varchar(2000),
)

--------#tmp41重复数据筛选1
create table ##tmp41
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

set nocount on 
--自定义数据
--Truncate table tmp4
--set @ca = 'AAAAA%'
--写入原始数据



set @sql1 = 
'insert into ##tmp11(CF_ITEM_NAME,CY_CYCLE,RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_STATUS,RN_TESTER_NAME)
select CF.CF_ITEM_NAME,C.CY_CYCLE,R.RN_CYCLE_ID,R.RN_TEST_ID,R.RN_RUN_ID,R.RN_RUN_NAME,R.RN_STATUS,RN_TESTER_NAME
from CYCL_FOLD as CF,CYCLE as C ,RUN as R
where CF_ITEM_ID = C.CY_FOLDER_ID and C.CY_CYCLE_ID = R.RN_CYCLE_ID AND CF.CF_ITEM_PATH LIKE '''+@m+''''
exec(@sql1)

--写入重复数据
set @sql2 = 'insert into ##tmp21
select t1.CF_ITEM_NAME,t1.CY_CYCLE,t1.RN_CYCLE_ID,t1.RN_TEST_ID,t1.RN_RUN_ID,t1.RN_RUN_NAME,t1.RN_STATUS,t1.RN_TESTER_NAME,t1.RN_number,RN_number_f_p
from ##tmp11 t1, (select RN_CYCLE_ID,RN_TEST_ID from ##tmp11 
group by RN_CYCLE_ID,RN_TEST_ID
having(count(RN_TEST_ID)>1)) tt 
where t1.RN_CYCLE_ID = tt.RN_CYCLE_ID and t1.RN_TEST_ID = tt.RN_TEST_ID '
exec(@sql2)
--order by RN_RUN_ID
--重复数据贴上标签
DECLARE aaa CURSOR for select RN_RUN_ID FROM ##tmp21
Open aaa
fetch next from aaa into @temp_temp 
while @@fetch_status=0
begin
	update ##tmp11 set RN_number = '2' where ##tmp11.RN_RUN_ID = @temp_temp
	update ##tmp21 set RN_number_f_p = '1' where ##tmp21.RN_STATUS = 'Failed'
	update ##tmp21 set RN_number_f_p = '0' where ##tmp21.RN_STATUS != 'Failed'
	fetch next from aaa into @temp_temp 
end
Close aaa    
Deallocate aaa 

--插入#tmp41 优先级failed过滤的数据
insert into ##tmp41
select * 
from
(select * from ##tmp21 t2 
where not exists
(select * from ##tmp21 where t2.RN_CYCLE_ID=RN_CYCLE_ID and t2.RN_TEST_ID = RN_TEST_ID and t2.RN_number_f_p < RN_number_f_p )) o

--过滤2完成的插入##tmp31
insert into ##tmp31
select CF_ITEM_NAME,CY_CYCLE,RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_STATUS,RN_TESTER_NAME
from ##tmp41 t4 where not exists
(select * from ##tmp41 where t4.RN_CYCLE_ID=RN_CYCLE_ID and t4.RN_TEST_ID = RN_TEST_ID and t4.RN_RUN_NAME < RN_RUN_NAME) order by RN_CYCLE_ID desc 

--不重复标签插入##tmp31
insert into ##tmp31
select CF_ITEM_NAME,CY_CYCLE,RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_STATUS,RN_TESTER_NAME 
from ##tmp11 where RN_number = 0 order by RN_CYCLE_ID desc 

--插入表头
insert into tmp4 values('测试项 ','测试点 ','000','测试步骤','status','用例执行日期','用例执行时间','用例执行步骤','用例执行结果','000')
--插入表tmp4
insert into tmp4
select t3.CF_ITEM_NAME,t3.CY_CYCLE,t3.RN_TEST_ID,sp.ST_STEP_NAME,sp.ST_STATUS, sp.ST_EXECUTION_DATE,sp.ST_EXECUTION_TIME,sp.ST_DESCRIPTION ,sp.ST_EXPECTED ,t3.RN_RUN_ID
from ##tmp31 t3,STEP sp
where t3.RN_RUN_ID = sp.ST_RUN_ID

update tmp4 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(13),'<out>')
update tmp4 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(10),'<out>')
update tmp4 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(13),'<out>')
update tmp4 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(10),'<out>')
update tmp4 set ST_STEP_NAME = REPLACE(ST_STEP_NAME,CHAR(13),'<out>')
update tmp4 set ST_STEP_NAME = REPLACE(ST_STEP_NAME,CHAR(10),'<out>')

--select * from tmp4

drop table ##tmp11
drop table ##tmp21
drop table ##tmp31
drop table ##tmp41
end