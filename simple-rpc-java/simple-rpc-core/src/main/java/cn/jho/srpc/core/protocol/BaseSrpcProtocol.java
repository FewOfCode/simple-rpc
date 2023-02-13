package cn.jho.srpc.core.protocol;

/**
 * <p>SrpcProtocol class.</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public abstract class BaseSrpcProtocol {

    protected String version;
    protected Long contentLength;

    public String getVersion() {
        return version;
    }

    public void setVersion(String version) {
        this.version = version;
    }

    public Long getContentLength() {
        return contentLength;
    }

    public void setContentLength(Long contentLength) {
        this.contentLength = contentLength;
    }


}
