SELECT
  user_pseudo_id,
  event_timestamp,
  event_params.value.int_value AS max_stage
FROM
  `{0}.events_*` AS T,
  T.event_params
WHERE
  event_name = 'ad_show'
  AND event_params.key = 'max_stage'
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
    AND '{4}' )
