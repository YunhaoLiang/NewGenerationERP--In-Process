CREATE OR REPLACE VIEW vw_account_balance AS
SELECT 
    fa.account_id,
    fa.account_name,
    fa.account_type,
    fa.balance as current_balance,
    COALESCE(SUM(CASE 
        WHEN t.transaction_type = 'income' THEN t.amount
        WHEN t.transaction_type = 'expense' THEN -t.amount
        WHEN t.transaction_type = 'transfer' THEN t.amount
    END), 0) as transaction_total,
    fa.balance + COALESCE(SUM(CASE 
        WHEN t.transaction_type = 'income' THEN t.amount
        WHEN t.transaction_type = 'expense' THEN -t.amount
        WHEN t.transaction_type = 'transfer' THEN t.amount
    END), 0) as actual_balance,
    fa.currency,
    fa.updated_at as last_updated
FROM 
    financial_accounts fa
LEFT JOIN 
    transactions t ON fa.account_id = t.account_id
GROUP BY 
    fa.account_id, fa.account_name, fa.account_type, fa.balance, fa.currency, fa.updated_at; 