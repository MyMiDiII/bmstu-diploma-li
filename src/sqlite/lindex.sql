.load ./lindex
create virtual table virtmaps using lindex(1, fcnn2-pt);
select * from virtmaps where key = 3465205493;
select * from virtmaps where key > 3465205493;
select * from virtmaps where key < 3465205493;
select * from virtmaps where key <= 3465205493;
select * from virtmaps where key >= 3465205493;
select * from virtmaps where key between 3465205493 and 5694768947 ;
insert into virtmaps values(1);
select * from virtmaps where key = 1;
