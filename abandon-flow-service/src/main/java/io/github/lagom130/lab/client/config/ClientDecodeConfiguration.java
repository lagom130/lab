package io.github.lagom130.lab.client.config;

import feign.codec.Decoder;
import feign.codec.ErrorDecoder;
import io.github.lagom130.lab.client.decoder.ClientErrorDecoder;
import io.github.lagom130.lab.client.decoder.ResultDecoder;
import org.springframework.context.annotation.Bean;

public class ClientDecodeConfiguration {
    @Bean
    public Decoder resultDecoder() {
        return new ResultDecoder();
    }

    @Bean
    public ErrorDecoder clientErrorDecoder() {
        return new ClientErrorDecoder();
    }
}
