SELECT
  A.max_rebirth,
  A.max_level,
  A.user_pseudo_id,
  P.online_time,
  Q.engagement_count
FROM (
  SELECT
    user_pseudo_id,
    0 as max_rebirth,
    1 as max_level
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
    AND '{3}' EXCEPT DISTINCT
  SELECT
    DISTINCT user_pseudo_id
  FROM
    `{0}.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'user_engagement'
    AND geo.country = '{2}'
    AND platform = '{1}'
    AND _TABLE_SUFFIX BETWEEN '{4}'
    AND '{4}' EXCEPT DISTINCT
    SELECT
      DISTINCT user_pseudo_id
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_event_level_achieved'
      AND event_params.key = 'level'
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{4}')
  WHERE
    user_pseudo_id IN (
    SELECT
      DISTINCT user_pseudo_id
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'user_engagement'
      AND geo.country = '{2}' /* 修改为指定国家 */
      AND platform = '{1}'
      AND _TABLE_SUFFIX BETWEEN '{5}'
      AND '{5}' )) AS A
LEFT JOIN (
  SELECT
    user_pseudo_id,
    CAST(ROUND(SUM(online_time)/60) AS INT64) AS online_time
  FROM (
    SELECT
      event_timestamp,
      event_params.value.double_value AS online_time,
      user_pseudo_id
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_alive_time'
      AND event_params.key = 'af_time'
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{4}')
  GROUP BY
    user_pseudo_id) AS P
ON
  A.user_pseudo_id = P.user_pseudo_id
LEFT JOIN (
  SELECT
    user_pseudo_id,
    COUNT(online_time) AS engagement_count
  FROM (
    SELECT
      event_timestamp,
      event_params.value.double_value AS online_time,
      user_pseudo_id
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_alive_time'
      AND event_params.key = 'af_time'
      AND event_params.value.double_value > 60
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{4}')
  GROUP BY
    user_pseudo_id) AS Q
ON
  A.user_pseudo_id = Q.user_pseudo_id
