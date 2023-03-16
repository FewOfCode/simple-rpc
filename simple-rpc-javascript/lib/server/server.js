/*
 * @Author: zhidal zhidal@qq.com
 * @Date: 2023-02-25 09:36:17
 * @Description: 服务端类
 * @LastEditors: zhidal zhidal@qq.com
 * @LastEditTime: 2023-03-16 15:33:55
 */

import net from 'node:net';
import fs from 'node:fs';

class Server {
  server;
  services;

  constructor() {
    this.server = this.create();
    this.services = {};
  }

  create() {
    const server = net.createServer((socket) => {
      console.log('客户端连接');
      socket.setEncoding('utf-8');
      this.handle(socket);
    });
    return server;
  }

  listen(port, host = 'localhost', listeningListener) {
    this.server.listen(port, host, () => {
      console.log(`服务器开始监听: ${host}:${port}`);
      if (listeningListener) {
        listeningListener();
      }
    });
  }

  addService(protocolPath, methods) {
    console.log('protocolPath: ', protocolPath, methods);
    const res = fs.readFileSync(protocolPath, { encoding: 'utf-8' });
    console.log('读取协议数据:', res);
    const data = JSON.parse(res);
    console.log('解析数据:', data);

    if (!data.server) {
      // 检测服务名
      console.error('协议错误, 未定义server');
    }
    if (data.methods) {
      // TODO: 检测方法
    }
    Reflect.set(this.services, data.server, methods);
    console.log('添加服务: ', this.services);
  }

  handle(socket) {
    socket.on('data', async (data) => {
      // 参数解析, [serviceName, methodName, ...methodArgs]
      try {
        const [serviceName, methodName, ...methodArgs] = JSON.parse(data);
        console.log('serviceName: ', serviceName);
        console.log('methodName: ', methodName);
        console.log('methodArgs: ', methodArgs);
        const res = await this.invokeMethod(
          serviceName,
          methodName,
          ...methodArgs,
        );
        console.log('运行结果: ', res);
        socket.write(JSON.stringify(res));
        socket.end();
      } catch (error) {
        console.error(error);
        socket.write(JSON.stringify(error));
        socket.end();
      }
      // TODO: 调用服务方法
    });
  }

  /**
   * @description: 调用方法
   * @param {*} serviceName
   * @param {*} methodName
   * @param {array} methodArgs
   * @return {*}
   */
  async invokeMethod(serviceName, methodName, ...methodArgs) {
    try {
      if (!this.services[serviceName]) {
        return Promise.reject(`不存在 ${serviceName} 服务!`);
      }
      if (!this.services[serviceName][methodName]) {
        return Promise.reject(`${serviceName} 不存在 ${methodName} 方法!`);
      }
      const method = this.services[serviceName][methodName]
      console.log('method : ', method);
      const res = method(...methodArgs);
      console.log('运行方法结果: ', res);
      return res;
    } catch (error) {
      return Promise.reject(error);
    }
  }
}

export { Server };
