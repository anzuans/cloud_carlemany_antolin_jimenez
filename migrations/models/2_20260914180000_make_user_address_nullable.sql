-- upgrade --
ALTER TABLE "userdb" ALTER COLUMN "address" DROP NOT NULL;

-- downgrade --
ALTER TABLE "userdb" ALTER COLUMN "address" SET NOT NULL;
