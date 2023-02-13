package cn.jho.srpc.core.protocol;

/**
 * <p>SrpcResponsePayload class.</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public class SrpcResponsePayload {

    private Object returnValue;

    public Object getReturnValue() {
        return returnValue;
    }

    public void setReturnValue(Object returnValue) {
        this.returnValue = returnValue;
    }
}
