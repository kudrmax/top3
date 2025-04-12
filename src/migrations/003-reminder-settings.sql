create table if not exists reminder_settings
(
    id                     serial primary key,
    tg_id                  int not null,
    creation_reminder_time text,
    reminder_times         text[],
    constraint unique_tg_id_for_reminder_settings unique (tg_id)
);