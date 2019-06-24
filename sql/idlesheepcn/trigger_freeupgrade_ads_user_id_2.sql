SELECT
  user_pseudo_id
FROM (
  SELECT
    A.user_pseudo_id,
    H.max_speedup_level,
    I.max_output_level,
    (H.max_speedup_level + I.max_output_level) as total_level
  FROM (
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
      AND '{3}' INTERSECT DISTINCT
    SELECT
      user_pseudo_id
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'user_engagement'
      AND geo.country = '{2}' /* 修改为指定国家 */
      AND platform = '{1}'
      AND _TABLE_SUFFIX BETWEEN '{4}'
      AND '{4}' /* 修改为留存日期范围 */ ) AS A
  LEFT JOIN (
    SELECT
      user_pseudo_id,
      MAX(speedup_level) AS max_speedup_level
    FROM (
      SELECT
        event_timestamp,
        event_params.value.int_value AS speedup_level,
        user_pseudo_id
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_speedup_upgrade'
        AND event_params.key = 'level'
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{4}')
    GROUP BY
      user_pseudo_id) AS H
  ON
    A.user_pseudo_id = H.user_pseudo_id
  LEFT JOIN (
    SELECT
      user_pseudo_id,
      MAX(output_level) AS max_output_level
    FROM (
      SELECT
        event_timestamp,
        event_params.value.int_value AS output_level,
        user_pseudo_id
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_output_upgrade'
        AND event_params.key = 'level'
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{4}')
    GROUP BY
      user_pseudo_id) AS I
  ON
    A.user_pseudo_id = I.user_pseudo_id)
WHERE
  total_level >= 20
