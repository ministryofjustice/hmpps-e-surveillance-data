-- Table: e-surv.persons

-- DROP TABLE IF EXISTS "e-surv".persons;

CREATE TABLE IF NOT EXISTS "e-surv".persons
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    delius_id character varying(7) COLLATE pg_catalog."default" NOT NULL,
    unique_device_wearer_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    person_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    given_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    family_name character varying(50) COLLATE pg_catalog."default" NOT NULL,
    alias character varying(50) COLLATE pg_catalog."default",
    "timestamp" character varying(24) COLLATE pg_catalog."default",
    toy boolean DEFAULT false,
    CONSTRAINT persons_pkey PRIMARY KEY (id),
    CONSTRAINT persons_person_id_key UNIQUE (person_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "e-surv".persons
    OWNER to postgres;

COMMENT ON TABLE "e-surv".persons
    IS 'Table for persons on probation. Note that the data profile here is small; identifiers should be used with other systems (e.g. nDelius) for further information.';

COMMENT ON COLUMN "e-surv".persons.toy
    IS 'Indicates whether the record is part of the toy testing dataset';