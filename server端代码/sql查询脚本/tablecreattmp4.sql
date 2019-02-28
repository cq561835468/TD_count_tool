create procedure tablecreattmp4
	@data nvarchar(max),
	@tmp nvarchar(max)
as
begin
declare @udata nvarchar(max)
declare @tablename nvarchar(max)


--set @data = 'ts_truelink_v2r6_db'
--set @tmp = 'tmp5'
set @udata = @data +'.' + 'dbo.'+ @tmp
---------------------------------------
if object_id(@udata,N'U') is not null	
	print 'existence'
else
----------------------------------
set @tablename = 'create table '+@tmp+'
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
)'
exec(@tablename)
-------------------------------------
end