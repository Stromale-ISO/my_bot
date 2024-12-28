--
-- PostgreSQL database dump
--

-- Dumped from database version 16.6 (Ubuntu 16.6-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.6 (Ubuntu 16.6-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: persons; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.persons (
    person_id integer NOT NULL,
    person_name character varying(50) NOT NULL,
    person_surname character varying(50) NOT NULL,
    person_birthdate date NOT NULL,
    person_description text
);


ALTER TABLE public.persons OWNER TO postgres;

--
-- Name: persons_person_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.persons_person_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.persons_person_id_seq OWNER TO postgres;

--
-- Name: persons_person_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.persons_person_id_seq OWNED BY public.persons.person_id;


--
-- Name: persons person_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.persons ALTER COLUMN person_id SET DEFAULT nextval('public.persons_person_id_seq'::regclass);


--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.persons (person_id, person_name, person_surname, person_birthdate, person_description) FROM stdin;
8	Иван	Иванов	1990-01-01	Программист Python
9	Мария	Петрова	1992-03-15	Дизайнер интерфейсов
10	Алексей	Смирнов	1988-06-25	Проектный менеджер
11	Ольга	Кузнецова	1995-10-10	Тестировщик программного обеспечения
12	Сергей	Попов	1985-11-20	Системный администратор
13	Анна	Новикова	1997-07-07	Специалист по Data Science
14	Дмитрий	Васильев	1983-12-05	Старший аналитик
15	Екатерина	Морозова	1991-04-18	Младший разработчик
16	Николай	Соколов	1989-09-09	Архитектор решений
17	Татьяна	Крылова	1994-02-28	Бизнес-аналитик
18	Владимир	Зайцев	1980-08-15	Сетевой инженер
19	Елена	Фролова	1993-01-10	Менеджер по продукту
20	Павел	Медведев	1987-05-30	Инженер DevOps
21	Алина	Григорьева	1996-11-11	Разработчик мобильных приложений
31	П	А	2000-01-01	Папьаь
\.


--
-- Name: persons_person_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.persons_person_id_seq', 31, true);


--
-- Name: persons persons_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (person_id);


--
-- PostgreSQL database dump complete
--

