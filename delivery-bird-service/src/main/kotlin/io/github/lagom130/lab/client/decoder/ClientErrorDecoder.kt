package io.github.lagom130.lab.client.decoder

import feign.Response
import feign.codec.ErrorDecoder
import io.github.logom130.lab.globalResponse.BizException

class ClientErrorDecoder : ErrorDecoder {
    override fun decode(s: String, response: Response): Exception {
        return BizException(response.status(), response.reason())
    }
}
