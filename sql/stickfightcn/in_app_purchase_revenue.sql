SELECT
  ifnull(sum(event_params.value.int_value)/1000000, 0) as total_revenue
FROM
  `{0}.events_*` AS T,
  T.event_params
WHERE
  event_name = 'in_app_purchase'
  AND event_params.key = 'price'
  --AND geo.country = '{2}'
  AND platform = '{1}'
  AND _TABLE_SUFFIX BETWEEN '{3}'
  AND '{4}'
