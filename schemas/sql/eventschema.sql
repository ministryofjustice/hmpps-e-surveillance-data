-- Table: e-surv.events

-- DROP TABLE IF EXISTS "e-surv".events;

CREATE TABLE IF NOT EXISTS "e-surv".events
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    person_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    event_name character varying(150) COLLATE pg_catalog."default" NOT NULL,
    "timestamp" character varying(24) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT events_pkey PRIMARY KEY (id),
    CONSTRAINT pop_fkey FOREIGN KEY (person_id)
        REFERENCES "e-surv".persons (person_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS "e-surv".events
    OWNER to postgres;

COMMENT ON TABLE "e-surv".events
    IS 'Table for tag events. Note that these are immutable. Subsequent events may cancel out. the effecfs of earlier events at the application layer. But the events themselves are not updated.';
-- Index: fki_pop_fkey

-- DROP INDEX IF EXISTS "e-surv".fki_pop_fkey;

CREATE INDEX IF NOT EXISTS fki_pop_fkey
    ON "e-surv".events USING btree
    (person_id COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;