SELECT
  C.af_button_name,
  C.ad_click_count,
  D.retention_user_count,
  C.ad_click_count/D.retention_user_count AS retetion_average_ad_click_count
FROM (
  SELECT
    af_button_name,
    COUNT(user_pseudo_id) AS ad_click_count
  FROM (
    SELECT
      A.user_pseudo_id,
      B.af_button_name
    FROM (
      SELECT
        user_pseudo_id,
        event_timestamp,
        event_params.value.int_value AS level
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_click_button'
        AND event_params.key = 'level'
        AND geo.country = '{2}' /* 修改为指定国家 */
        AND platform = '{1}'
        AND _TABLE_SUFFIX BETWEEN '{5}'
        AND '{5}'
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
          AND '{3}' INTERSECT DISTINCT /* 保留留存用户 */
        SELECT
          DISTINCT user_pseudo_id
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'user_engagement'
          AND geo.country = '{2}' /* 修改为指定国家 */
          AND platform = '{1}'
          AND _TABLE_SUFFIX BETWEEN '{4}'
          AND '{4}' ) ) AS A,
      (
      SELECT
        user_pseudo_id,
        event_timestamp,
        event_params.value.string_value AS af_button_name
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_click_button'
        AND event_params.key = 'af_button_name'
        AND geo.country = '{2}' /* 修改为指定国家 */
        AND platform = '{1}'
        AND _TABLE_SUFFIX BETWEEN '{5}'
        AND '{5}' ) AS B
    WHERE
      A.user_pseudo_id = B.user_pseudo_id
      AND A.event_timestamp = B.event_timestamp )
  GROUP BY
    af_button_name) AS C,
  (
  SELECT
    COUNT(user_pseudo_id) AS retention_user_count
  FROM (
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
        AND '{3}' INTERSECT DISTINCT /* 保留留存用户 */
      SELECT
        DISTINCT user_pseudo_id
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'user_engagement'
        AND geo.country = '{2}' /* 修改为指定国家 */
        AND platform = '{1}'
        AND _TABLE_SUFFIX BETWEEN '{4}'
        AND '{4}' ) ) AS D
