SELECT
  C.ad_position,
  C.ad_view_count,
  D.daily_user_count,
  C.ad_view_count/D.daily_user_count AS daily_average_ad_view_count
FROM (
  SELECT
    ad_position,
    COUNT(user_pseudo_id) AS ad_view_count
  FROM (
    SELECT
      A.user_pseudo_id,
      B.ad_position
    FROM (
      SELECT
        user_pseudo_id,
        event_timestamp,
        event_params.value.int_value AS af_max_stage
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'ad_show'
        AND event_params.key = 'af_max_stage'
        AND geo.country = '{2}' /* 修改为指定国家 */
        AND platform = '{1}'
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{3}' ) AS A,
      (
      SELECT
        user_pseudo_id,
        event_timestamp,
        event_params.value.string_value AS ad_position
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'ad_show'
        AND event_params.key = 'ad_position'
        AND geo.country = '{2}' /* 修改为指定国家 */
        AND platform = '{1}'
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{3}' ) AS B
    WHERE
      A.user_pseudo_id = B.user_pseudo_id
      AND A.event_timestamp = B.event_timestamp )
  GROUP BY
    ad_position) AS C,
  (
  SELECT
    COUNT(DISTINCT user_pseudo_id) AS daily_user_count
  FROM
    `{0}.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'user_engagement'
    AND geo.country = '{2}' /* 修改为指定国家 */
    AND platform = '{1}'
    AND _TABLE_SUFFIX BETWEEN '{3}'
    AND '{3}') AS D
