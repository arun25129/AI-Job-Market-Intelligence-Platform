CREATE TABLE jobs (
    job_id SERIAL PRIMARY KEY,
    job_title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    salary VARCHAR(100),
    experience VARCHAR(100),
    skills TEXT,
    job_description TEXT,
    posted_date DATE,
    source VARCHAR(100),
    job_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);