SELECT
  instancegame_id,
  event_count,
  COUNT(user_pseudo_id) AS user_count
FROM (
    SELECT
      A.user_pseudo_id,
      A.instancegame_id,
      COUNT(A.event_timestamp) AS event_count
    FROM (
      SELECT
        user_pseudo_id,
        event_timestamp,
        event_params.value.int_value AS instancegame_id
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_instanceGame_entry'
        AND event_params.key = 'af_instancegame_id'
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{3}' /* 修改为从注册到要查询的留存日期范围 */
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
          AND '{3}' ) ) AS A,
      (
      SELECT
        user_pseudo_id,
        event_timestamp,
        event_params.value.int_value AS stage_id
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_instanceGame_entry'
        AND event_params.key = 'af_stage_id' ) AS B
    WHERE
      A.user_pseudo_id = B.user_pseudo_id
      AND A.event_timestamp = B.event_timestamp
    GROUP BY
      A.user_pseudo_id,
      A.instancegame_id
  )
GROUP BY
  instancegame_id,
  event_count
ORDER BY
  instancegame_id,
  event_count
