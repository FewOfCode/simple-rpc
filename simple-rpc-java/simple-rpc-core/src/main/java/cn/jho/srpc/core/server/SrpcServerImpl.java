package cn.jho.srpc.core.server;

import cn.jho.srpc.core.SrpcRuntimeException;
import cn.jho.srpc.core.anno.SrpcService;
import cn.jho.srpc.core.constant.SrpcConst;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadFactory;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * <p>SrpcServerImpl class.</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public class SrpcServerImpl implements SrpcServer {

    private static final Logger LOGGER = LoggerFactory.getLogger(SrpcServerImpl.class);
    public static final int DEFAULT_CORE_POOL_SIZE = 5;
    public static final int DEFAULT_MAX_POOL_SIZE = 50;
    public static final int DEFAULT_KEEP_ALIVE_TIME = 60;

    private final ExecutorService threadPool;
    private final int port;
    private final Map<String, Object> registeredServices;
    private ServerSocket serverSocket;

    public SrpcServerImpl() {
        this(SrpcConst.DEFAULT_PORT);
    }

    public SrpcServerImpl(int port) {
        this.port = port;
        this.registeredServices = new HashMap<>();
        BlockingQueue<Runnable> workingQueue = new ArrayBlockingQueue<>(100);
        ThreadFactory threadFactory = Executors.defaultThreadFactory();
        this.threadPool = new ThreadPoolExecutor(DEFAULT_CORE_POOL_SIZE, DEFAULT_MAX_POOL_SIZE, DEFAULT_KEEP_ALIVE_TIME,
                TimeUnit.SECONDS, workingQueue, threadFactory);

    }

    @Override
    @SuppressWarnings("java:S106")
    public void start() {
        try {
            serverSocket = new ServerSocket(port);
            System.out.println("Srpc server start.");

            Socket client;
            while ((client = serverSocket.accept()) != null) {
                threadPool.execute(new ServiceTask(client, registeredServices));
            }
        } catch (SocketException e) {
            LOGGER.error("Socket client connection failed.", e);
        } catch (IOException e) {
            throw new SrpcRuntimeException("启动Srpc服务器失败", e);
        }
    }

    @Override
    public void shutdown() {
        try {
            if (serverSocket != null) {
                serverSocket.close();
            }
        } catch (IOException e) {
            throw new SrpcRuntimeException("关闭Srpc服务器失败", e);
        }
    }

    @Override
    public void register(Object service) throws IllegalAccessException {
        Optional<Class<?>> opt = Arrays.stream(service.getClass().getInterfaces())
                .filter(clz -> clz.isAnnotationPresent(SrpcService.class))
                .findAny();

        Class<?> interfaceClazz = opt.orElseThrow(
                () -> new IllegalAccessException("无效的服务：" + service.getClass() + "，无法注册"));

        this.registeredServices.put(interfaceClazz.getName(), service);
    }

    public static void main(String[] args) {
        SrpcServer srpcServer = new SrpcServerImpl();
        srpcServer.start();
    }

}
