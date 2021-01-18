-- *****************************************************************
-- Part 1
-- *****************************************************************

-- Initial query to identify card holders and number of cards - 53 records
SELECT *
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id;

-- Group by card holder and count number of cards
-- Inner join, only care about union of card_holder and credit_card
SELECT card_holder.name, COUNT(credit_card.card) AS "Card Count"
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
GROUP BY card_holder.name
ORDER BY "Card Count" DESC

-- Bring in transaction data - no grouping yet, sanity check data and join logic - 3500 records
SELECT card_holder.card_holder_id, card_holder.name, credit_card.card, t.date, t.amount, t.card
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
ORDER BY card_holder.name, t.date

-- See full dataset with filter applied (no groups yet), looks good
SELECT card_holder.card_holder_id, card_holder.name, credit_card.card, t.date, t.amount, t.card
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE t.amount < 2.00
ORDER BY card_holder.name, t.date

-- How can you isolate (or group) the transactions of each cardholder?
-- Count the transactions that are less than $2.00 per cardholder.

-- Group by card holder and count filtered transactions
SELECT card_holder.card_holder_id, card_holder.name, COUNT(credit_card.card) AS "Transaction count under $2.00"
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE t.amount < 2.00
GROUP BY card_holder.card_holder_id, card_holder.name
ORDER BY "Transaction count under $2.00" DESC, card_holder.name

-- Is there any evidence to suggest that a credit card has been hacked? Explain your rationale.
-- ANSWER - if the following is true
-- Some fraudsters hack a credit card by making several small transactions (generally less than $2.00), which are typically ignored by cardholders.
-- then we can clearly see some individuals who raise suspician with an unusual amount of transactions under 2.00

-- What are the top 100 highest transactions made between 7:00 am and 9:00 am?
-- Ensure date parsing and filtering correct
SELECT card_holder.name, credit_card.card, t.date, EXTRACT(HOUR FROM date) AS "date_hour", t.amount
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE EXTRACT(HOUR FROM date) >= 7 AND EXTRACT(HOUR FROM date) < 9
ORDER BY card_holder.name, credit_card.card, t.date

-- Order by transaction amt and select top 100
SELECT card_holder.name, credit_card.card, t.date, EXTRACT(HOUR FROM date) AS "date_hour", t.amount
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE EXTRACT(HOUR FROM date) >= 7 AND EXTRACT(HOUR FROM date) < 9
ORDER BY t.amount DESC, card_holder.name
LIMIT 100

-- Create table view
CREATE VIEW top_100_between_7_and_9 AS
SELECT card_holder.name, credit_card.card, t.date, EXTRACT(HOUR FROM date) AS "date_hour", t.amount
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE EXTRACT(HOUR FROM date) >= 7 AND EXTRACT(HOUR FROM date) < 9
ORDER BY t.amount DESC, card_holder.name
LIMIT 100

-- Drill down on person of suspicion
SELECT card_holder.name, credit_card.card, t.date, EXTRACT(HOUR FROM date) AS "date_hour", t.amount
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE card_holder.name = 'Robert Johnson'
ORDER BY t.amount DESC, card_holder.name

-- Is there a higher number of fraudulent transactions made during this time frame versus the rest of the day?
-- All transactions, 3500 rows total

-- Transactions under $2 - 350 rows
SELECT card_holder.name, credit_card.card, t.date, EXTRACT(HOUR FROM date) AS "date_hour", t.amount
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE amount < 2.00
ORDER BY card_holder.name, credit_card.card, t.date

-- Transactions under $2 between 7 and 9 - 30 rows
SELECT card_holder.name, credit_card.card, t.date, EXTRACT(HOUR FROM date) AS "date_hour", t.amount
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE amount < 2.00 AND EXTRACT(HOUR FROM date) >= 7 AND EXTRACT(HOUR FROM date) < 9
ORDER BY card_holder.name, credit_card.card, t.date

-- Transactions under $2 outside 7 and 9 - 320 rows
SELECT card_holder.name, credit_card.card, t.date, EXTRACT(HOUR FROM date) AS "date_hour", t.amount
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE amount < 2.00 AND (EXTRACT(HOUR FROM date) < 7 OR EXTRACT(HOUR FROM date) >= 9)
ORDER BY card_holder.name, credit_card.card, t.date

-- Pull in merchant data - 350 rows
SELECT card_holder.name, credit_card.card, t.date, EXTRACT(HOUR FROM date) AS "date_hour", t.amount, m.merchant_name
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
LEFT JOIN merchant as m ON t.merchant_id = m.merchant_id
WHERE amount < 2.00
ORDER BY m.merchant_name, t.date, date_hour

-- group by merchant - count the hacks between 7 and 9 (count records)
SELECT  m.merchant_name, SUM(t.amount) AS "tot_amt", COUNT(date)
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
LEFT JOIN merchant as m ON t.merchant_id = m.merchant_id
WHERE amount < 2.00
GROUP BY m.merchant_name
ORDER BY COUNT(date) DESC

-- Instead of starting with card_holder, lets start with transactions and confirm same result counts - all good
-- Results: 350 total, 30 within 7-9 window, 320 outside window
SELECT 
	t.transaction_id, t.date, 
	EXTRACT(HOUR FROM date) AS "date_hour", 
	(EXTRACT(HOUR FROM date) >= 7 AND EXTRACT(HOUR FROM date) < 9) AS "7_to_9",
	(EXTRACT(HOUR FROM date) < 7 OR EXTRACT(HOUR FROM date) >= 9) AS "outside_window",
	t.amount, t.card, ch.name, m.merchant_name	
FROM transaction as t
INNER JOIN credit_card as c ON c.card = t.card
INNER JOIN card_holder as ch ON ch.card_holder_id = c.card_holder_id
LEFT JOIN merchant as m ON t.merchant_id = m.merchant_id
WHERE amount < 2.00
ORDER BY "7_to_9" DESC, m.merchant_name

-- Group and sort by merchant
SELECT 
	m.merchant_name, 
	COUNT(transaction_id) AS "transaction_count", 
	SUM(t.amount) AS "transaction_total"
FROM transaction as t
INNER JOIN credit_card as c ON c.card = t.card
INNER JOIN card_holder as ch ON ch.card_holder_id = c.card_holder_id
LEFT JOIN merchant as m ON t.merchant_id = m.merchant_id
WHERE amount < 2.00
GROUP BY m.merchant_name
ORDER BY "transaction_count" DESC, "transaction_total" DESC
LIMIT 5

-- Create view for top_5_merchants
CREATE VIEW top_5_merchants AS
SELECT 
	m.merchant_name, 
	COUNT(transaction_id) AS "transaction_count", 
	SUM(t.amount) AS "transaction_total"
FROM transaction as t
INNER JOIN credit_card as c ON c.card = t.card
INNER JOIN card_holder as ch ON ch.card_holder_id = c.card_holder_id
LEFT JOIN merchant as m ON t.merchant_id = m.merchant_id
WHERE amount < 2.00
GROUP BY m.merchant_name
ORDER BY "transaction_count" DESC, "transaction_total" DESC
LIMIT 5

-- Query table view: top_100_between_7_and_9
SELECT * FROM top_100_between_7_and_9

-- Query table view: top_5_merchants
SELECT * FROM top_5_merchants

-- *****************************************************************
-- Part 2
-- *****************************************************************

-- Query card_holders 2 and 18
SELECT card_holder.card_holder_id, t.date, EXTRACT(HOUR FROM date) AS "hour", t.amount
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE (card_holder.card_holder_id = 18 OR card_holder.card_holder_id = 2)
ORDER BY t.date

-- Query card_holder 25 from jan to jun 2018
-- 124 records total (excluding date filter)
-- 68 records with date filter
SELECT  
	t.date, 
	EXTRACT(MONTH FROM date) AS "month", 
	EXTRACT(DAY FROM date) AS "day", 
	EXTRACT(YEAR FROM date) AS "year", 
	t.amount
FROM card_holder
INNER JOIN credit_card ON card_holder.card_holder_id = credit_card.card_holder_id
INNER JOIN transaction as t ON credit_card.card = t.card
WHERE 
	card_holder.card_holder_id = 25 AND
	EXTRACT(YEAR FROM date) = 2018 AND
	EXTRACT(MONTH FROM date) >= 1 AND
	EXTRACT(MONTH FROM date) <= 6
ORDER BY t.date




