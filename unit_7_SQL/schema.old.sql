CREATE TABLE "card_holder" (
    "card_holder_id" INT   NOT NULL,
    "name" VARCHAR(255)   NOT NULL,
    CONSTRAINT "pk_card_holder" PRIMARY KEY (
        "card_holder_id"
     )
);

CREATE TABLE "credit_card" (
    "card" VARCHAR(20)   NOT NULL,
    "card_holder_id" INT   NOT NULL
);

CREATE TABLE "merchant_category" (
    "merchant_category_id" INT   NOT NULL,
    "category_name" VARCHAR(255)   NOT NULL,
    CONSTRAINT "pk_merchant_category" PRIMARY KEY (
        "merchant_category_id"
     )
);

CREATE TABLE "merchant" (
    "merchant_id" INT   NOT NULL,
    "merchant_name" VARCHAR(255)   NOT NULL,
    "merchant_category_id" INT   NOT NULL,
    CONSTRAINT "pk_merchant" PRIMARY KEY (
        "merchant_id"
     )
);

CREATE TABLE "transaction" (
    "transaction_id" INT   NOT NULL,
    "date" TIMESTAMP   NOT NULL,
    "amount" INT   NOT NULL,
    "card" VARCHAR(20)   NOT NULL,
    "merchant_id" INT   NOT NULL,
    CONSTRAINT "pk_transaction" PRIMARY KEY (
        "transaction_id"
     )
);

ALTER TABLE "credit_card" ADD CONSTRAINT "fk_credit_card_card_holder_id" FOREIGN KEY("card_holder_id")
REFERENCES "card_holder" ("card_holder_id");

ALTER TABLE "merchant" ADD CONSTRAINT "fk_merchant_merchant_category_id" FOREIGN KEY("merchant_category_id")
REFERENCES "merchant_category" ("merchant_category_id");

ALTER TABLE "transaction" ADD CONSTRAINT "fk_transaction_merchant_id" FOREIGN KEY("merchant_id")
REFERENCES "merchant" ("merchant_id");

