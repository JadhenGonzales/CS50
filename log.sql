-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Checking Crime Scene Reports that took place on the time and place of crime
SELECT *
  FROM crime_scene_reports
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND street = "Humphrey Street";
-- 10:15 AM at bakery, 3 witnesses interviewed, bakery mentioned,


--check interviews that mention the bakery on the day of crime
SELECT name, transcript
  FROM interviews
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND transcript LIKE "%bakery%";
-- Within 10min, car left from the parking lot (ruth)
-- Thief withdrawed money from ATM in Legett Street (eugene)
-- Called someone for less than a min, planned to take earliest flight the next morning (7/29), accomplice purchased tickets (raymond)


-- Check every car that exited parking lot within timeframe and owner details
SELECT hour, minute, bsl.license_plate, name, p.id, phone_number, passport_number
  FROM bakery_security_logs AS bsl
  JOIN people AS p
    ON bsl.license_plate = p.license_plate
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND hour = 10
   AND activity = "exit"
   AND minute BETWEEN 15 AND 25;
-- 8 suspects


-- Check atm transactions on day of crime together with name of account holder
SELECT name, atm.account_number, amount
  FROM atm_transactions AS atm
  JOIN bank_accounts AS ba
    ON atm.account_number = ba.account_number
  JOIN people AS p
    ON ba.person_id = p.id
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND atm_location = "Leggett Street"
   AND transaction_type = "withdraw"
   AND p.id IN (
       SELECT id
         FROM people
        WHERE license_plate IN (
              SELECT license_plate
                FROM bakery_security_logs
               WHERE year = 2021
                 AND month = 7
                 AND day = 28
                 AND hour = 10
                 AND activity = "exit"
                 AND minute BETWEEN 15 AND 25));
-- 4 suspects, Bruce, Diana, Iman, Luca


-- Check phone calls
SELECT name, receiver
  FROM people AS p
  JOIN phone_calls AS pc
    ON p.phone_number = pc.caller
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND duration BETWEEN 0 AND 60;
-- Bruce or Diana


-- Check receiver
SELECT name, phone_number
  FROM people
 WHERE phone_number IN ("(375) 555-8161","(725) 555-3243");
-- Robin or Philip


-- Check flight passengers
SELECT name, passport_number
FROM people
WHERE passport_number IN (
      SELECT passport_number
        FROM passengers
       WHERE flight_id = (
                SELECT id
                  FROM flights
                 WHERE year = 2021
                   AND month = 7
                   AND day = 29
                   AND origin_airport_id = 8
              ORDER BY hour ASC, minute ASC
                 LIMIT 1));
-- Thief is Bruce, Robin is Accomplice

-- Check destination
  SELECT city
    FROM flights
    JOIN airports
      ON flights.destination_airport_id = airports.id
   WHERE year = 2021
     AND month = 7
     AND day = 29
     AND origin_airport_id = 8
ORDER BY hour ASC, minute ASC
         LIMIT 1;