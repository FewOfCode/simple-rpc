package cn.jho.srpc.core.protocol;

/**
 * <p>SrpcResponse class.</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public class SrpcResponse extends BaseSrpcProtocol {

    private SrpcResponsePayload payload;

    public SrpcResponsePayload getPayload() {
        return payload;
    }

    public void setPayload(SrpcResponsePayload payload) {
        this.payload = payload;
    }
    
}
