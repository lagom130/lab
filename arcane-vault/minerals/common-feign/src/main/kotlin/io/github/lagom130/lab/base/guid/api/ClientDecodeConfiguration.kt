package io.github.lagom130.lab.base.guid.api

import feign.codec.Decoder
import feign.codec.ErrorDecoder
import io.github.lagom130.lab.common.feign.decoder.*
import org.springframework.context.annotation.Bean

class ClientDecodeConfiguration {
    @Bean
    fun resultDecoder(): Decoder {
        return ResultDecoder()
    }

    @Bean
    fun clientErrorDecoder(): ErrorDecoder {
        return ClientErrorDecoder()
    }
}
