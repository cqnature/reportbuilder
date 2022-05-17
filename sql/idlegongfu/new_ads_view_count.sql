SELECT
  C.af_ad_scene,
  C.ad_view_count,
  D.new_user_count,
  C.ad_view_count/D.new_user_count AS daily_average_ad_view_count
FROM (
  SELECT
    af_ad_scene,
    COUNT(user_pseudo_id) AS ad_view_count
  FROM (
    SELECT
      A.user_pseudo_id,
      B.af_ad_scene
    FROM (
      SELECT
        user_pseudo_id,
        event_timestamp,
        event_params.value.int_value AS af_chapter_id
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_ad_view'
        AND event_params.key = 'af_chapter_id'
        AND geo.country = '{2}' /* 修改为指定国家 */
        AND platform = '{1}'
        AND _TABLE_SUFFIX BETWEEN '{4}'
        AND '{4}'
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
        event_params.value.string_value AS af_ad_scene
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_ad_view'
        AND event_params.key = 'af_ad_scene'
        AND geo.country = '{2}' /* 修改为指定国家 */
        AND platform = '{1}'
        AND _TABLE_SUFFIX BETWEEN '{4}'
        AND '{4}' ) AS B
    WHERE
      A.user_pseudo_id = B.user_pseudo_id
      AND A.event_timestamp = B.event_timestamp )
  GROUP BY
    af_ad_scene) AS C,
  (
  SELECT
    COUNT(user_pseudo_id) AS new_user_count
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
