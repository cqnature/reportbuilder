SELECT
  event_date,
  app_info.version as app_version
FROM
  `{0}.events_*` AS T,
  T.event_params
WHERE
  event_name = 'first_open'
  AND _TABLE_SUFFIX BETWEEN '{3}'
  AND '{3}' /* 修改为从注册到要查询的留存日期范围 */
  AND user_pseudo_id = '{4}'