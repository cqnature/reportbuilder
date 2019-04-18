SELECT
  max_stage,
  COUNT(user_pseudo_id) AS user_count
FROM (
  SELECT
    user_pseudo_id,
    MAX(event_params.value.int_value) AS max_stage
  FROM
    `{0}.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'af_stage_progress'
    AND event_params.key = 'af_stage'
    AND _TABLE_SUFFIX BETWEEN '{3}'
    AND '{3}'
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
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{3}'
  )
  GROUP BY
    user_pseudo_id)
GROUP BY
  max_stage
ORDER BY
  max_stage
