package io.github.lagom130.lab.common.feign.decoder

import feign.Response
import feign.codec.ErrorDecoder
import io.github.lagom130.lab.common.core.exception.BizException

class ClientErrorDecoder : ErrorDecoder {
    override fun decode(s: String, response: Response): Exception {
        return BizException(response.status(), response.reason())
    }
}
