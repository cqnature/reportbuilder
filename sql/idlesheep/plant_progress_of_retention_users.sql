SELECT
  max_level,
  COUNT(user_pseudo_id) as user_count
FROM (
  SELECT
      user_pseudo_id,
      max(event_params.value.int_value) as max_level  /* 只要已解锁的最大等级 */
  FROM
    `{0}.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'af_event_level_achieved'
    AND event_params.key = 'af_event_id'
    AND _TABLE_SUFFIX BETWEEN '{3}' AND '{4}' /* 修改为从注册到要查询的留存日期范围 */
    AND user_pseudo_id IN (
      SELECT
        DISTINCT user_pseudo_id
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'first_open'
        AND geo.country != '{2}' /* 修改为指定国家 */
        AND platform = '{1}'
        AND _TABLE_SUFFIX BETWEEN '{3}' AND '{3}' /* 修改为注册日期范围 */
      INTERSECT DISTINCT
      SELECT
        user_pseudo_id
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'user_engagement'
        AND geo.country != '{2}' /* 修改为指定国家 */
        AND platform = '{1}'
        AND _TABLE_SUFFIX BETWEEN '{4}' AND '{4}' /* 修改为留存日期范围 */
    )
  GROUP BY user_pseudo_id /* 按用户id去重，每个id只保留最大矿层进度数 */
  )
GROUP BY max_level
ORDER BY max_level
