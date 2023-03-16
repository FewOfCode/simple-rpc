/*
 * @Author: zhidal zhidal@qq.com
 * @Date: 2023-02-24 19:46:56
 * @Description: 服务端测试demo
 * @LastEditors: zhidal zhidal@qq.com
 * @LastEditTime: 2023-03-16 14:47:29
 */

import { Server } from '../lib/index.js';
import path from 'node:path';

const server = new Server();

const add = (a, b) => {
  console.log('获取参数', a, b);
  return a + b;
};
const sub = (a, b) => a - b;

console.log('url: ', import.meta);
server.addService(path.resolve('./test_protocol.json'), {
  add,
  sub,
});

server.listen(1840);
