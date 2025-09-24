SELECT * FROM sakila.customer;
select * from customer where store_id=2
SELECT c.customer_id,
       c.first_name,
       c.last_name,
       COUNT(r.rental_id) AS total_rentals
FROM sakila.customer c
JOIN sakila.rental r ON c.customer_id = r.customer_id
GROUP BY c.customer_id, c.first_name, c.last_name
ORDER BY total_rentals DESC;

