package cn.jho.srpc.core.server;

import static cn.jho.srpc.core.constant.SrpcProtocolConst.COLON_SEPARATOR;
import static cn.jho.srpc.core.constant.SrpcProtocolConst.PAYLOAD;

import cn.jho.srpc.core.SrpcRuntimeException;
import cn.jho.srpc.core.protocol.SrpcRequest;
import cn.jho.srpc.core.protocol.SrpcRequestPayload;
import cn.jho.srpc.core.utils.JacksonUtils;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.Socket;
import java.util.Map;

/**
 * {@link cn.jho.srpc.core.anno.SrpcService}任务
 *
 * @author JHO xu-jihong@qq.com
 */
public class ServiceTask implements Runnable {

    private final Socket client;
    private final Map<String, Object> registeredServices;

    public ServiceTask(Socket client, Map<String, Object> registeredServices) {
        this.client = client;
        this.registeredServices = registeredServices;
    }

    @Override
    public void run() {
        SrpcRequest srpcRequest = read();
        // TODO 校验版本
        System.out.println(srpcRequest);
    }

    private SrpcRequest read() {
        /*
         *  version:1\r\n
         *  content-length:1024\r\n
         *  \r\n
         *  payload:xxxx
         */
        SrpcRequest request = new SrpcRequest();

        try {
            BufferedReader reader = new BufferedReader(new InputStreamReader(client.getInputStream()));

            // 读取版本
            String versionLine = reader.readLine();
            request.setVersion(versionLine.split(COLON_SEPARATOR)[1]);

            // 读取content length
            String contentLengthLine = reader.readLine();
            request.setContentLength(Long.valueOf(contentLengthLine.split(COLON_SEPARATOR)[1]));

            // 读取空行
            int len = System.lineSeparator().length();
            char[] cbuf = new char[len];
            reader.read(cbuf, 0, len);

            // 读取payload
            len = Math.toIntExact(request.getContentLength()) + (PAYLOAD + COLON_SEPARATOR).length();
            cbuf = new char[len];
            reader.read(cbuf, 0, len);
            String payloadLine = new String(cbuf);
            SrpcRequestPayload payload = JacksonUtils.readValue(payloadLine.split(COLON_SEPARATOR, 2)[1],
                    SrpcRequestPayload.class);
            request.setPayload(payload);

            return request;
        } catch (Exception e) {
            throw new SrpcRuntimeException("Failed to read SrpcRequest.", e);
        }
    }

}
