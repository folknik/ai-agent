create database users;
\connect users;

create schema if not exists users;

create table if not exists users.user_requests (
    id              serial primary key,
    user_id         int8 not null,
    chat_id         int8 not null,
    is_bot          boolean not null,
    first_name      varchar not null,
    last_name       varchar null,
    username        varchar null,
    is_premium      boolean null,
    url             varchar not null,
    created_at      timestamptz default now() not null
 );


create table if not exists users.chats (
    id              serial primary key,
    chat_id         int8 not null,
    user_id         int8 not null,
    created_at      timestamptz default now() not null
 );