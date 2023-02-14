package cn.jho.srpc.core.protocol;

import java.util.Map;

/**
 * <p>SrpcRequestPayLoad class.</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public class SrpcRequestPayLoad {

    private String methodName;
    private Map<String, Object> parameters;
    private Map<String, Object> options;

    public String getMethodName() {
        return methodName;
    }

    public void setMethodName(String methodName) {
        this.methodName = methodName;
    }

    public Map<String, Object> getParameters() {
        return parameters;
    }

    public void setParameters(Map<String, Object> parameters) {
        this.parameters = parameters;
    }

    public Map<String, Object> getOptions() {
        return options;
    }

    public void setOptions(Map<String, Object> options) {
        this.options = options;
    }
}
