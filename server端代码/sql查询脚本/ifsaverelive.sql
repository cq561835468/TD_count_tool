create procedure ifsaverelive
	@save nvarchar(max)
as
begin
--declare @save nvarchar(max)
--set @save = 'ifrelivetable'
IF EXISTS (select schema_id from sys.objects where name = @save)
	select name from sys.objects where name = @save
ELSE
	select name from sys.objects where name = @save
end