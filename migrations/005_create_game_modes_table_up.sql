CREATE TABLE "game_modes" (
  "id" SERIAL PRIMARY KEY,
  "name" varchar NOT NULL,
  "description" varchar,
  "created_at" timestamp NOT NULL,
  "updated_at" timestamp NOT NULL default current_timestamp
);