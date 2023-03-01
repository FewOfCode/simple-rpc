package cn.jho.srpc.core.protocol;

import static cn.jho.srpc.core.constant.SrpcProtocolConst.CONTENT_LENGTH;
import static cn.jho.srpc.core.constant.SrpcProtocolConst.PAYLOAD;
import static cn.jho.srpc.core.constant.SrpcProtocolConst.VERSION;

import cn.jho.srpc.core.utils.JacksonUtils;
import java.nio.charset.StandardCharsets;

/**
 * <p>SrpcRequest class.</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public class SrpcRequest extends BaseSrpcProtocol {

    private SrpcRequestPayload payload;

    public SrpcRequestPayload getPayload() {
        return payload;
    }

    public void setPayload(SrpcRequestPayload payload) {
        this.payload = payload;
    }

    public byte[] toPacket() {
        return toString().getBytes(StandardCharsets.UTF_8);
    }

    @Override
    public String toString() {
        String payloadStr = JacksonUtils.writeValueAsString(payload);
        return VERSION + ":" + version
                + System.lineSeparator()
                + CONTENT_LENGTH + ":" + payloadStr.getBytes(StandardCharsets.UTF_8).length
                + System.lineSeparator()
                + System.lineSeparator()
                + PAYLOAD + ":" + payloadStr;
    }
}
