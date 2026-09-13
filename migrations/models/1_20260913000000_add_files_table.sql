-- upgrade --
CREATE TABLE IF NOT EXISTS "filedb" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(255) NOT NULL,
    "description" VARCHAR(500),
    "content_path" VARCHAR(500),
    "original_filename" VARCHAR(255),
    "user_id" INT NOT NULL
);

-- downgrade --
DROP TABLE IF EXISTS "filedb";