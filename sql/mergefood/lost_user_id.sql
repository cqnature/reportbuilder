SELECT DISTINCT user_pseudo_id
FROM `{0}.events_*` AS T,
     T.event_params
WHERE event_name = 'first_open'
  AND geo.country = '{2}' /* 修改为指定国家 */
  AND platform = '{1}'
  AND _TABLE_SUFFIX BETWEEN '{3}' AND '{3}'
EXCEPT DISTINCT
SELECT user_pseudo_id
FROM `{0}.events_*` AS T,
     T.event_params
WHERE event_name = 'user_engagement'
  AND geo.country = '{2}' /* 修改为指定国家 */
  AND platform = '{1}'
  AND _TABLE_SUFFIX BETWEEN '{4}' AND '{4}'
