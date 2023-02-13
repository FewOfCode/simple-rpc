package cn.jho.srpc.core.protocol;

/**
 * <p>SrpcRequest class.</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public class SrpcRequest extends BaseSrpcProtocol {

    private SrpcRequestPayLoad payload;

    public SrpcRequestPayLoad getPayload() {
        return payload;
    }

    public void setPayload(SrpcRequestPayLoad payload) {
        this.payload = payload;
    }

}
