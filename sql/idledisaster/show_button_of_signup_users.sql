SELECT
    DISTINCT user_pseudo_id
FROM
  `{0}.events_*` AS T,
  T.event_params
WHERE
  event_name = 'af_show_button'
  AND event_params.key = 'af_button_name'
  AND event_params.value.string_value = 'speedup_show'
  AND _TABLE_SUFFIX BETWEEN '{3}' AND '{3}'
  AND user_pseudo_id IN (
    SELECT
       DISTINCT user_pseudo_id
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'first_open'
      AND geo.country = '{2}' /* 修改为指定国家 */
      AND platform = '{1}'
      AND _TABLE_SUFFIX BETWEEN '{3}' AND '{3}' /* 修改为events数据范围 */
  )
