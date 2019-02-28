create procedure tablecreattmp6
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
ST_STEP_NAME varchar(2000),
ST_STATUS varchar(2000),
ST_EXECUTION_DATE varchar(2000),
ST_EXECUTION_TIME varchar(2000)
)'
exec(@tablename)
-------------------------------------
end