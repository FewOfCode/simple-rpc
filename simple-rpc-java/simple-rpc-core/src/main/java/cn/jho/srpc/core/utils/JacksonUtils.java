package cn.jho.srpc.core.utils;

import cn.jho.srpc.core.SrpcRuntimeException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

/**
 * <p>JacksonUtils</p>
 *
 * @author JHO xu-jihong@qq.com
 */
public class JacksonUtils {

    private static final ObjectMapper OBJECT_MAPPER = new ObjectMapper();

    private JacksonUtils() {

    }

    public static String writeValueAsString(Object obj) {
        try {
            return OBJECT_MAPPER.writeValueAsString(obj);
        } catch (JsonProcessingException e) {
            throw new SrpcRuntimeException("序列化对象失败", e);
        }
    }

    public static <T> T readValue(String jsonString, Class<T> clazz) {
        try {
            return OBJECT_MAPPER.readValue(jsonString, clazz);
        } catch (JsonProcessingException e) {
            throw new SrpcRuntimeException("反序列化对象失败", e);
        }
    }

}
