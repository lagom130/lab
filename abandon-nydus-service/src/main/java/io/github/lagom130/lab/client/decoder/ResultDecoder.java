package io.github.lagom130.lab.client.decoder;

import com.fasterxml.jackson.databind.JavaType;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.TypeFactory;
import feign.FeignException;
import feign.Response;
import feign.Util;
import feign.codec.DecodeException;
import feign.codec.Decoder;
import io.github.lagom130.lab.globalResponse.Result;

import java.io.IOException;
import java.lang.reflect.Type;
import java.net.BindException;

public class ResultDecoder implements Decoder {
    private ObjectMapper objectMapper = new ObjectMapper();
    @Override
    public Object decode(Response response, Type type) throws IOException, DecodeException, FeignException {
        if (response.body() == null) {
            throw new DecodeException(response.status(), "没有返回有效的数据", response.request());
        }
        String bodyStr = Util.toString(response.body().asReader(Util.UTF_8));
        //对结果进行转换
        JavaType javaType = TypeFactory.defaultInstance().constructType(Result.class);
        Result result = objectMapper.readValue(bodyStr, javaType);
        //如果返回错误，且为内部错误，则直接抛出异常
        if (result.getCode() != 200) {
            throw new BindException("接口返回错误：" + result.getMsg());
        }
        return result.getData();
    }
}