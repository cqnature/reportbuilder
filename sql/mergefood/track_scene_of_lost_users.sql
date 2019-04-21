SELECT B.first_open,
        A1.entrance_animation_begin,
        A2.guide1_begin,
        A3.guide1_compound_food2,
        A4.guide1_enter_name_begin,
        A5.guide1_enter_name_end,
        A6.guide3_begin,
        A7.guide3_end FROM
(
    SELECT count(user_pseudo_id) as first_open from (
        SELECT
            DISTINCT user_pseudo_id
        FROM
            `analytics_188328474.events_*` AS T,
            T.event_params
        WHERE
            event_name = 'first_open'
            AND geo.country = 'China' /* 修改为指定国家 */
            AND platform = '{0}'
            AND _TABLE_SUFFIX BETWEEN '{1}' AND '{2}'
            AND user_pseudo_id IN (
                SELECT
                    DISTINCT user_pseudo_id
                  FROM
                    `analytics_188328474.events_*` AS T,
                    T.event_params
                  WHERE
                    event_name = 'first_open'
                    AND geo.country = 'China' /* 修改为指定国家 */
                    AND platform = '{0}'
                    AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为注册日期范围 */
      				EXCEPT DISTINCT /* 排除留存用户 */
      				SELECT
      					DISTINCT user_pseudo_id
      				FROM
      					`analytics_188328474.events_*` AS T,
      					T.event_params
      				WHERE
      					event_name = 'user_engagement'
      					AND geo.country = 'China' /* 修改为指定国家 */
      					AND platform = '{0}'
      					AND _TABLE_SUFFIX BETWEEN '{2}' AND '{2}' /* 修改为留存日期范围 */
            )
    )
) AS B,
(
    SELECT count(user_pseudo_id) as entrance_animation_begin from (
        SELECT
          user_pseudo_id
        FROM
          `analytics_188328474.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_track_scene'
          AND event_params.key = 'af_scene'
          AND event_params.value.string_value	= 'entrance_animation_begin'
          AND _TABLE_SUFFIX BETWEEN '{1}' AND '{2}'
          AND user_pseudo_id IN (
              SELECT
                  DISTINCT user_pseudo_id
                FROM
                  `analytics_188328474.events_*` AS T,
                  T.event_params
                WHERE
                  event_name = 'first_open'
                  AND geo.country = 'China' /* 修改为指定国家 */
                  AND platform = '{0}'
                  AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为注册日期范围 */
    				EXCEPT DISTINCT /* 排除留存用户 */
    				SELECT
    					DISTINCT user_pseudo_id
    				FROM
    					`analytics_188328474.events_*` AS T,
    					T.event_params
    				WHERE
    					event_name = 'user_engagement'
    					AND geo.country = 'China' /* 修改为指定国家 */
    					AND platform = '{0}'
    					AND _TABLE_SUFFIX BETWEEN '{2}' AND '{2}' /* 修改为留存日期范围 */
          )
          GROUP BY user_pseudo_id
    )
) AS A1,
(
    SELECT count(user_pseudo_id) as guide1_begin from (
        SELECT
          user_pseudo_id
        FROM
          `analytics_188328474.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_track_scene'
          AND event_params.key = 'af_scene'
          AND event_params.value.string_value	= 'guide1_begin'
          AND _TABLE_SUFFIX BETWEEN '{1}' AND '{2}'
          AND user_pseudo_id IN (
              SELECT
                  DISTINCT user_pseudo_id
                FROM
                  `analytics_188328474.events_*` AS T,
                  T.event_params
                WHERE
                  event_name = 'first_open'
                  AND geo.country = 'China' /* 修改为指定国家 */
                  AND platform = '{0}'
                  -- AND _TABLE_SUFFIX BETWEEN '20190306' AND '20190306' /* 修改为注册日期范围 */
                  AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为注册日期范围 */
    				EXCEPT DISTINCT /* 排除留存用户 */
    				SELECT
    					DISTINCT user_pseudo_id
    				FROM
    					`analytics_188328474.events_*` AS T,
    					T.event_params
    				WHERE
    					event_name = 'user_engagement'
    					AND geo.country = 'China' /* 修改为指定国家 */
    					AND platform = '{0}'
    					AND _TABLE_SUFFIX BETWEEN '{2}' AND '{2}' /* 修改为留存日期范围 */
          )
          GROUP BY user_pseudo_id
    )
) AS A2,
(
    SELECT count(user_pseudo_id) as guide1_compound_food2 from (
        SELECT
          user_pseudo_id
        FROM
          `analytics_188328474.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_track_scene'
          AND event_params.key = 'af_scene'
          AND event_params.value.string_value	= 'guide1_compound_food2'
          AND _TABLE_SUFFIX BETWEEN '{1}' AND '{2}'
          AND user_pseudo_id IN (
              SELECT
                  DISTINCT user_pseudo_id
                FROM
                  `analytics_188328474.events_*` AS T,
                  T.event_params
                WHERE
                  event_name = 'first_open'
                  AND geo.country = 'China' /* 修改为指定国家 */
                  AND platform = '{0}'
                  -- AND _TABLE_SUFFIX BETWEEN '20190306' AND '20190306' /* 修改为注册日期范围 */
                  AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为注册日期范围 */
    				EXCEPT DISTINCT /* 排除留存用户 */
    				SELECT
    					DISTINCT user_pseudo_id
    				FROM
    					`analytics_188328474.events_*` AS T,
    					T.event_params
    				WHERE
    					event_name = 'user_engagement'
    					AND geo.country = 'China' /* 修改为指定国家 */
    					AND platform = '{0}'
    					AND _TABLE_SUFFIX BETWEEN '{2}' AND '{2}' /* 修改为留存日期范围 */
          )
          GROUP BY user_pseudo_id
    )
) AS A3,
(
    SELECT count(user_pseudo_id) as guide1_enter_name_begin from (
        SELECT
          user_pseudo_id
        FROM
          `analytics_188328474.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_track_scene'
          AND event_params.key = 'af_scene'
          AND event_params.value.string_value	= 'guide1_enter_name_begin'
          AND _TABLE_SUFFIX BETWEEN '{1}' AND '{2}'
          AND user_pseudo_id IN (
              SELECT
                  DISTINCT user_pseudo_id
                FROM
                  `analytics_188328474.events_*` AS T,
                  T.event_params
                WHERE
                  event_name = 'first_open'
                  AND geo.country = 'China' /* 修改为指定国家 */
                  AND platform = '{0}'
                  -- AND _TABLE_SUFFIX BETWEEN '20190306' AND '20190306' /* 修改为注册日期范围 */
                  AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为注册日期范围 */
    				EXCEPT DISTINCT /* 排除留存用户 */
    				SELECT
    					DISTINCT user_pseudo_id
    				FROM
    					`analytics_188328474.events_*` AS T,
    					T.event_params
    				WHERE
    					event_name = 'user_engagement'
    					AND geo.country = 'China' /* 修改为指定国家 */
    					AND platform = '{0}'
    					AND _TABLE_SUFFIX BETWEEN '{2}' AND '{2}' /* 修改为留存日期范围 */
          )
          GROUP BY user_pseudo_id
    )
) AS A4,
(
    SELECT count(user_pseudo_id) as guide1_enter_name_end from (
        SELECT
          user_pseudo_id
        FROM
          `analytics_188328474.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_track_scene'
          AND event_params.key = 'af_scene'
          AND event_params.value.string_value	= 'guide1_enter_name_end'
          AND _TABLE_SUFFIX BETWEEN '{1}' AND '{2}'
          AND user_pseudo_id IN (
              SELECT
                  DISTINCT user_pseudo_id
                FROM
                  `analytics_188328474.events_*` AS T,
                  T.event_params
                WHERE
                  event_name = 'first_open'
                  AND geo.country = 'China' /* 修改为指定国家 */
                  AND platform = '{0}'
                  -- AND _TABLE_SUFFIX BETWEEN '20190306' AND '20190306' /* 修改为注册日期范围 */
                  AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为注册日期范围 */
    				EXCEPT DISTINCT /* 排除留存用户 */
    				SELECT
    					DISTINCT user_pseudo_id
    				FROM
    					`analytics_188328474.events_*` AS T,
    					T.event_params
    				WHERE
    					event_name = 'user_engagement'
    					AND geo.country = 'China' /* 修改为指定国家 */
    					AND platform = '{0}'
    					AND _TABLE_SUFFIX BETWEEN '{2}' AND '{2}' /* 修改为留存日期范围 */
          )
          GROUP BY user_pseudo_id
    )
) AS A5,
(
    SELECT count(user_pseudo_id) as guide3_begin from (
        SELECT
          user_pseudo_id
        FROM
          `analytics_188328474.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_track_scene'
          AND event_params.key = 'af_scene'
          AND event_params.value.string_value	= 'guide3_begin'
          AND _TABLE_SUFFIX BETWEEN '{1}' AND '{2}'
          AND user_pseudo_id IN (
              SELECT
                  DISTINCT user_pseudo_id
                FROM
                  `analytics_188328474.events_*` AS T,
                  T.event_params
                WHERE
                  event_name = 'first_open'
                  AND geo.country = 'China' /* 修改为指定国家 */
                  AND platform = '{0}'
                  -- AND _TABLE_SUFFIX BETWEEN '20190306' AND '20190306' /* 修改为注册日期范围 */
                  AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为注册日期范围 */
    				EXCEPT DISTINCT /* 排除留存用户 */
    				SELECT
    					DISTINCT user_pseudo_id
    				FROM
    					`analytics_188328474.events_*` AS T,
    					T.event_params
    				WHERE
    					event_name = 'user_engagement'
    					AND geo.country = 'China' /* 修改为指定国家 */
    					AND platform = '{0}'
    					AND _TABLE_SUFFIX BETWEEN '{2}' AND '{2}' /* 修改为留存日期范围 */
          )
          GROUP BY user_pseudo_id
    )
) AS A6,
(
    SELECT count(user_pseudo_id) as guide3_end from (
        SELECT
          user_pseudo_id
        FROM
          `analytics_188328474.events_*` AS T,
          T.event_params
        WHERE
          event_name = 'af_track_scene'
          AND event_params.key = 'af_scene'
          AND event_params.value.string_value	= 'guide3_end'
          AND _TABLE_SUFFIX BETWEEN '{1}' AND '{2}'
          AND user_pseudo_id IN (
              SELECT
                  DISTINCT user_pseudo_id
                FROM
                  `analytics_188328474.events_*` AS T,
                  T.event_params
                WHERE
                  event_name = 'first_open'
                  AND geo.country = 'China' /* 修改为指定国家 */
                  AND platform = '{0}'
                  -- AND _TABLE_SUFFIX BETWEEN '20190306' AND '20190306' /* 修改为注册日期范围 */
                  AND _TABLE_SUFFIX BETWEEN '{1}' AND '{1}' /* 修改为注册日期范围 */
    				EXCEPT DISTINCT /* 排除留存用户 */
    				SELECT
    					DISTINCT user_pseudo_id
    				FROM
    					`analytics_188328474.events_*` AS T,
    					T.event_params
    				WHERE
    					event_name = 'user_engagement'
    					AND geo.country = 'China' /* 修改为指定国家 */
    					AND platform = '{0}'
    					AND _TABLE_SUFFIX BETWEEN '{2}' AND '{2}' /* 修改为留存日期范围 */
          )
          GROUP BY user_pseudo_id
    )
) AS A7
