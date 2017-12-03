use master;
go

if db_id('TVMS') is not null
begin
  drop database TVMS;
end;
go

if db_id('TVMS') is null
begin
  create database TVMS;
end;
go

use TVMS;
go

create schema lab1;
go

create table lab1.BaseSelection
(
    ID  int identity(1, 1)
  , val int
  , constraint PK_Lab1BaseSelection primary key (ID)
);

if exists(select * from lab1.BaseSelection)
begin

  truncate table lab1.BaseSelection;

end;
go

insert into lab1.BaseSelection (val)
values (38), (60), (41), (51), (33), (42), (45), (21), (53), (60)
     , (68), (52), (47), (46), (49), (49), (14), (57), (54), (59)
     , (77), (47), (28), (48), (58), (32), (42), (58), (61), (30)
     , (61), (35), (47), (72);

-- 1 Task

declare @Variant int = 14

declare @SelectionSize as int = 20 + @Variant;

declare @MaxVal as float = (select max(bs.val)
                          from lab1.BaseSelection as bs)
      , @MinVal as float = (select min(bs.val)
                          from lab1.BaseSelection as bs);

declare @VariationRange as int = @MaxVal - @MinVal;

declare @NumberOfGroups as int = floor(1 + 3.322 * log(@SelectionSize, 10));

declare @IntervalLength as float = cast(@VariationRange as float) / cast(@NumberOfGroups as float);

select @SelectionSize  as n
     , @MaxVal         as [Max]
     , @MinVal         as [Min]
     , @VariationRange as R
     , @NumberOfGroups as K
     , @IntervalLength as h

; with IntervalSelection
as
(
  select @MinVal as LeftVal, @MinVal + @IntervalLength as RightVal

  union all

  select isl.RightVal, isl.RightVal + @IntervalLength
  from IntervalSelection as isl
  where isl.RightVal + @IntervalLength <= @MaxVal
)
, NumberedIntervalSelection
as
(
  select row_number() over (order by isl.LeftVal, isl.RightVal) as LineNum
       , isl.LeftVal
       , isl.RightVal
  from IntervalSelection as isl
)
, SelectionWithIntCenterAndFrequency
as
(
  select nis.LineNum
       , nis.LeftVal
       , nis.RightVal
       , (nis.LeftVal + nis.RightVal) / 2 as IntervalCenter
       , frq.Frequency
  from NumberedIntervalSelection as nis
  cross apply (
               select count(*) as Frequency
               from lab1.BaseSelection as bs
               where (
                          bs.val >  nis.LeftVal
                      and bs.val <= nis.RightVal
                     )
                     or
                     (
                          bs.val      = @MinVal
                      and nis.LineNum = 1
                     )
              ) as frq
)
, SelectionWithRunningFreqAndRelationalFreq
as
(
  select icf.LineNum
       , icf.LeftVal
       , icf.RightVal
       , icf.IntervalCenter
       , icf.Frequency
       , sum(icf.Frequency) over (order by icf.LineNum
                                  rows between unbounded preceding
                                           and current row) as RunningFrequency
       , cast(icf.Frequency as float) / @SelectionSize as RelationalFrequency
  from SelectionWithIntCenterAndFrequency as  icf
)
, SelectionWithRunningRelationalFrequency
as
(
  select rdrf.LineNum
       , rdrf.LeftVal
       , rdrf.RightVal
       , rdrf.IntervalCenter
       , rdrf.Frequency
       , rdrf.RunningFrequency
       , rdrf.RelationalFrequency
       , sum(rdrf.RelationalFrequency) over(order by rdrf.LineNum
                                            rows between unbounded preceding
                                                     and current row) as RunningRelFreq
  from SelectionWithRunningFreqAndRelationalFreq as rdrf
)
select *
from SelectionWithRunningRelationalFrequency as r

union all

select null
     , null
     , null
     , null
     , sum(rs.Frequency)
     , null
     , sum(rs.RelationalFrequency)
     , null
from SelectionWithRunningRelationalFrequency as rs
