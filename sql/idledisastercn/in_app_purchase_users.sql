SELECT
  user_pseudo_id,
  event_params.value.string_value as item_name,
  event_timestamp
FROM
  `{0}.events_*` AS T,
  T.event_params
WHERE
  event_name = 'in_app_purchase'
  AND event_params.key = 'product_id'
  AND geo.country = '{2}'
  AND platform = '{1}'
  AND _TABLE_SUFFIX BETWEEN '{3}'
  AND '{4}'
  AND user_pseudo_id IN (
  SELECT
    DISTINCT user_pseudo_id
  FROM
    `{0}.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'first_open'
    AND geo.country = '{2}'
    AND platform = '{1}'
    AND _TABLE_SUFFIX BETWEEN '{3}'
    AND '{3}' )
