SELECT
   DISTINCT app_info.version as app_version
FROM
  `{0}.events_*` AS T,
  T.event_params
WHERE
  event_name = 'first_open'
  AND geo.country = '{2}' /* 修改为指定国家 */
  AND platform = '{1}'
  AND _TABLE_SUFFIX BETWEEN '{3}' AND '{3}' /* 修改为events数据范围 */
ORDER BY app_version
