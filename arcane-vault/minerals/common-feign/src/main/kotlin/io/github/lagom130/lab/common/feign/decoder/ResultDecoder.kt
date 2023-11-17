package io.github.lagom130.lab.common.feign.decoder

import com.fasterxml.jackson.databind.ObjectMapper
import feign.FeignException
import feign.Response
import feign.Util
import feign.codec.DecodeException
import feign.codec.Decoder
import io.github.lagom130.lab.common.core.exception.BizException
import io.github.lagom130.lab.common.core.vo.GlobalResult
import java.io.IOException
import java.lang.reflect.Type

class ResultDecoder : Decoder {
    private val objectMapper = ObjectMapper()

    @Throws(IOException::class, DecodeException::class, FeignException::class)
    override fun decode(response: Response, type: Type): Any? {
        if (response.body() == null) {
            throw DecodeException(response.status(), "没有返回有效的数据", response.request())
        }
        val bodyStr: String = Util.toString(response.body().asReader(Util.UTF_8))
        //对结果进行转换
        val result: GlobalResult<*> = objectMapper.readValue(bodyStr, GlobalResult::class.java)
        //如果返回错误，且为内部错误，则直接抛出异常
        if (result.code !== 200) {
            throw BizException(500, "接口返回错误：" + result.msg)
        }
        return result.data
    }
}