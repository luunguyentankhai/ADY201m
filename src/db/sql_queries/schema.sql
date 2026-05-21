CREATE TABLE IF NOT EXISTS "Online_Payments_Fraud_Detection_Dataset" (
	"step" integer,
	"type" text,
	"amount" double precision,
	"nameOrig" varchar(50),
	"oldbalanceOrg" double precision,
	"newbalanceOrig" double precision,
	"nameDest" varchar(50),
	"oldbalanceDest" double precision,
	"newbalanceDest" double precision,
	"isFraud" smallint,
	"isFlaggedFraud" smallint
)


