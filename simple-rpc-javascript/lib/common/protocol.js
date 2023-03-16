/*
 * @Author: zhidal zhidal@qq.com
 * @Date: 2023-02-27 16:40:25
 * @Description: 协议信息处理
 * @LastEditors: zhidal zhidal@qq.com
 * @LastEditTime: 2023-02-27 16:52:54
 */

import fs from 'node:fs';

function readProtocol(filepath) {
  const res = fs.readFileSync(filepath, { encoding: 'utf-8' });
  console.log('读取协议数据:', res);
  const data = JSON.parse(res);
  console.log('解析数据:', data);
  if (!data.server) {
    // 检测服务名
    throw Error('协议错误, 未定义server');
  }
  return data;
}

export { readProtocol };
