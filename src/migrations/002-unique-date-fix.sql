alter table daily_plans
    drop constraint if exists unique_date_for_daily_plans;

alter table daily_plans
    add constraint unique_tg_id_date unique (tg_id, date);