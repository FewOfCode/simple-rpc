package cn.jho.srpc.core.server;

/**
 * <p>SrpcServer interface.</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public interface SrpcServer {

    /**
     * 启动Srpc服务
     */
    void start();

    /**
     * 关闭Srpc服务
     */
    void shutdown();

    /**
     * 注册Rpc服务
     *
     * @param service 需要注册的Rpc服务
     * @throws IllegalAccessException 无效服务
     */
    void register(Object service) throws IllegalAccessException;

}
