SELECT
  chapter_id,
  COUNT(DISTINCT user_pseudo_id) as user_count
FROM (
  SELECT
      user_pseudo_id,
      max(event_params.value.int_value) as chapter_id  /* 只要已解锁的最大矿层数 */
  FROM
    `{0}.events_*` AS T,
    T.event_params
  WHERE
    event_name = 'af_pass_stage'
    AND event_params.key = 'af_chapter_id'
    AND _TABLE_SUFFIX BETWEEN '{3}' AND '{3}'
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
        AND _TABLE_SUFFIX BETWEEN '{3}' AND '{3}' /* 修改为events数据范围 */
    )
  GROUP BY user_pseudo_id /* 按用户id去重，每个id只保留最大矿层进度数 */
  )
GROUP BY chapter_id
ORDER BY chapter_id
