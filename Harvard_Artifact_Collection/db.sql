use Harvards_Artifacts_Collection;

select * from artifact_colors;
select * from artifact_media;
select * from artifact_metadata;

#artifact_metadata

select * from artifact_metadata where century = '11th century' and culture = 'Byzantine';
select distinct culture from artifact_metadata;
select * from artifact_metadata where period = 'Archaic Period';
select title,accessionyear from artifact_metadata order by accessionyear desc;
select department, count(*) as artifact_count from artifact_metadata group by department;

#artifact_media

select * from artifact_media where imagecount > 1;
SELECT AVG(`rank`) AS average_rank FROM artifact_media WHERE `rank` IS NOT NULL;
select * from artifact_media where mediacount < colorcount;
select * from artifact_media where datebegin between 1500 and 1600;
select * from artifact_media where mediacount = 0;

#artifact_colors

select distinct hue from artifact_colors;
SELECT color, COUNT(*) AS frequency FROM artifact_colors WHERE color IS NOT NULL GROUP BY color ORDER BY frequency DESC LIMIT 5;
select hue,avg(percent) as average_percentage from artifact_colors where hue is not NULL and percent is not NULL group by hue order by average_percentage desc;
select distinct color from artifact_colors where objectid = 195623;
select COUNT(*) as color_count from artifact_colors where color is not NULL;

# Join based Queries 

select m.title, c.hue, m.culture from artifact_metadata m join artifact_colors c on m.id = c.objectid where m.culture = 'Byzantine';
select m.title, c.hue from artifact_metadata m join artifact_colors c on m.id = c.objectid;
select m.title, m.culture, md.`rank` from artifact_metadata m join artifact_media md on m.id = md.objectid where m.period is not NULL;
select m.title from artifact_metadata m join artifact_colors c on m.id = c.objectid join artifact_media md on m.id = md.objectid where c.hue = 'Grey' order by md.`rank` desc LIMIT 10;
select m.classification, COUNT(DISTINCT m.id) as artifact_per_classification, avg(md.mediacount) as average_media_count from artifact_metadata m  join artifact_media md on m.id = md.objectid group by m.classification;

#customized Queries

#List artifact titles with their total number of media files.
select m.title, count(md.mediacount) as number_of_media_files from artifact_metadata m  join artifact_media md on m.id = md.objectid group by m.title order by number_of_media_files desc;
#Show artifact titles, hues, and media counts for artifacts from the “British period” period.
select m.title, c.hue, md.mediacount from artifact_metadata m join artifact_colors c on m.id = c.objectid join artifact_media md on m.id = md.objectid where m.period = 'British period';
#Find all artifacts with the hue “Blue” and their corresponding rank.
SELECT m.title, md.`rank`, c.hue FROM artifact_metadata m JOIN artifact_colors c ON m.id = c.objectid JOIN artifact_media md ON m.id = md.objectid WHERE c.hue = 'Blue';
#List each artifact title with its culture and the number of associated colors.
select m.title, m.culture, COUNT(c.color) as color_count from artifact_metadata m join artifact_colors c on m.id = c.objectid group by m.title, m.culture order by color_count desc;
#Get the average rank of artifacts per culture.
select m.culture,avg(md.`rank`) as average_rank_per_culture from artifact_metadata m join artifact_media md on m.id = md.objectid group by m.culture order by average_rank_per_culture desc;
#List artifact titles along with all their hues and media counts, ordered by rank descending.
select m.title, c.hue, md.mediacount from artifact_metadata m join artifact_colors c on m.id = c.objectid join artifact_media md on m.id = md.objectid order by md.`rank`desc;
#Find artifacts where the number of colors used exceeds the number of media files.
select m.title, count(c.color) as number_of_color, md.mediacount from artifact_metadata m join artifact_colors c on m.id = c.objectid join artifact_media md on m.id = md.objectid group by m.title,md.mediacount having number_of_color > md.mediacount order by number_of_color desc;
#Show the top 5 artifacts with the most colors used, along with their titles and cultures.
select m.title, m.culture, count(c.color) as number_of_color from artifact_metadata m join artifact_colors c on m.id = c.objectid  group by m.title,m.culture order by number_of_color desc limit 5;
#List artifact titles, cultures, and hues for artifacts acquired after 1800.
select m.title, m.culture, c.hue, m.accessionyear from artifact_metadata m join artifact_colors c on m.id = c.objectid where m.accessionyear > 1800 order by m.accessionyear asc;
#Find all artifacts that share the same hue and list their titles and cultures.
SELECT m.title, m.culture, c.hue FROM artifact_metadata m JOIN artifact_colors c ON m.id = c.objectid WHERE c.hue IN (SELECT hue FROM artifact_colors GROUP BY hue HAVING COUNT(DISTINCT objectid) > 1)ORDER BY c.hue, m.title;

