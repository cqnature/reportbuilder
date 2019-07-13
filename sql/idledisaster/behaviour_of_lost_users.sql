SELECT
  A.max_rebirth,
  A.max_level,
  A.user_pseudo_id,
  P.online_time,
  Q.engagement_count,
  T.max_disaster_output_level,
  R.max_disaster_count_level,
  S.max_output_level
FROM (
  SELECT
    user_pseudo_id,
    rebirth as max_rebirth,
    level as max_level
  FROM (
    SELECT
      C.user_pseudo_id,
      C.event_timestamp,
      D.rebirth,
      E.level
    FROM (
      SELECT
        A.user_pseudo_id,
        MAX(A.event_timestamp) AS event_timestamp
      FROM (
        SELECT
          user_pseudo_id,
          event_timestamp,
          event_params.value.int_value AS rebirth
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_event_level_achieved'
          AND event_params.key = 'af_event_id'
          AND _TABLE_SUFFIX BETWEEN '{3}'
          AND '{4}' /* 修改为从注册到要查询的留存日期范围 */
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
            AND '{3}' /* 修改为注册日期范围 */ EXCEPT DISTINCT
          SELECT
            user_pseudo_id
          FROM
            `{0}.events_*` AS T,
            T.event_params
          WHERE
            event_name = 'user_engagement'
            AND geo.country = '{2}' /* 修改为指定国家 */
            AND platform = '{1}'
            AND _TABLE_SUFFIX BETWEEN '{4}'
            AND '{4}' /* 修改为留存日期范围 */ ) ) AS A,
        (
        SELECT
          user_pseudo_id,
          event_timestamp,
          event_params.value.int_value AS level
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_event_level_achieved'
          AND event_params.key = 'level' ) AS B
      WHERE
        A.user_pseudo_id = B.user_pseudo_id
        AND A.event_timestamp = B.event_timestamp
      GROUP BY
        A.user_pseudo_id ) AS C,
      (
      SELECT
        user_pseudo_id,
        event_timestamp,
        event_params.value.int_value AS rebirth
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_event_level_achieved'
        AND event_params.key = 'af_event_id' ) AS D,
      (
      SELECT
        user_pseudo_id,
        event_timestamp,
        event_params.value.int_value AS level
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_event_level_achieved'
        AND event_params.key = 'level' ) AS E
    WHERE
      C.user_pseudo_id = D.user_pseudo_id
      AND C.user_pseudo_id = E.user_pseudo_id
      AND C.event_timestamp = D.event_timestamp
      AND C.event_timestamp = E.event_timestamp
      AND C.user_pseudo_id IN (
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
    )
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
    AND rebirth = {6}
    AND level = {7} ) AS A
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
      AND event_params.value.double_value > 60
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{4}')
  GROUP BY
    user_pseudo_id) AS Q
ON
  A.user_pseudo_id = Q.user_pseudo_id
  LEFT JOIN (
      SELECT
        Z.user_pseudo_id,
        MAX(Z.disaster_output_level) AS max_disaster_output_level
      FROM (
        SELECT
          user_pseudo_id,
          event_timestamp
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_disaster_output_upgrade'
          AND event_params.key = 'af_disaster_id'
          AND event_params.value.int_value = 1
          AND _TABLE_SUFFIX BETWEEN '{3}'
          AND '{4}' ) AS X,
        (
        SELECT
          user_pseudo_id,
          event_timestamp
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_disaster_output_upgrade'
          AND event_params.key = 'af_event_id'
          AND event_params.value.int_value = 0
          AND _TABLE_SUFFIX BETWEEN '{3}'
          AND '{4}' ) AS Y,
      (
      SELECT
        user_pseudo_id,
        event_params.value.int_value AS disaster_output_level,
        event_timestamp
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_disaster_output_upgrade'
        AND event_params.key = 'level'
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{4}' ) AS Z
      WHERE
        X.user_pseudo_id = Y.user_pseudo_id
        AND X.event_timestamp = Y.event_timestamp
        AND X.user_pseudo_id = Z.user_pseudo_id
        AND X.event_timestamp = Z.event_timestamp
      GROUP BY
        user_pseudo_id
    ) AS T
  ON
    A.user_pseudo_id = T.user_pseudo_id
LEFT JOIN (
    SELECT
      Z.user_pseudo_id,
      MAX(Z.disaster_count_level) AS max_disaster_count_level
    FROM (
      SELECT
        user_pseudo_id,
        event_timestamp
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_disaster_count_upgrade'
        AND event_params.key = 'af_disaster_id'
        AND event_params.value.int_value = 1
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{4}' ) AS X,
      (
      SELECT
        user_pseudo_id,
        event_timestamp
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_disaster_count_upgrade'
        AND event_params.key = 'af_event_id'
        AND event_params.value.int_value = 0
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{4}' ) AS Y,
    (
    SELECT
      user_pseudo_id,
      event_params.value.int_value AS disaster_count_level,
      event_timestamp
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_disaster_count_upgrade'
      AND event_params.key = 'level'
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{4}' ) AS Z
    WHERE
      X.user_pseudo_id = Y.user_pseudo_id
      AND X.event_timestamp = Y.event_timestamp
      AND X.user_pseudo_id = Z.user_pseudo_id
      AND X.event_timestamp = Z.event_timestamp
    GROUP BY
      user_pseudo_id
  ) AS R
ON
  A.user_pseudo_id = R.user_pseudo_id
  LEFT JOIN (
      SELECT
        Z.user_pseudo_id,
        MAX(Z.output_level) AS max_output_level
      FROM (
        SELECT
          user_pseudo_id,
          event_timestamp
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_output_upgrade'
          AND event_params.key = 'af_event_id'
          AND event_params.value.int_value = 0
          AND _TABLE_SUFFIX BETWEEN '{3}'
          AND '{4}' ) AS X,
      (
      SELECT
        user_pseudo_id,
        event_params.value.int_value AS output_level,
        event_timestamp
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_output_upgrade'
        AND event_params.key = 'level'
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{4}' ) AS Y
      WHERE
        X.user_pseudo_id = Y.user_pseudo_id
        AND X.event_timestamp = Y.event_timestamp
      GROUP BY
        user_pseudo_id
    ) AS S
  ON
    A.user_pseudo_id = S.user_pseudo_id
