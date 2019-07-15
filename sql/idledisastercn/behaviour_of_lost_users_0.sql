SELECT
  A.max_rebirth,
  A.max_level,
  A.user_pseudo_id,
  P.online_time,
  Q.engagement_count,
  S.max_output_level,
  U.max_speedup_level,
  V.max_extracount_level,
  R.max_disaster_count_level,
  T.max_disaster_output_level,
  W.max_disaster_speedup_level,
  O.max_disaster_skill_level,
  B.guide1_begin_trigger,
  C.guide1_house_trigger,
  D.guide1_disaster_trigger,
  L.guide1_end_trigger,
  E.guide5_begin_trigger,
  F.guide5_end_trigger,
  G.guide7_begin_trigger,
  H.guide7_end_trigger,
  I.guide8_begin_trigger,
  J.guide8_end_trigger,
  K.guide9_begin_trigger,
  M.guide9_end_trigger
FROM (
  SELECT
    user_pseudo_id,
    0 as max_rebirth,
    1 as max_level
  FROM (
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
    AND '{4}' EXCEPT DISTINCT
    SELECT
      DISTINCT user_pseudo_id
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_event_level_achieved'
      AND event_params.key = 'level'
      AND _TABLE_SUFFIX BETWEEN '{3}'
      AND '{4}')
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
      AND '{5}' )) AS A
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
        X.user_pseudo_id,
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
      X.user_pseudo_id,
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
        X.user_pseudo_id,
        MAX(Y.output_level) AS max_output_level
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
    LEFT JOIN (
        SELECT
          X.user_pseudo_id,
          MAX(Y.speedup_level) AS max_speedup_level
        FROM (
          SELECT
            user_pseudo_id,
            event_timestamp
          FROM
            `{0}.events_*` AS T,
            T.event_params
          WHERE
            event_name = 'af_speedup_upgrade'
            AND event_params.key = 'af_event_id'
            AND event_params.value.int_value = 0
            AND _TABLE_SUFFIX BETWEEN '{3}'
            AND '{4}' ) AS X,
        (
        SELECT
          user_pseudo_id,
          event_params.value.int_value AS speedup_level,
          event_timestamp
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_speedup_upgrade'
          AND event_params.key = 'level'
          AND _TABLE_SUFFIX BETWEEN '{3}'
          AND '{4}' ) AS Y
        WHERE
          X.user_pseudo_id = Y.user_pseudo_id
          AND X.event_timestamp = Y.event_timestamp
        GROUP BY
          user_pseudo_id
      ) AS U
    ON
      A.user_pseudo_id = U.user_pseudo_id
  LEFT JOIN (
      SELECT
        X.user_pseudo_id,
        MAX(Y.extracount_level) AS max_extracount_level
      FROM (
        SELECT
          user_pseudo_id,
          event_timestamp
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_extracount_upgrade'
          AND event_params.key = 'af_event_id'
          AND event_params.value.int_value = 0
          AND _TABLE_SUFFIX BETWEEN '{3}'
          AND '{4}' ) AS X,
      (
      SELECT
        user_pseudo_id,
        event_params.value.int_value AS extracount_level,
        event_timestamp
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_extracount_upgrade'
        AND event_params.key = 'level'
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{4}' ) AS Y
      WHERE
        X.user_pseudo_id = Y.user_pseudo_id
        AND X.event_timestamp = Y.event_timestamp
      GROUP BY
        user_pseudo_id
    ) AS V
  ON
    A.user_pseudo_id = V.user_pseudo_id
  LEFT JOIN (
    SELECT
      X.user_pseudo_id,
      MAX(Z.disaster_speedup_level) AS max_disaster_speedup_level
    FROM (
      SELECT
        user_pseudo_id,
        event_timestamp
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_disaster_speedUp_upgrade'
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
        event_name = 'af_disaster_speedUp_upgrade'
        AND event_params.key = 'af_event_id'
        AND event_params.value.int_value = 0
        AND _TABLE_SUFFIX BETWEEN '{3}'
        AND '{4}' ) AS Y,
    (
    SELECT
      user_pseudo_id,
      event_params.value.int_value AS disaster_speedup_level,
      event_timestamp
    FROM
      `{0}.events_*` AS T,
      T.event_params
    WHERE
      event_name = 'af_disaster_speedUp_upgrade'
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
  ) AS W
  ON
  A.user_pseudo_id = W.user_pseudo_id
  LEFT JOIN (
      SELECT
        X.user_pseudo_id,
        MAX(Z.disaster_skill_level) AS max_disaster_skill_level
      FROM (
        SELECT
          user_pseudo_id,
          event_timestamp
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_disaster_skill_upgrade'
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
          event_name = 'af_disaster_skill_upgrade'
          AND event_params.key = 'af_event_id'
          AND event_params.value.int_value = 0
          AND _TABLE_SUFFIX BETWEEN '{3}'
          AND '{4}' ) AS Y,
      (
      SELECT
        user_pseudo_id,
        event_params.value.int_value AS disaster_skill_level,
        event_timestamp
      FROM
        `{0}.events_*` AS T,
        T.event_params
      WHERE
        event_name = 'af_disaster_skill_upgrade'
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
    ) AS O
  ON
    A.user_pseudo_id = O.user_pseudo_id
    LEFT JOIN (
      SELECT
        user_pseudo_id,
        COUNT(event_timestamp) AS guide1_begin_trigger
      FROM (
        SELECT
          event_timestamp,
          user_pseudo_id
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_track_scene'
          AND event_params.key = 'af_scene'
          AND event_params.value.string_value = 'guide1_begin'
          AND _TABLE_SUFFIX BETWEEN '{3}'
          AND '{4}')
      GROUP BY
        user_pseudo_id) AS B
        ON
          A.user_pseudo_id = B.user_pseudo_id
    LEFT JOIN (
      SELECT
        user_pseudo_id,
        COUNT(event_timestamp) AS guide1_house_trigger
      FROM (
        SELECT
          event_timestamp,
          user_pseudo_id
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_track_scene'
          AND event_params.key = 'af_scene'
          AND event_params.value.string_value = 'guide1_house'
          AND _TABLE_SUFFIX BETWEEN '{3}'
          AND '{4}')
      GROUP BY
        user_pseudo_id) AS C
        ON
          A.user_pseudo_id = C.user_pseudo_id
    LEFT JOIN (
      SELECT
        user_pseudo_id,
        COUNT(event_timestamp) AS guide1_disaster_trigger
      FROM (
        SELECT
          event_timestamp,
          user_pseudo_id
        FROM
          `{0}.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_track_scene'
          AND event_params.key = 'af_scene'
          AND event_params.value.string_value = 'guide1_disaster'
          AND _TABLE_SUFFIX BETWEEN '{3}'
          AND '{4}')
      GROUP BY
        user_pseudo_id) AS D
        ON
          A.user_pseudo_id = D.user_pseudo_id
      LEFT JOIN (
        SELECT
          user_pseudo_id,
          COUNT(event_timestamp) AS guide1_end_trigger
        FROM (
          SELECT
            event_timestamp,
            user_pseudo_id
          FROM
            `{0}.events_*` AS T,
            T.event_params
          WHERE
            event_name = 'af_track_scene'
            AND event_params.key = 'af_scene'
            AND event_params.value.string_value = 'guide1_end'
            AND _TABLE_SUFFIX BETWEEN '{3}'
            AND '{4}')
        GROUP BY
          user_pseudo_id) AS L
          ON
            A.user_pseudo_id = L.user_pseudo_id
        LEFT JOIN (
          SELECT
            user_pseudo_id,
            COUNT(event_timestamp) AS guide5_begin_trigger
          FROM (
            SELECT
              event_timestamp,
              user_pseudo_id
            FROM
              `{0}.events_*` AS T,
              T.event_params
            WHERE
              event_name = 'af_track_scene'
              AND event_params.key = 'af_scene'
              AND event_params.value.string_value = 'guide5_begin'
              AND _TABLE_SUFFIX BETWEEN '{3}'
              AND '{4}')
          GROUP BY
            user_pseudo_id) AS E
            ON
              A.user_pseudo_id = E.user_pseudo_id
          LEFT JOIN (
            SELECT
              user_pseudo_id,
              COUNT(event_timestamp) AS guide5_end_trigger
            FROM (
              SELECT
                event_timestamp,
                user_pseudo_id
              FROM
                `{0}.events_*` AS T,
                T.event_params
              WHERE
                event_name = 'af_track_scene'
                AND event_params.key = 'af_scene'
                AND event_params.value.string_value = 'guide5_end'
                AND _TABLE_SUFFIX BETWEEN '{3}'
                AND '{4}')
            GROUP BY
              user_pseudo_id) AS F
              ON
                A.user_pseudo_id = F.user_pseudo_id
            LEFT JOIN (
              SELECT
                user_pseudo_id,
                COUNT(event_timestamp) AS guide7_begin_trigger
              FROM (
                SELECT
                  event_timestamp,
                  user_pseudo_id
                FROM
                  `{0}.events_*` AS T,
                  T.event_params
                WHERE
                  event_name = 'af_track_scene'
                  AND event_params.key = 'af_scene'
                  AND event_params.value.string_value = 'guide7_begin'
                  AND _TABLE_SUFFIX BETWEEN '{3}'
                  AND '{4}')
              GROUP BY
                user_pseudo_id) AS G
                ON
                  A.user_pseudo_id = G.user_pseudo_id
          LEFT JOIN (
            SELECT
              user_pseudo_id,
              COUNT(event_timestamp) AS guide7_end_trigger
            FROM (
              SELECT
                event_timestamp,
                user_pseudo_id
              FROM
                `{0}.events_*` AS T,
                T.event_params
              WHERE
                event_name = 'af_track_scene'
                AND event_params.key = 'af_scene'
                AND event_params.value.string_value = 'guide7_end'
                AND _TABLE_SUFFIX BETWEEN '{3}'
                AND '{4}')
            GROUP BY
              user_pseudo_id) AS H
              ON
                A.user_pseudo_id = H.user_pseudo_id
            LEFT JOIN (
              SELECT
                user_pseudo_id,
                COUNT(event_timestamp) AS guide8_begin_trigger
              FROM (
                SELECT
                  event_timestamp,
                  user_pseudo_id
                FROM
                  `{0}.events_*` AS T,
                  T.event_params
                WHERE
                  event_name = 'af_track_scene'
                  AND event_params.key = 'af_scene'
                  AND event_params.value.string_value = 'guide8_begin'
                  AND _TABLE_SUFFIX BETWEEN '{3}'
                  AND '{4}')
              GROUP BY
                user_pseudo_id) AS I
                ON
                  A.user_pseudo_id = I.user_pseudo_id
              LEFT JOIN (
                SELECT
                  user_pseudo_id,
                  COUNT(event_timestamp) AS guide8_end_trigger
                FROM (
                  SELECT
                    event_timestamp,
                    user_pseudo_id
                  FROM
                    `{0}.events_*` AS T,
                    T.event_params
                  WHERE
                    event_name = 'af_track_scene'
                    AND event_params.key = 'af_scene'
                    AND event_params.value.string_value = 'guide8_end'
                    AND _TABLE_SUFFIX BETWEEN '{3}'
                    AND '{4}')
                GROUP BY
                  user_pseudo_id) AS J
                  ON
                    A.user_pseudo_id = J.user_pseudo_id
            LEFT JOIN (
              SELECT
                user_pseudo_id,
                COUNT(event_timestamp) AS guide9_begin_trigger
              FROM (
                SELECT
                  event_timestamp,
                  user_pseudo_id
                FROM
                  `{0}.events_*` AS T,
                  T.event_params
                WHERE
                  event_name = 'af_track_scene'
                  AND event_params.key = 'af_scene'
                  AND event_params.value.string_value = 'guide9_begin'
                  AND _TABLE_SUFFIX BETWEEN '{3}'
                  AND '{4}')
              GROUP BY
                user_pseudo_id) AS K
                ON
                  A.user_pseudo_id = K.user_pseudo_id
              LEFT JOIN (
                SELECT
                  user_pseudo_id,
                  COUNT(event_timestamp) AS guide9_end_trigger
                FROM (
                  SELECT
                    event_timestamp,
                    user_pseudo_id
                  FROM
                    `{0}.events_*` AS T,
                    T.event_params
                  WHERE
                    event_name = 'af_track_scene'
                    AND event_params.key = 'af_scene'
                    AND event_params.value.string_value = 'guide9_end'
                    AND _TABLE_SUFFIX BETWEEN '{3}'
                    AND '{4}')
                GROUP BY
                  user_pseudo_id) AS M
                  ON
                    A.user_pseudo_id = M.user_pseudo_id
