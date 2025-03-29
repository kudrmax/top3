create table if not exists daily_plans
(
    id         serial primary key,
    tg_id      int  not null,
    date       date not null,
    plans      text not null,
    count      int  not null,
    real_count int,
    constraint unique_date_for_daily_plans unique (date)
);