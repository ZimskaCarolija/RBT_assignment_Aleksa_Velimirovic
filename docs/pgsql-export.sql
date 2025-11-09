CREATE TABLE "users"(
    "id" INTEGER NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "password" VARCHAR(255) NOT NULL,
    "full_name" VARCHAR(255) NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "deleted_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "role_id" INTEGER NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
CREATE TABLE "roles"(
    "id" SMALLINT NOT NULL,
    "name" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "roles" ADD PRIMARY KEY("id");
CREATE TABLE "vacation_entitlements"(
    "id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "year" SMALLINT NOT NULL,
    "total_days" SMALLINT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "deleted_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NULL
);
ALTER TABLE
    "vacation_entitlements" ADD PRIMARY KEY("id");
CREATE TABLE "vacation_records"(
    "id" INTEGER NOT NULL,
    "user_id" INTEGER NOT NULL,
    "start_date" DATE NOT NULL,
    "end_date" DATE NOT NULL,
    "days_count" SMALLINT NOT NULL,
    "year" SMALLINT NOT NULL,
    "note" TEXT NULL
);
ALTER TABLE
    "vacation_records" ADD PRIMARY KEY("id");
ALTER TABLE
    "vacation_records" ADD CONSTRAINT "vacation_records_start_date_foreign" FOREIGN KEY("start_date") REFERENCES "users"("id");
ALTER TABLE
    "vacation_entitlements" ADD CONSTRAINT "vacation_entitlements_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_role_id_foreign" FOREIGN KEY("role_id") REFERENCES "roles"("id");

INSERT INTO "roles" ("id", "name") VALUES
(1, 'Admin'),
(2, 'Employee')
ON CONFLICT ("id") DO NOTHING;

INSERT INTO "users" ("id", "email", "password", "full_name", "role_id", "created_at") VALUES
(1, 'velimirovicaleksa001@gmail.com', 'scrypt:32768:8:1$cMHwVoMWyyxnFDFn$d276e6debbdbca1bc014c41d04b1307b2453431e36e7f1cc91ad90c5d3156690e8d351641e67dfc4b8140d548a30c66facc3eb2bb08564f5ce9e00e5cb7d17e2', 'Aleksa Velimirovic', 1, NOW())
ON CONFLICT ("id") DO NOTHING;