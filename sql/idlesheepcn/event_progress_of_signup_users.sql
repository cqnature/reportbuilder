SELECT
  instancegame_id,
  stage_id,
  COUNT(user_pseudo_id) AS user_count
FROM (
  SELECT
    C.user_pseudo_id,
    C.event_timestamp,
    D.instancegame_id,
    E.stage_id
  FROM (
    SELECT
      A.user_pseudo_id,
      MAX(A.event_timestamp) AS event_timestamp
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
      A.user_pseudo_id ) AS C,
    (
    SELECT
      user_pseudo_id,
      event_timestamp,
      event_params.value.int_value AS instancegame_id
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_instanceGame_entry'
      AND event_params.key = 'af_instancegame_id' ) AS D,
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
      AND event_params.key = 'af_stage_id' ) AS E
  WHERE
    C.user_pseudo_id = D.user_pseudo_id
    AND C.user_pseudo_id = E.user_pseudo_id
    AND C.event_timestamp = D.event_timestamp
    AND C.event_timestamp = E.event_timestamp )
GROUP BY
  instancegame_id,
  stage_id
ORDER BY
  instancegame_id,
  stage_id
