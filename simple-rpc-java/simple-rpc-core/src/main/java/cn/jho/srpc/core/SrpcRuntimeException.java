package cn.jho.srpc.core;

/**
 * <p>SrpcRuntimeException</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public class SrpcRuntimeException extends RuntimeException {

    public SrpcRuntimeException(String message) {
        super(message);
    }

    public SrpcRuntimeException(Throwable cause) {
        super(cause);
    }

    public SrpcRuntimeException(String message, Throwable cause) {
        super(message, cause);
    }

}
