-- EXTENSIONS

CREATE extension IF NOT EXISTS pgcrypto;

-- DEV CLEANUP - drop all tables so we can create them again

DROP TABLE blogs;
DROP TABLE accounts;

-- Accounts table

CREATE TABLE IF NOT EXISTS accounts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password TEXT NOT NULL,
    created timestamptz NOT NULL DEFAULT NOW(),
    updated timestamptz NOT NULL DEFAULT NOW(),

    UNIQUE(username),
    UNIQUE(email)
);

INSERT INTO accounts (username, email, password) VALUES ('test', 'test@example.dk', crypt('mypassword', gen_salt('bf')));

-- Blogs Table

CREATE TABLE IF NOT EXISTS blogs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255) NOT NULL,
    body TEXT,
    
    created timestamptz NOT NULL DEFAULT NOW(),
    created_by uuid NOT NULL,
    updated timestamptz NOT NULL DEFAULT NOW()
);
ALTER TABLE blogs add constraint fk_blogs_accounts FOREIGN KEY (created_by) REFERENCES accounts (id);

INSERT INTO blogs (title, body, created_by) VALUES (
    'Test blog 1', 
    'This is some test content for the first blog post.',
    (SELECT id FROM accounts WHERE username = 'test')
);

INSERT INTO blogs (title, body, created_by) VALUES (
    'Test blog 2', 
    'This is some test content for the second blog post. yiiir!',
    (SELECT id FROM accounts WHERE username = 'test')
);

INSERT INTO blogs (title, body, created_by) VALUES (
    'Test blog 3', 
    'A third thing... could there be a fourth thing?',
    (SELECT id FROM accounts WHERE username = 'test')
);