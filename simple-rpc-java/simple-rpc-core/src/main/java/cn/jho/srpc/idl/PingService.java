package cn.jho.srpc.idl;

import cn.jho.srpc.core.anno.SrpcService;

/**
 * <p>PingService interface.</p>
 *
 * @author JHO xu-jihong@qq.com
 */
@SrpcService
public interface PingService {

    /**
     * Ping：内置rpc方法
     *
     * @param ping Ping请求
     * @return {@link Pong}
     */
    Pong ping(Ping ping);

}
