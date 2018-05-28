# Systems with small planets
select s.radius as sun_radius, p.radius as planet_radius
from Star as s, Planet as p
where s.kepler_id = p.kepler_id
and s.radius/p.radius > 1
order by sun_radius DESC;

# How many planets for big stars
select s.radius, COUNT(p.koi_name)
from Star as s
join Planet as p using (kepler_id)
group by s.radius, s.kepler_id
having COUNT(p.koi_name) > 1 and s.radius > 1
order by s.radius desc;

# Lonely stars
select s.kepler_id, s.t_eff, s.radius
from Star s
left outer join Planet p using(kepler_id)
where p.koi_name is null
order by t_eff desc;

# Subquery joint stars and planets
select ROUND(AVG(p.t_eq), 1), MIN(s.t_eff), MAX(s.t_eff)
from Star s, Planet p
where s.kepler_id = p.kepler_id
and s.t_eff > (
  select AVG(s.t_eff)
  from Star s
);

# Find the radii of those planets in the Planet table which orbit the five largest stars in the Star table.
select p.koi_name, p.radius, s.radius
from Planet p
inner join Star s
on s.kepler_id = p.kepler_id
and s.kepler_id in (
  select kepler_id
  from Star
  order by radius desc
  limit 5)
order by p.koi_name asc;

