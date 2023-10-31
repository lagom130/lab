package io.github.lagom130.lab.client;

import io.github.lagom130.lab.client.config.ClientDecodeConfiguration;
import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;

@FeignClient(value = "meta-service", configuration = ClientDecodeConfiguration.class)
public interface MetaClient {
    @GetMapping(value = "/snowflakes/global/identifier")
    Long getSnowflakeId();
}
