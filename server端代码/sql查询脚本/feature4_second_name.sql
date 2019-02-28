create procedure feature4_second_name
	@tablebase varchar(max),
	@name varchar(max) 
as
begin
declare @temp_temp varchar(max) 
declare @sql1 varchar(max) 
declare @sql2 varchar(max) 
--declare @name varchar(max) 
--declare @tablebase varchar(max) 
--set @tablebase = '[kdm39_2800v1r4_db]'
--set @name = 'temp'
create table ##tmp1
(
AL_ITEM_ID varchar(max),
AL_FATHER_ID varchar(max),
AL_DESCRIPTION varchar(max),
AL_ABSOLUTE_PATH  varchar(max),
)

set @sql1 = 'DECLARE aaa CURSOR for select AL_ABSOLUTE_PATH FROM '+@tablebase+'.[dbo].[ALL_LISTS] where AL_DESCRIPTION = '''+@name+''''
exec(@sql1)
Open aaa
fetch next from aaa into @temp_temp 
while @@fetch_status=0
begin
	print @temp_temp 
	set @temp_temp = @temp_temp + '%'
	set @sql2 = 'insert into ##tmp1 SELECT [AL_ITEM_ID],[AL_FATHER_ID],[AL_DESCRIPTION],[AL_ABSOLUTE_PATH] FROM '+@tablebase+'.[dbo].[ALL_LISTS] where AL_ABSOLUTE_PATH like '''+@temp_temp+''''
	exec(@sql2)
	fetch next from aaa into @temp_temp 
end 


Close aaa    
Deallocate aaa 
select AL_DESCRIPTION from ##tmp1
drop table ##tmp1

end