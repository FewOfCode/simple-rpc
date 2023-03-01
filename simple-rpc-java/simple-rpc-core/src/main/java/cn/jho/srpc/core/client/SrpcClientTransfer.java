package cn.jho.srpc.core.client;

import cn.jho.srpc.core.protocol.SrpcRequest;
import cn.jho.srpc.core.protocol.SrpcResponse;
import cn.jho.srpc.core.protocol.SrpcResponsePayload;
import cn.jho.srpc.core.utils.JacksonUtils;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.Socket;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * <p>SrpcClientTransfer</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public class SrpcClientTransfer {

    private static final Logger LOGGER = LoggerFactory.getLogger(SrpcClientTransfer.class);

    private final String host;
    private final int port;

    public SrpcClientTransfer(String host, int port) {
        this.host = host;
        this.port = port;
    }

    public SrpcResponse request(SrpcRequest request) throws IOException {
        LOGGER.info("Request {}:{} with packet {}", host, port, request);

        try (Socket socket = new Socket(host, port)) {
            OutputStream out = socket.getOutputStream();
            out.write(request.toPacket());
            out.flush();

            InputStream in = socket.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(in));

            SrpcResponse response = new SrpcResponse();
            /*
                version:1\r\n
                content-length:1024\r\n
                \r\n
                payload:xxxx
             */
            String line = reader.readLine();
            String[] split = line.replace("\r\n", "").split(":");
            // TODO 校验版本
            if (split.length > 1) {
                response.setVersion(split[1]);
            }

            line = reader.readLine();
            split = line.replace("\r\n", "").split(":");
            if (split.length > 1) {
                response.setContentLength(Long.valueOf(split[1]));
            }

            StringBuilder sb = new StringBuilder();
            while ((line = reader.readLine()) != null) {
                sb.append(line);
            }
            String payloadInfo = sb.toString();
            split = payloadInfo.split(":", 2);
            if (split.length > 1) {
                SrpcResponsePayload payload = JacksonUtils.readValue(split[1], SrpcResponsePayload.class);
                response.setPayload(payload);
            }

            return response;
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

}
