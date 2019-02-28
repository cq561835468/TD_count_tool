create procedure ifrelivetable
	@tablename nvarchar(max),
	@data nvarchar(max)
as
begin
declare @if nvarchar(max)
--set @tablename = 'tmp4'
--set @data = 'nvr_nvr_v11_db'
set @if = @data + '.dbo.'+@tablename
IF EXISTS (SELECT  * FROM dbo.SysObjects WHERE ID = object_id(@if) AND OBJECTPROPERTY(ID, 'IsTable') = 1)
	SELECT  name FROM dbo.SysObjects WHERE ID = object_id(@if)
ELSE
	SELECT  name FROM dbo.SysObjects WHERE ID = object_id(@if)
end