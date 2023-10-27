package io.github.lagom130.lab.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;

@FeignClient("meta-service")
public interface MetaClient {
    @GetMapping(value = "/snowflakes/global/identifier")
    Long getSnowflakeId();
}
