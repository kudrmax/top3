create table if not exists daily_plans
(
    id          serial primary key,
    telegram_id int not null,
    constraint unique_telegram_id_for_users unique (telegram_id)
);