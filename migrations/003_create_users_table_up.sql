CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "uid" varchar NOT NULL,
  "nickname" varchar NOT NULL,
  "avatar_type" varchar,
  "avatar_current_id" varchar,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NOT NULL default current_timestamp,
  "last_access" timestamp
);