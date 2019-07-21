SELECT
    B.level as level,
    COUNT(B.event_timestamp) as ads_view_count,
    COUNT(DISTINCT B.user_pseudo_id) as ads_user_count
FROM
(
    SELECT
      user_pseudo_id,
      event_timestamp,
      event_params.value.int_value AS af_event_id
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_ad_view'
      AND event_params.key = 'af_event_id'
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
        AND '{4}' )) AS A,
(
    SELECT
      user_pseudo_id,
      event_timestamp,
      event_params.value.int_value AS level
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_ad_view'
      AND event_params.key = 'level' ) AS B
    WHERE
    A.user_pseudo_id = B.user_pseudo_id
    AND A.event_timestamp = B.event_timestamp
    AND A.af_event_id = {5}
GROUP BY B.level
