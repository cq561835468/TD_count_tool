create procedure tablecreattmp_alltest
as
begin
create table tmp_alltest
(
test_id nvarchar(max),
test_name nvarchar(max),
test_step nvarchar(max),
test_des nvarchar(max),
test_exp nvarchar(max)
)
end