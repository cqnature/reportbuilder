SELECT
  A.user_pseudo_id,
  A.item_name,
  A.event_timestamp,
  B.value
FROM (
  SELECT
    user_pseudo_id,
    event_params.value.string_value AS item_name,
    event_timestamp
  FROM
    `{0}.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'spend_virtual_currency'
    AND event_params.key = 'item_name'
    AND geo.country != '{2}'
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
      AND geo.country != '{2}'
      AND platform = '{1}'
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{3}' ) ) AS A,
  (
  SELECT
    user_pseudo_id,
    event_params.value.double_value AS value,
    event_timestamp
  FROM
    `{0}.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'spend_virtual_currency'
    AND event_params.key = 'value'
    AND geo.country != '{2}'
    AND platform = '{1}'
    AND _TABLE_SUFFIX BETWEEN '{3}'
    AND '{4}' ) AS B
WHERE
  A.user_pseudo_id = B.user_pseudo_id
  AND A.event_timestamp = B.event_timestamp
