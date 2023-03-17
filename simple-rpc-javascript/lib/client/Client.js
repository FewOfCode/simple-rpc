/*
 * @Author: zhidal zhidal@qq.com
 * @Date: 2023-02-25 09:43:32
 * @Description: 客户端类
 * @LastEditors: zhidal zhidal@qq.com
 * @LastEditTime: 2023-03-16 14:41:01
 */

import net from 'node:net';

import { readProtocol } from '../common/protocol.js';
class Client {
  port;
  host;
  serverName;
  methods;

  constructor(port, host = 'localhost') {
    this.port = port;
    this.host = host;
    this.methods = {};
  }

  /**
   * @description: 创建socket
   * @param {*} message
   * @param {*} port
   * @return {*}
   */
  createSocket(message, port) {
    // TODO: 创建连接
    return new Promise((resolve, reject) => {
      let socket = net.createConnection(port || this.port, () => {
        socket.write(message);
        socket.on('data', (data) => {
          const decoder = new TextDecoder('utf-8');
          const str = decoder.decode(data);
          console.log(str);
        });
      });
    });
  }

  /**
   * @description: 添加服务
   * @param {*} protocolPath
   * @param {*} methods
   * @return {*}
   */
  addService(protocolPath) {
    const data = readProtocol(protocolPath);
    this.serverName = data.server;
    this.methods = data.method;
  }

  invoke(methodsName, ...args) {
    return new Promise((resolve, reject) => {
      let socket = net.createConnection(this.port, () => {
        socket.write(JSON.stringify([this.serverName, methodsName, ...args]));
        socket.on('data', (data) => {
          const decoder = new TextDecoder('utf-8');
          const str = decoder.decode(data);
          console.log(str);
          resolve(str)
        });
      });
    });
  }
}

export { Client };
