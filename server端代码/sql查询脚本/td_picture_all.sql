create procedure td_picture_all
@m nvarchar(max)
as
begin
DECLARE @sql1 nvarchar(2000)
DECLARE @sql2 nvarchar(2000)
DECLARE @sql3 nvarchar(2000)
--DECLARE @m nvarchar(max)
DECLARE @temp_temp nvarchar(2000)
DECLARE @replace_one nvarchar(2000)
DECLARE @replace_two nvarchar(2000)
DECLARE @replace_three nvarchar(2000)
DECLARE @replace_four nvarchar(2000)
DECLARE @replace_five nvarchar(2000)
DECLARE @replace_sex nvarchar(2000)

-------##tmp1原始数据
create table ##tmp111
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

--------#tmp41数据筛选
create table ##tmp411
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
--set @m = 'AAAAA%'
--写入原始数据

set @sql1 = 
'insert into ##tmp111(CF_ITEM_NAME,CY_CYCLE,RN_CYCLE_ID,RN_TEST_ID,RN_RUN_ID,RN_RUN_NAME,RN_STATUS,RN_TESTER_NAME)
select CF.CF_ITEM_NAME,C.CY_CYCLE,R.RN_CYCLE_ID,R.RN_TEST_ID,R.RN_RUN_ID,R.RN_RUN_NAME,R.RN_STATUS,RN_TESTER_NAME
from CYCL_FOLD as CF,CYCLE as C ,RUN as R
where CF_ITEM_ID = C.CY_FOLDER_ID and C.CY_CYCLE_ID = R.RN_CYCLE_ID AND CF.CF_ITEM_PATH LIKE '''+@m+''''
exec(@sql1)

--插入表头
insert into tmp4 values('测试项 ','测试点 ','000','测试步骤','status','用例执行日期','用例执行时间','用例执行步骤','用例执行结果','000')
--插入表tmp4
insert into tmp4
select t3.CF_ITEM_NAME,t3.CY_CYCLE,t3.RN_TEST_ID,sp.ST_STEP_NAME,sp.ST_STATUS, sp.ST_EXECUTION_DATE,sp.ST_EXECUTION_TIME,sp.ST_DESCRIPTION ,sp.ST_EXPECTED ,t3.RN_RUN_ID
from ##tmp111 t3,STEP sp
where t3.RN_RUN_ID = sp.ST_RUN_ID

set @replace_one = 'update dbo.tmp4 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(13),'''+'<out>'+''')'
set @replace_two = 'update dbo.tmp4 set ST_DESCRIPTION = REPLACE(ST_DESCRIPTION,CHAR(10),'''+'<out>'+''')'
set @replace_three = 'update dbo.tmp4 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(13),'''+'<out>'+''')'
set @replace_four = 'update dbo.tmp4 set ST_EXPECTED = REPLACE(ST_EXPECTED,CHAR(10),'''+'<out>'+''')'
set @replace_five = 'update dbo.tmp4 set ST_STEP_NAME = REPLACE(ST_STEP_NAME,CHAR(13),'''+'<out>'+''')'
set @replace_sex = 'update dbo.tmp4 set ST_STEP_NAME = REPLACE(ST_STEP_NAME,CHAR(10),'''+'<out>'+''')'
exec(@replace_one)
exec(@replace_two)
exec(@replace_three)
exec(@replace_four)
exec(@replace_five)
exec(@replace_sex)

--select * from ##tmp111
--select * from tmp4

drop table ##tmp111
drop table ##tmp411
end