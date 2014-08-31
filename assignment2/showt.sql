show tables;


SELECT count(*) FROM (
  SELECT * from frequency where docid='10398_txt_earn'
) x;

SELECT count(*) FROM (
  SELECT term from frequency where docid='10398_txt_earn' and count=1
) x;

SELECT count(*) FROM (
  SELECT term from frequency where docid='10398_txt_earn' and count=1 union SELECT term from frequency where docid='925_txt_trade' and count=1
) x;

SELECT distinct count(*) FROM (
  SELECT docid from frequency group by term having Sum(frequency.count) > 300
) x;

#Como hacer esto con un join??
SELECT distinct count(*) FROM (
  select * from (SELECT docid from frequency where term='transactions' or term='world') group by docid having Count(docid) = 2
) x;

a = SELECT docid from frequency where term='transactions';
b = SELECT docid from frequency where term='world';
SELECT distinct count(*) FROM (
     SELECT docid
     FROM 
     INNER JOIN 
     ON frequency.docid
) x;

#Matrix multiply
select row_num, col_num, sum(product) from(
    select a.row_num, b.col_num, a.value * b.value as product from a
    inner join b
    on a.col_num=b.row_num
)
group by row_num, col_num;

#Similarity Matrix
select * from (
select id1, id2, sum(product) as sim from(
    select frequency.docid as id1, freq.docid as id2, frequency.count * freq.count as product from frequency
    inner join frequency as freq
    on frequency.term=freq.term
)
group by id1, id2
)
where id1='10080_txt_crude' and id2='17035_txt_earn';

#Create View
CREATE VIEW query AS 
SELECT 'q' as docid, 'washington' as term, 1 as count 
UNION
SELECT 'q' as docid, 'taxes' as term, 1 as count
UNION 
SELECT 'q' as docid, 'treasury' as term, 1 as count
UNION 
SELECT * FROM frequency;

select max(sim) from (
select id1, id2, sum(product) as sim from(
    select query.docid as id1, freq.docid as id2, query.count * freq.count as product from query
    inner join frequency as freq
    on query.term=freq.term
)
group by id1, id2
)
where id1='q';



