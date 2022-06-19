SELECT
  ifnull(MAX(event_params.value.int_value), 0) AS max_stage
FROM
  `{0}.events_*` AS T,
  T.event_params
WHERE
  event_name = 'af_pass_stage'
  AND event_params.key = 'af_max_stage'
  AND _TABLE_SUFFIX BETWEEN '{3}'
  AND '{4}' /* 修改为从注册到要查询的留存日期范围 */
  AND user_pseudo_id = '{5}'
  AND event_timestamp <= {6}