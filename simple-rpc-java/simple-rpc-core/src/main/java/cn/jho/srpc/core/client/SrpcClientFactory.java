package cn.jho.srpc.core.client;

import static cn.jho.srpc.core.constant.SrpcConst.DEFAULT_HOST;
import static cn.jho.srpc.core.constant.SrpcConst.DEFAULT_PORT;
import static cn.jho.srpc.core.constant.SrpcProtocolConst.JAVA_INTERFACE_NAME;
import static cn.jho.srpc.core.constant.SrpcProtocolConst.PROTOCOL_VERSION_V1;

import cn.jho.srpc.core.protocol.SrpcRequest;
import cn.jho.srpc.core.protocol.SrpcRequestPayload;
import cn.jho.srpc.core.protocol.SrpcResponse;
import cn.jho.srpc.idl.Ping;
import cn.jho.srpc.idl.PingService;
import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.lang.reflect.Parameter;
import java.lang.reflect.Proxy;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * <p>SrpcClient class.</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public class SrpcClientFactory implements InvocationHandler {

    private final SrpcClientTransfer clientTransfer;

    public SrpcClientFactory() {
        this(DEFAULT_HOST, DEFAULT_PORT);
    }

    public SrpcClientFactory(String host, int port) {
        this.clientTransfer = new SrpcClientTransfer(host, port);
    }

    @SuppressWarnings("unchecked")
    public <T> T getService(Class<T> clazz) {
        return (T) Proxy.newProxyInstance(clazz.getClassLoader(), new Class<?>[]{clazz}, this);
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        SrpcRequest request = new SrpcRequest();
        request.setVersion(PROTOCOL_VERSION_V1);
        request.setPayload(buildPayload(method, args));

        SrpcResponse response = clientTransfer.request(request);
        return response.getPayload().getReturnValue();
    }

    private SrpcRequestPayload buildPayload(Method method, Object[] args) {
        SrpcRequestPayload payload = new SrpcRequestPayload();
        payload.setMethodName(method.getName());

        Parameter[] params = method.getParameters();
        Map<String, Object> payloadParams = new LinkedHashMap<>();
        for (int i = 0; i < params.length; i++) {
            Parameter param = params[i];
            payloadParams.put(param.getName(), args[i]);
        }
        payload.setParameters(payloadParams);

        Map<String, Object> options = new HashMap<>();
        options.put(JAVA_INTERFACE_NAME, method.getDeclaringClass().getName());
        payload.setOptions(options);

        return payload;
    }

    public static void main(String[] args) {
        SrpcClientFactory factory = new SrpcClientFactory();
        PingService service = factory.getService(PingService.class);
        Ping ping = new Ping();
        ping.setName("jho");
        service.ping(ping);
    }

}
