/*
 * @Author: zhidal zhidal@qq.com
 * @Date: 2023-02-24 19:47:17
 * @Description: 客户端测试demo
 * @LastEditors: zhidal zhidal@qq.com
 * @LastEditTime: 2023-03-16 15:22:21
 */

import { Client } from '../lib/index.js';
import path from 'node:path';

const file = path.resolve('./test_protocol.json');
console.log('path: ', file);
const client = new Client(1840);
client.addService(file);
client
  .invoke('add', 1, 2)
  .then((res) => {
    console.log('add res: ', res);
  })
  .catch((error) => {
    console.error(error);
  });
