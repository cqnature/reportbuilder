SELECT
  A.max_level,
  A.user_pseudo_id,
  B.compound_count,
  C.enter_shop_count,
  P.online_time,
  Q.engagement_count
FROM (
  SELECT
    user_pseudo_id,
    max_level
  FROM (
    SELECT
      user_pseudo_id,
      MAX(event_params.value.int_value) AS max_level
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'level_up'
      AND event_params.key = 'level'
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
        AND '{4}')
    GROUP BY
      user_pseudo_id)
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
      AND '{5}' )
    AND max_level = {6} ) AS A
LEFT JOIN (
    SELECT
    F.user_pseudo_id,
    COUNT(F.event_timestamp) AS compound_count
  FROM (
    SELECT
      user_pseudo_id,
      event_timestamp
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_compound_food'
      AND event_params.key = 'af_customer_user_id'
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{4}' ) AS F,
    (
    SELECT
      user_pseudo_id,
      MIN(event_timestamp) AS min_event_timestamp
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_compound_food'
      AND event_params.key = 'level'
      AND event_params.value.int_value = {6}
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{4}'
    GROUP BY
      user_pseudo_id) AS G
  WHERE
    F.user_pseudo_id = G.user_pseudo_id
    AND F.event_timestamp > G.min_event_timestamp
  GROUP BY user_pseudo_id ) AS B
ON
  A.user_pseudo_id = B.user_pseudo_id
LEFT JOIN (
  SELECT
      D.user_pseudo_id,
      COUNT(D.event_timestamp) as enter_shop_count
    FROM (
    SELECT
      user_pseudo_id,
      event_timestamp
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_click_button'
      AND event_params.key = 'af_button_name'
      AND event_params.value.string_value = 'menu_click'
      AND _TABLE_SUFFIX BETWEEN '{5}'
      AND '{5}') AS D,
    (SELECT
      user_pseudo_id,
      event_timestamp
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_click_button'
      AND event_params.key = 'level'
      AND event_params.value.int_value = {6}
      AND _TABLE_SUFFIX BETWEEN '{5}'
      AND '{5}') AS E
    WHERE D.user_pseudo_id = E.user_pseudo_id
    AND D.event_timestamp = E.event_timestamp
    GROUP BY user_pseudo_id ) AS C
ON
    A.user_pseudo_id = C.user_pseudo_id
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
      AND event_params.value.double_value > 120
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{4}')
  GROUP BY
    user_pseudo_id) AS Q
ON
  A.user_pseudo_id = Q.user_pseudo_id
