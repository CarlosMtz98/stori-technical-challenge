INSERT INTO transaction(datetime, amount, type, idempotency_id)
SELECT
    NOW() - (random() * interval '1 year') as datetime,
    random() * 10000 as amount,
    CASE
        WHEN random() < 0.5 THEN 'DEBIT'
        ELSE 'CREDIT'
    END as type,
    gen_random_uuid() as idempotencyId
FROM generate_series(1, 100);

INSERT INTO recipient(email, first_name, last_name) VALUES
('cmtz.rdz.98@gmail.com', 'Carlos', 'Martínez')