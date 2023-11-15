package io.github.lagom130.lab.client.config

import feign.codec.Decoder
import feign.codec.ErrorDecoder
import io.github.lagom130.lab.client.decoder.ClientErrorDecoder
import io.github.lagom130.lab.client.decoder.ResultDecoder
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
