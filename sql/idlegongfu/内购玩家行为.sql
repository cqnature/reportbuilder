SELECT
  ifnull(user_id, '') as user_id,
  event_date,
  event_timestamp,
  app_info.version as app_version,
  event_params.value.string_value as product_name,
FROM
  `{0}.events_*` AS T,
  T.event_params
WHERE
  event_name = 'in_app_purchase'
  AND event_params.key = 'product_name'
  AND geo.country = '{2}'
  AND platform = '{1}'
  AND _TABLE_SUFFIX BETWEEN '{3}'
  AND '{4}'
  AND user_pseudo_id = '{5}'
  order by event_timestamp